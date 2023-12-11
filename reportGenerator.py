import os
import pandas as pd
from urllib.parse import quote
import re

# Configuration
CONFIG = {
    'input_folder': './input',
    'output_folder': './output',
    'data_folder': './data',
    'length': 'long', # 'short' or 'long'
    'separate_files': 'y', # 'y' or 'n'
    'short_file_name': 'Report.md',
    'include_links': 'y', # 'y' or 'n'
    'importance_order': {'Critical': 5, 'High': 4, 'Medium': 3, 'Low': 2, 'No Issue': 1, 'Unknown': 0},
    'importance_emoji_map': {'Critical': '💣', 'High': '🔴', 'Medium': '🟠', 'Low': '🟡', 'No Issue': '🔵', 'Unknown': '🟣'},
    'section_emoji_map': {
        'Accessibility': '♿️',
        'AMP': '⚡',
        'Duplicate Content': '🔄',
        'Indexability': '🔍',
        'Internal': '🏠',
        'International': '🌐',
        'Links': '🔗',
        'Mobile Friendly': '📱',
        'On Page': '📄',
        'Performance': '⚙️',
        'Redirects': '➡️',
        'Rendered': '🖼️',
        'Search Traffic': '🔍🚦',
        'Security': '🔒',
        'XML Sitemaps': '🗺️'
    },
    'src_column': 'Learn More',  # Source column for the merge
    'map_column': 'Learn More ML',  # Map column for the merge
    # Fallback mapping
    'column_fallbacks': {
        'Section ML': {'fallback_column': 'Section'}, # The column Section ML falls back to Section
        'Hint ML': {'fallback_column': 'Hint'}, # The column Hint ML falls back to Hint
        'Learn More ML': {'fallback_column': 'Learn More'}, # The column Learn More ML falls back to Learn More
        'Importance ML': {'fallback_column': 'Importance', 'remove_non_alpha': True, 'replace': {'None': 'No Issue'}}, # The column Importance ML falls back to Importance with aditional options to remove text and replace text
        'Type ML': {'fallback_column': 'Warning Type', 'remove_non_alpha': True}, # The column Type ML falls back to Warning Type with aditional options to remove text
        'Description ML': {'replacement': 'Not Available'}, # The column Description ML falls back to text "Not Available"
    },
}

def find_input_csv():
    # List all files in the input folder
    files = os.listdir(CONFIG['input_folder'])
    # Find the first file with a CSV extension
    for file in files:
        if file.lower().endswith('.csv'):
            return os.path.join(CONFIG['input_folder'], file)
    # If no CSV file is found, return None
    return None

# Replace special characters in the given text.
def replace_special_characters(text):
    return str(text).replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')
# Function to remove non-alpha and non-space characters
def remove_non_alpha(text):
    # Remove non-alphabetic characters except space
    text = re.sub(r'[^a-zA-Z\s]', '', str(text))
    # Remove spaces that come before a-zA-Z
    text = re.sub(r'\s+([a-zA-Z])', r'\1', text)
    return text

# Fallback mapping
# Fallback mapping
def process_fallbacks(df, column, config):
    fallback_column = config.get(column, {}).get('fallback_column')
    remove_non_alpha_func = config.get(column, {}).get('remove_non_alpha', False)
    replace_dict = config.get(column, {}).get('replace', {})
    
    replacement = config.get(column, {}).get('replacement')  # New line to get the replacement value

    if fallback_column is not None:
        df[column].fillna(df[fallback_column], inplace=True)

    if replace_dict:
        df[column].replace(replace_dict, inplace=True)

    if callable(remove_non_alpha_func):  # Check if remove_non_alpha is a callable function
        df[column] = df[column].apply(lambda x: remove_non_alpha_func(x) if pd.notna(x) else x)
    elif remove_non_alpha_func:  # Check if remove_non_alpha is True
        df[column] = df[column].apply(lambda x: remove_non_alpha(x) if pd.notna(x) else x)

    if replacement is not None:  # New condition to check for replacement
        df[column] = df[column].fillna(replacement)

def write_heading(md_file, heading_type, heading_value, emoji_map):
    # Check if the heading value has an emoji mapping
    emoji_value = emoji_map.get(heading_value, '')
    # Write heading with emoji
    md_file.write(f"{heading_type} {emoji_value} {heading_value}\n")

def write_table_row(md_file, row, df_map):
    # Data mapping
    hint = replace_special_characters(row.get("Hint ML", ""))
    type_column = row.get("Type ML", "")
    description_column = replace_special_characters(row.get("Description ML", ""))
    urls_column = row.get("URLs", "")
    impacted_pages_column = row.get("Impacted Pages (%)", "")
    learn_more_column = row.get("Learn More ML", "")
    sheet_url_column = row.get("Sheet URL", "")
    importance_column = row.get("Importance ML", "")
    # Add Links
    linked_hint = f"[{hint}]({learn_more_column})" if CONFIG['include_links'] == 'y' else hint
    linked_urls = f"[{urls_column}]({sheet_url_column})" if CONFIG['include_links'] == 'y' else urls_column
    # Calculate Priority
    importance_value = CONFIG['importance_order'].get(importance_column, 0)
    priority = f"{round(impacted_pages_column * ((importance_value * 2) / 10), 2)}%"

    if CONFIG['length'] == 'long':
        heading_type = "###" if CONFIG['separate_files'].lower() == 'y' else "####"
        md_file.write(f"{heading_type} {linked_hint}\n")
        md_file.write("| Type | Impacted URLs | Priority |\n")
        md_file.write("|------|------|------|\n")
        md_file.write(f"| {type_column} | {linked_urls} ({impacted_pages_column}%) | {priority} |\n")
        md_file.write(f"{description_column} \n")
    else:
        md_file.write(f"| {linked_hint} | {type_column} | {linked_urls} ({impacted_pages_column}%) | {priority} |\n")

