> [!WARNING]
> This is absolutely not production ready this is only hobbyist project

# Bookmark parser

Simple python parser for html bookmarks exported from a web browser that saves all urls it finds there to a file and can:
- replace a two letter country code that some websites put at the start of their urls so `en` would turn `pl.website.com` to `en.website.com`
- start saving the urls after a specified regex string is encountered

## Configuration

You have configure the script with the variables:
- `input_path` - string with a path to your bookmarks html file
- `output_path` - string with a path where the output urls should be saved
- OPTIONAL `desired_country_code` -  string with a two letter country code that some websites put at the start of their urls so `en` would turn `pl.website.com` to `en.website.com`
- OPTIONAL `start_string` - regex string that starts the process so any urls before it will be omitted

## Quick Start

```console
$ python3 preparse.py
```