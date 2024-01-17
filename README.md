# SiteBulb CSV Report to Markdown

## Overview
This script generates markdown reports based on input CSV files containing data related to website issues. The generated reports include information about different sections, hints, types of warnings, and their respective details.

The general use case of this script would be to generate a custom report based on SiteBulb's provided data. You can get an export from SiteBulb containing lists of all the URLs that have issues.

The report can then be generated, linking items by type of issue, and injecting emojis to represent section headings and importance values. and most importantly, offering you the ability to write your own custom Hints, Descriptions and links. This allows you to effectively hide the origin of the data (SiteBulb), in favor of your own custom-written 'descriptions' and 'explination' links.

## Prerequisites
- Python 3.x
- Pandas library

## Usage
1. Generate your reports in SiteBulb. This script uses the 'All Hints' report which should contain hints from all the issues your site faces. This report is generated in Google Drive and the final markdown file(s) will use the Google Drive spreadsheet links in their copy.
2. Place your input CSV files in the `./input` folder.
3. Configure the script using the `CONFIG` dictionary in the script file.
4. Run the script using the following command:

```bash
python reportGenerator.py
```

5. The generated reports will be available in the `./output` folder.

## Configuration
The script uses a configuration dictionary (`CONFIG`) to customize its behavior. Key configurations include:

- `input_folder`: Folder for SiteBulb CSV exports.
- `output_folder`: Folder to store generated Markdown reports.
- `data_folder`: Folder containing the mapping CSV file.
- `length`: Report length ('short' or 'long').
- `separate_files`: Create separate files for each section ('y' or 'n').
- `short_file_name`: Name of the short report file if not separating files.
- `include_links`: Include links in the report ('y' or 'n').
- `importance_order`: Order of importance levels.
- `importance_emoji_map`: Emoji mapping for importance levels.
- `section_emoji_map`: Emoji mapping for report sections.
- `src_column`: Source column for the merge.
- `map_column`: Map column for the merge.
- `column_fallbacks`: Fallback mapping for columns.

## Custom Data Mapping
You can use your own custom descriptions and hints by modifying the map.csv file. I would recommend opening this in a spreadsheet editor to work on it.
Any column with a heading containing the word "Custom" can be modified with any data you like. This data will then be used in the markdown file generation.

## Fallback Mapping
The script supports fallback mapping for different columns, allowing you to define fallback behavior for missing or empty values.

## Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

Author Staples1010
