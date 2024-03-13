import os
import pandas as pd
from urllib.parse import quote
import re
from includes.config import CONFIG
import html

def load_csv(file_path):
    return pd.read_csv(file_path)

def map_values(value, query_map, query):
    # If the value is not in the importance map, use the entry with 'value': 0 as fallback
    fallback_entry = query_map.get('Unknown', {'name': 'Unknown', 'value': 0, 'emoji': '⚫'})
    
    # Retrieve the fallback value dynamically from the fallback entry
    fallback_value = fallback_entry.get(query, fallback_entry[query])

    # Get the mapped value from the query_map or use the fallback_value
    mapped_value = query_map.get(value, fallback_entry).get(query, fallback_value)

    print(f"Mapping Importance: Value={value}, Mapped Value={mapped_value}")
    return mapped_value


def find_input_csv():
    # List all files in the input folder
    files = os.listdir(CONFIG['input_folder'])
    # Find the first file with a CSV extension
    for file in files:
        if file.lower().endswith('.csv'):
            return os.path.join(CONFIG['input_folder'], file)
    # If no CSV file is found, return None
    return None

def write_heading(md_file, heading_weight, heading, emoji):
    if emoji != None:
        compiled_heading = f"{heading_weight} {emoji} {heading}"
    else:
        compiled_heading = f"{heading_weight} {heading}"
    # Write heading with emoji
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
    df_input['importance_rank'] = df_input['Importance'].apply(lambda x: map_values(x, CONFIG['importance_map'], query='value'))

    # Order DataFrame based on "importance_rank" column
    df_input.sort_values(by='importance_rank', ascending=False, inplace=True)

    # Get unique sections
    unique_sections = df_input['Section'].astype(str).unique()

    # Create markdown file
    if CONFIG['separate_files'] == 'y':
        # print(f"All sections: {unique_sections}")
        
        # Iterate through unique section headings
        for section in unique_sections:
            print(f"Starting '{section}' section.")
            # Create markdown file
            output_md = os.path.join(CONFIG['output_folder'], f'{section}.md')
            # Call write section function
            write_section_md(output_md, df_input, str(section), df_map)
            print(f"Markdown file '{output_md}' created successfully.")
    else:
        # print(f"All sections: {unique_sections}")
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
                section_title = str(section)
                heading = map_values(section_title, CONFIG["section_map"], query='name')
                if heading == 'Unknown':
                    heading = section_title
                print(heading)
                emoji = map_values(section_title, CONFIG["section_map"], query='emoji')
                heading_weight = "#" if CONFIG['separate_files'] == 'y' else "##"
                write_heading(md_file, heading_weight, heading, emoji)

            # Get unique importance values within the section
            unique_importance = df_section["Importance"].astype(str).unique()
            print(f"Unique Importance Values: '{unique_importance}'")

            # Iterate through unique importance values
            for importance in unique_importance:
                # Filter DataFrame for the current section and importance
                df_section_importance = df_section[df_section["Importance"] == importance]
                
                # Write importance heading with emoji function
                heading = map_values(importance, CONFIG["importance_map"], query='name')
                emoji = map_values(importance, CONFIG["importance_map"], query='emoji')
                heading_weight = "##" if CONFIG['separate_files'].lower() == 'y' else "###"
                write_heading(md_file, heading_weight, heading, emoji)

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
        if not df_map_row.empty and column_header in df_map_row.columns:
            # Check if the column exists and the DataFrame is not empty
            values = df_map_row[column_header].values
            if len(values) > 0:
                heading_type = "####" if CONFIG['separate_files'].lower() == 'y' else "#####"
                write_heading(md_file, heading_type, column_header, emoji=None)
                values = [str(val) for val in values]
                md_file.write(f"{html.escape(' '.join(values))}\n")
                md_file.write("\n")
            md_file.write("\n")



def write_table_row(md_file, row, df_map):
    hint = row.get("Hint", "")
    
    # Query df_map for the given hint
    df_map_row = df_map[df_map['Hint'] == hint]

    if not df_map_row.empty:
        # Use the custom hint or fallback to the mappable hint
        if df_map_row.get("Hint Column"):
            hint = html.escape(df_map_row.get("Hint Column", "").iloc[0])
        else:
            hint = df_map_row.get("Hint", "").iloc[0]
            hint = html.escape(str(hint)) if hint else ""

        hint_type = df_map_row.get("Type", "").iloc[0]
        description = df_map_row.get("Description", "").iloc[0]
        description = html.escape(str(description)) if description else ""
        learn_more = df_map_row.get("Learn More", "").iloc[0]

        # Fallback to input data if there's no value in df_map
        if pd.isna(hint):
            hint = row.get("Hint", "")
            hint = html.escape(str(hint)) if hint else ""
        if pd.isna(hint_type):
            hint_type = map_values(row.get("Warning Type", ""), CONFIG['warning_type_map'], query='name')
        if pd.isna(description):
            description = row.get("Description", "")
            description = html.escape(str(description)) if description else ""            
        if pd.isna(learn_more):
            learn_more = row.get("Learn More", "")
    else:
        # Fallback to input data if df_map_row is empty
        hint = row.get("Hint", "")
        hint = html.escape(str(hint)) if hint else ""
        hint_type = map_values(row.get("Warning Type", ""), CONFIG['warning_type_map'], query='name')
        description = row.get("Description", "")
        description = html.escape(str(description)) if description else ""
        learn_more = row.get("Learn More", "")

    # Src data
    importance = row.get("Importance", "")
    urls = row.get("URLs", "")
    impacted_pages = float(row.get("Coverage", ""))
    sheet_url = row.get("Sheet URL", "")

    # Add Links
    linked_hint = f"[{hint}]({learn_more})" if CONFIG['include_resource_links'] == 'y' else hint
    linked_urls = f"[{urls}]({sheet_url})" if CONFIG['include_sheets_links'] == 'y' else urls
    # Calculate Priority
    # print(f"Importance: {importance}")
    importance_value = float(map_values(importance, CONFIG['importance_map'], 'value'))
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