def create_markdown():
    # Find input CSV file
    input_csv = find_input_csv()

    if input_csv is None:
        print("No CSV file found in the input folder.")
        return

    # Read input CSV file into a DataFrame
    df_input = pd.read_csv(input_csv)

    # Read map CSV file into a DataFrame
    map_csv = os.path.join(CONFIG['data_folder'], 'map.csv')
    df_map = pd.read_csv(map_csv)

    # Merge input and map DataFrames based on the "Hint" column
    df_merged = pd.merge(df_input, df_map, left_on=CONFIG['src_column'], right_on=CONFIG['map_column'], how='left')

    # Handle NaN values in the merged DataFrame
    for column in CONFIG['column_fallbacks']:
        process_fallbacks(df_merged, column, CONFIG['column_fallbacks'])

    # Order DataFrame based on "Custom Importance" column
    if "Importance ML" in df_merged.columns:
        df_merged.sort_values(by="Importance ML", key=lambda x: x.map(CONFIG['importance_order']), inplace=True, ascending=False)

    # Get unique section headings
    unique_section_headings_ml = df_merged["Section ML"].unique() if "Section ML" in df_merged.columns else []
    unique_section_headings_map = df_map["Section ML"].unique() if "Section ML" in df_map.columns else []

    # Filter out sections with no hints
    valid_sections = df_merged.loc[~df_merged["Hint ML"].isna(), "Section ML"].unique()

    unique_section_headings = (
        [section for section in unique_section_headings_ml if section in valid_sections]
        if len(unique_section_headings_ml) > 0 and all(pd.notna(x) for x in unique_section_headings_ml)
        else [section for section in unique_section_headings_map if section in valid_sections]
    ) or df_merged["Section"].unique()

    # Ensure that it's a list, even if there's only one element
    unique_section_headings = [unique_section_headings] if isinstance(unique_section_headings, (str, int)) else unique_section_headings

    if CONFIG['separate_files'].lower() == 'y':
        # Iterate through unique section headings
        for section_heading in unique_section_headings:
            print(f"Starting '{section_heading}' section.")
            # Create markdown file
            output_md = os.path.join(CONFIG['output_folder'], f'{section_heading}.md')
            # Call write section function
            write_section_md(output_md, df_merged, section_heading, df_map)
            print(f"Markdown file '{output_md}' created successfully.")
    else:
        print(f"Starting " + CONFIG['short_file_name'] + ".")
        # Create markdown file
        output_md = os.path.join(CONFIG['output_folder'], CONFIG['short_file_name'])
        # Call write section function
        write_section_md(output_md, df_merged, unique_section_headings, df_map)        
        print(f"Markdown file '{output_md}' created successfully.")

def write_section_md(output_md, df_merged, unique_section_headings, df_map):
    with open(output_md, 'w', encoding='utf-8') as md_file:
        # Check if unique_section_headings is iterable
        if isinstance(unique_section_headings, (str, int)):
            # If it's a single value, create a list to iterate
            unique_section_headings = [unique_section_headings]

        for section_heading in unique_section_headings:
            # Filter DataFrame for the current section heading
            df_section = df_merged[df_merged["Section ML"] == section_heading]
            # Write section heading with emoji function
            emoji_map = CONFIG['section_emoji_map']
            heading_type = "#" if CONFIG['separate_files'].lower() == 'y' else "##"
            write_heading(md_file, heading_type, section_heading, emoji_map)
            
            # Get unique importance values within the section
            unique_importance_values = df_section["Importance ML"].unique()
            print(f"Unique Importance Values: '{unique_importance_values}'")

            # Iterate through unique importance values
            for importance_value in unique_importance_values:
                # Filter DataFrame for the current section and importance value
                df_section_importance = df_section[df_section["Importance ML"] == importance_value]
                
                # Write importance heading with emoji function
                emoji_map = CONFIG['importance_emoji_map']
                heading_type = "##" if CONFIG['separate_files'].lower() == 'y' else "###"
                write_heading(md_file, heading_type, importance_value, emoji_map)

                if CONFIG['length'] == 'short':
                    md_file.write("| Issue | Type | Impacted URLs | Priority |\n")
                    md_file.write("|------|------|------|------|\n")
                # Iterate through sorted merged data for the current section and importance value
                for _, row in df_section_importance.iterrows():
                    # Create a Markdown table using table function
                    write_table_row(md_file, row, df_map)

                md_file.write("\n")

# Make some sick ass reports!
create_markdown()