# SiteBulb CSV Report to Markdown

## Overview
This script generates markdown reports based on input CSV files containing data related to website issues. The generated reports include information about different sections, hints, types of warnings, and their respective details.

The general use case of this script would be to generate a custom report based on SiteBulb's provided data. You can get an export from SiteBulb containing lists of all the URLs that have issues. The 'All Hints - Summary' file that can be exported to Google Drive.

The report can then be generated, linking items by type of issue, and injecting emojis to represent section headings and importance values. And most importantly, offering you the ability to write your own custom Hints, Descriptions links and apply custom data with the use of custom column mapping. This allows you to effectively hide the origin of the data (SiteBulb), in favour of your own custom-written 'descriptions' and 'explanation' links.

## Prerequisites
- Python 3.x
- Pandas library

## Usage
1. Generate your reports in SiteBulb. This script uses the 'All Hints' report which should contain hints about all the issues your site faces. This report is generated in Google Drive and the final markdown file(s) will use the Google Drive spreadsheet links in their copy.
2. Place your input CSV files in the `./input` folder.
3. Configure the script using the `CONFIG` dictionary in `/includes/config.py`.
4. Run the script using the following command:
    ```bash
    python reportGenerator.py
    ```
    
    Or explicitly use Python 3:

    ```bash
    python reportGenerator.py
    ```
5. The generated reports will be available in the `./output` folder.

---

## Configuration
The script uses a configuration dictionary (`CONFIG`) to customize its behavior. Key configurations include:

- `input_folder`: Folder for SiteBulb CSV exports.
- `output_folder`: Folder to store generated Markdown reports.
- `data_folder`: Folder containing the mapping CSV file.
- `length`: Report length (`short` or `long`).
- `extra_columns`: Include extra columns e.g. `['Column Name 1', 'Column Name 2', 'Column Name 3']`.
- `separate_files`: Create separate files for each section (`y` or `n`).
- `section_title`: `y` or `n` to display a title for the section.
- `short_file_name`: Name of the short report file if not separating files.
- `include_links`: Include links in the report (`y` or `n`).
- `importance_map`: A dictionary of importance values found in SiteBulb containing mapped data for `name`, `value` and `emoji`.
- `section_map`: A dictionary of section name values found in SiteBulb containing mapped data for `name` and `emoji`.
- `match_columns`: Coming Soon.

## Custom Data Mapping
You can use your own custom descriptions and hints by modifying the map.csv file. I would recommend opening this in a spreadsheet editor to work on it.
You can modify any column, but Hint must remain untouched as this is the key used for the lookup. This data will then be used in the markdown file generation.

## Fallbacks
The script will fallback to the data found in Sitebulb if no mapping data is found.

## Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

Author Staples1010

<a href="https://www.buymeacoffee.com/Invulnerable.Orc"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a coffee&emoji=&slug=Invulnerable.Orc&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" /></a>
