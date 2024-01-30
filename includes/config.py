# Configuration
CONFIG = {
    'input_folder': './input',
    'output_folder': './output',
    'data_folder': './data',
    'length': 'long', # 'short' or 'long' to control how much data is presented.
    'extra_columns': [], # Include extra columns e.g. ['Column Name 1', 'Column Name 2', 'Column Name 3']
    'separate_files': 'y', # 'y' or 'n' to create separate files for each section.
    'section_title': 'y', # 'y' or 'n' to display a title for the section.
    'short_file_name': 'Report.md',
    'include_links': 'y', # 'y' or 'n'
    'importance_map': {
        '4 - Critical': {
            'name': 'Critical',
            'value': 5,
            'emoji': '💣'
        },
        '3 - High': {
            'name': 'High',
            'value': 4,
            'emoji': '🔴'
        },
        '2 - Medium': {
            'name': 'Medium',
            'value': 3,
            'emoji': '🟠'
        },
        '1 - Low': {
            'name': 'Low',
            'value': 2,
            'emoji': '🟡'
        },
        '0 - None': {
            'name': 'No Issue',
            'value': 1,
            'emoji': '🔵'
        },
        'Unknown': {
            'name': 'Unknown',
            'value': 0,
            'emoji': '🟣'
        }
    },
    'section_map': {
        'Accessibility': {
            'name': 'Accessibility',
            'emoji': '♿️'
        },
        'AMP': {
            'name': 'AMP',
            'emoji': '⚡'
        },
        'Duplicate Content': {
            'name': 'Duplicate Content',
            'emoji': '🔄'
        },
        'Indexability': {
            'name': 'Indexability',
            'emoji': '🔍'
        },
        'Internal': {
            'name': 'Internal',
            'emoji': '🏠'
        },
        'International': {
            'name': 'International',
            'emoji': '🌐'
        },
        'Links': {
            'name': 'Links',
            'emoji': '🔗'
        },
        'Mobile Friendly': {
            'name': 'Mobile Friendly',
            'emoji': '📱'
        },
        'On Page': {
            'name': 'On Page',
            'emoji': '📄'
        },
        'Performance': {
            'name': 'Performance',
            'emoji': '⚙️'
        },
        'Redirects': {
            'name': 'Redirects',
            'emoji': '➡️'
        },
        'Rendered': {
            'name': 'Rendered',
            'emoji': '🖼️'
        },
        'Search Traffic': {
            'name': 'Search Traffic',
            'emoji': '🔍🚦'
        },
        'Security': {
            'name': 'Security',
            'emoji': '🔒'
        },
        'XML Sitemaps': {
            'name': 'XML Sitemaps',
            'emoji': '🗺️'
        }
    },
    #'match_columns': {
    #    'Learn More',
    #    'Hint'
    #}
}
