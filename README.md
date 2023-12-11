# SiteBulb CSV Report to Markdown

## Overview
This script generates markdown reports based on input CSV files containing data related to website issues. The generated reports include information about different sections, hints, types of warnings, and their respective details.

The general usecase of this script would be to generate a custom report based an SiteBulb's provided data. You can get an export from SiteBulb containing lists of all the URLs that have issues.

The roport can then be generated, linking items by type of issue, injecting emojis to represent section headings and importance values. and most importantly, offering you the ability to write your own custom Hints, Descriptions and links. This allows you to effectivly hide the origin of the data (SiteBulb), in favour of your own custom written descriptions and explination links.

## Prerequisites
- Python 3.x
- Pandas library

## Usage
1. Place your input CSV files in the `./input` folder.
2. Configure the script using the `CONFIG` dictionary in the script file.
3. Run the script using the following command:

```bash
python reportGenerator.py
```

4. The generated reports will be available in the `./output` folder.

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

## Fallback Mapping
The script supports fallback mapping for different columns, allowing you to define fallback behavior for missing or empty values.

## Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

Author Staples1010