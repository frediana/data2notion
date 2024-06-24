# data2notion: export your data to Notion

[![PyPI - Version](https://img.shields.io/pypi/v/data2notion)](https://pypi.org/project/data2notion/)
[![License](https://img.shields.io/pypi/l/data2notion)](https://raw.githubusercontent.com/pierresouchay/data2notion/main/LICENSE)

This tool is intended for exporting various data from 3rd party systems
into Notion. If you tool can export some records, then you can make this data available to Notion!

## Goals

When working as a CTO, I had the need to expose data from various systems (Applications, AWS, SIEM, Active Directory, users, groups...)
into Notion to generate automatic reports and select what I wanted to expose, so it made all systems transparent and open.
This was extremelly precious to automatically generate reports for audits.

One of the advantages of the tool is that:

 - it creates entries in Notion database if entries do not exists
 - it modifies the various fields of the Notion database if they have been modified
 - it cleanups the old records when they don't exist anymore

So, if you run this tool everyday, you have a Notion database in sync with the data from all your third party systems.
And you can start commenting, taking decisions and documenting those entries within Notion: it gives you a centralized
way to discuss topics about all of your IT, provides comments, reminders (eg: reming me about renewing this certificate
in 2 years, check if the fix has been performed in 2 months...), and cleanup dead stuff automatically.

Initially, the tool was only dealing with CSV, but data2notion also deals with various formats and APIs, so you can
integrate faster and better!

# Features

data2notion supports plugins, so you can either work with JSON/CSV export or implement your own retrieval of data, for instance,
from a 3rd party API.

## Basic Usage

```bash
data2notion write-to-notion <notion_database_id> <plugin> --help
```

Will list the arguments that are specific to a plugin.

### CSV plugin

Export CSV files arrays in Notion.

```bash
data2notion write-to-notion <notion_database_id> csv --help
usage: data2notion write-to-notion notion_database_id csv [-h] [--csv-dialect {excel,excel-tab,unix,excel_with_semi-colon}] csv_file

Write to Notion DB from a CSV file

positional arguments:
  csv_file              CSV file to inject in Notion, if '-' is set, read from stdin

options:
  -h, --help            show this help message and exit
  --csv-dialect {excel,excel-tab,unix,excel_with_semi-colon}
                        CSV Dialect, excel by default
```

### JSON Plugin

Export some JSON arrays in Notion.

```bash
usage: data2notion write-to-notion notion_database_id json [-h] [--json-path PATH_IN_JSON] json_file

Write to Notion DB from a JSON file containing an array

positional arguments:
  json_file             JSON file to inject in Notion, if '-' is set, read from stdin

options:
  -h, --help            show this help message and exit
  --json-path PATH_IN_JSON
                        JSON path separated by dots to look for the array, example: calendar.appointments
```

### Prometheus Plugin

Export metrics from prometheus (lastest values only) in Notion database.

```bash
usage: main.py write-to-notion notion_database_id prometheus [-h] [--prometheus-url PROMETHEUS_URL]
                                                             [--column-name-mapping COLUMN_NAME_MAPPING COLUMN_NAME_MAPPING]
                                                             [--row-id-expression ROW_ID_EXPRESSION] [--remove-column REMOVE_COLUMN]
                                                             query

Write Prometheus metrics to Notion

positional arguments:
  query                 PromQL Prometheus query to perfom, aggregation supported

options:
  -h, --help            show this help message and exit
  --prometheus-url PROMETHEUS_URL
                        The URL of Prometheus instance to query, default to $PROMETHEUS_URL or http://localhost:9090
  --column-name-mapping COLUMN_NAME_MAPPING COLUMN_NAME_MAPPING
                        map a column into a specific name (timestamp, value + labels) into another name: --column-name-mapping value MyValueColumnInNotion (can
                        be repeated). Title column is mapped automatically
  --row-id-expression ROW_ID_EXPRESSION
                        First column value (default=__default__'): default will concatenate metric name and labels You can use python expression using labels,
                        example: --row-id-expression 'f"my_metrics{labels_str}"'labels_str:= label concatened the prometheus way, but all label can be used for
                        evalutation.By default, it will use `__name__{labels_str}` if __name__ exists, otherwise, __name__ will be replace by a hash of the
                        query (if you perform aggregation).
  --remove-column REMOVE_COLUMN
                        Remove a column, can be specified multiple times
```


## Creating you own plugins

Adding plugin can be done using environment variable `$DATA2NOTION_ADDITIONAL_PLUGINS` which support the
following syntax `python_module.python_file:PluginClass`, thus to enable a new imaginary Bugzilla plugin, you might for instance
export the variable:

```bash
export DATA2NOTION_ADDITIONAL_PLUGINS="bugzilla_api.bugzilla_plugin:BugzillPlugin"
```

Then, the plugin should be visible in:
```bash
data2notion plugins
```

and you might use it as any other plugin.

