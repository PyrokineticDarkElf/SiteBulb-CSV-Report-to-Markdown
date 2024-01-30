import os
import pandas as pd
from urllib.parse import quote
import re
from includes.config import CONFIG

def load_csv(file_path):
    return pd.read_csv(file_path)

def map_importance(value):
    importance_mapping = CONFIG['importance_map']
    mapped_value = importance_mapping.get(value, {}).get('value', 0)
    print(f"Mapping Importance: Value={value}, Mapped Value={mapped_value}")
    return mapped_value


def map_section_emoji(section):
    section_mapping = CONFIG['section_map']
    return section_mapping.get(section, '')

def find_input_csv():
    # List all files in the input folder
    files = os.listdir(CONFIG['input_folder'])
    # Find the first file with a CSV extension
    for file in files:
        if file.lower().endswith('.csv'):
            return os.path.join(CONFIG['input_folder'], file)
    # If no CSV file is found, return None
    return None

def write_heading(md_file, heading_weight, heading, mapping):
    if mapping is None:
        compiled_heading = f"{heading_weight} {heading}"
        md_file.write(f"{compiled_heading}\n")
        return
    # Check if the heading value has an emoji mapping
    map_data = mapping.get(heading, {})
    emoji = map_data.get('emoji', '') + " " if map_data.get('emoji', '') is not None else ""
    name = map_data.get('name', '')
    print(f"Debug - Heading: {heading}, Emoji: {emoji}, Name: {name}")

    # Write heading with emoji
    compiled_heading = f"{heading_weight} {emoji}{name}"
    print(f"Heading: {compiled_heading}")
    md_file.write(f"{compiled_heading}\n")

def create_markdown():
    # Find input CSV file
    input_csv = find_input_csv()
    map_csv = os.path.join(CONFIG['data_folder'], 'map.csv')

    if not os.path.exists(input_csv) or not os.path.exists(map_csv):
        print("CSV files not found.")
        return

    # Load CSV files
    df_input = load_csv(input_csv)
    df_map = load_csv(map_csv)

    # Map Importance values
    df_input['importance_rank'] = df_input['Importance'].apply(map_importance)

    # Order DataFrame based on "importance_rank" column
    df_input.sort_values(by='importance_rank', ascending=False, inplace=True)

    # Get unique sections
    unique_sections = df_input['Section'].astype(str).unique()

    # Create markdown file
    if CONFIG['separate_files'] == 'y':
        print(f"All sections: {unique_sections}")
        
        # Iterate through unique section headings
        for section in unique_sections:
            print(f"Starting '{section}' section.")
            # Create markdown file
            output_md = os.path.join(CONFIG['output_folder'], f'{section}.md')
            # Call write section function
            write_section_md(output_md, df_input, str(section), df_map)
            print(f"Markdown file '{output_md}' created successfully.")
    else:
        print(f"All sections: {unique_sections}")
        print(f"Starting " + CONFIG['short_file_name'] + ".")
        # Create markdown file
        output_md = os.path.join(CONFIG['output_folder'], CONFIG['short_file_name'])
        # Call write section function
        write_section_md(output_md, df_input, str(unique_sections), df_map)        
        print(f"Markdown file '{output_md}' created successfully.")




def write_section_md(output_md, df_input, unique_sections, df_map):
    with open(output_md, 'w', encoding='utf-8') as md_file:
        # Check if unique_sections is iterable
        if isinstance(unique_sections, (str, int)):
            # If it's a single value, create a list to iterate
            unique_sections = [unique_sections]

        for section in unique_sections:
            # Filter DataFrame for the current section heading
            df_section = df_input[df_input["Section"] == section]
            print(f"Section: {section}, DataFrame structure:\n{df_section}")
            if CONFIG['section_title'] == 'y':
                # Write section heading with emoji function
                mapping = CONFIG['section_map']
                heading_weight = "#" if CONFIG['separate_files'] == 'y' else "##"
                write_heading(md_file, heading_weight, str(section), mapping)

            # Get unique importance values within the section
            unique_importance = df_section["Importance"].astype(str).unique()
            print(f"Unique Importance Values: '{unique_importance}'")

            # Iterate through unique importance values
            for importance in unique_importance:
                # Filter DataFrame for the current section and importance
                df_section_importance = df_section[df_section["Importance"] == importance]
                
                # Write importance heading with emoji function
                mapping = CONFIG['importance_map']
                heading_weight = "##" if CONFIG['separate_files'].lower() == 'y' else "###"
                write_heading(md_file, heading_weight, importance, mapping)

                write_table(md_file, df_section_importance, df_map)

                md_file.write("\n")



def write_table(md_file, df_section_importance, df_map):
    if CONFIG['length'] == 'short':
        md_file.write("| Issue | Type | Impacted URLs | Priority |\n")
        md_file.write("|------|------|------|------|\n")
    # Iterate through sorted merged data for the current section and importance
    for _, row in df_section_importance.iterrows():
        # Create a Markdown table using table function
        write_table_row(md_file, row, df_map)

    

def write_extras_md(md_file, df_map_row):
    for column_header in CONFIG['extra_columns']:
        heading_type = "####" if CONFIG['separate_files'].lower() == 'y' else "#####"
        write_heading(md_file, heading_type, column_header, mapping=None)
        if not df_map_row.empty and column_header in df_map_row.columns:
            # Check if the column exists and the DataFrame is not empty
            values = df_map_row[column_header].values
            if len(values) > 0:
                md_file.write(f"{values[0]} ")
        md_file.write("\n")



def write_table_row(md_file, row, df_map):
    hint = row.get("Hint", "")
    
    # Query df_map for the given hint
    df_map_row = df_map[df_map['Hint'] == hint]

    if not df_map_row.empty:
        hint = df_map_row.get("Hint", "").iloc[0]
        hint_type = df_map_row.get("Type", "").iloc[0]
        description = df_map_row.get("Description", "").iloc[0]
        learn_more = df_map_row.get("Learn More", "").iloc[0]

        # Fallback to input data if there's no value in df_map
        if pd.isna(hint):
            hint = row.get("Hint", "")
        if pd.isna(hint_type):
            hint_type = row.get("Warning Type", "") # NEED TO RUN MAP!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        if pd.isna(description):
            description = row.get("Description", "")
        if pd.isna(learn_more):
            learn_more = row.get("Learn More", "")
    else:
        # Fallback to input data if df_map_row is empty
        hint = row.get("Hint", "")
        hint_type = row.get("Warning Type", "") # NEED TO RUN MAP!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        description = row.get("Description", "")
        learn_more = row.get("Learn More", "")

    # Src data
    importance = row.get("Importance", "")
    urls = row.get("URLs", "")
    impacted_pages = float(row.get("Coverage", ""))
    sheet_url = row.get("Sheet URL", "")

    # Add Links
    linked_hint = f"[{hint}]({learn_more})" if CONFIG['include_links'] == 'y' else hint
    linked_urls = f"[{urls}]({sheet_url})" if CONFIG['include_links'] == 'y' else urls
    # Calculate Priority
    print(f"Importance: {importance}")
    importance_value = float(CONFIG['importance_map'].get(importance, {}).get('value', ''))
    priority = f"{round(impacted_pages * ((importance_value * 2) / 10), 2)}%"

    if CONFIG['length'] == 'long':
        heading_type = "###" if CONFIG['separate_files'].lower() == 'y' else "####"
        md_file.write(f"{heading_type} {linked_hint}\n")
        md_file.write("| Type | Impacted URLs | Priority |\n")
        md_file.write("|------|------|------|\n")
        md_file.write(f"| {hint_type} | {linked_urls} ({impacted_pages}%) | {priority} |\n")
        md_file.write(f"{description} \n")
        if len(CONFIG['extra_columns']) > 0:
            write_extras_md(md_file, df_map_row)
    else:
        md_file.write(f"| {linked_hint} | {hint_type} | {linked_urls} ({impacted_pages}%) | {priority} |\n")


# Make some sick reports!
create_markdown()
