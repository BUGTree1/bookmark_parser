> [!WARNING]
> This is absolutely not production ready this is only hobbyist project

# Bookmark parser

Simple python parser for html bookmarks exported from a web browser that:
- Saves all urls it finds there to a file
- Prints what domains it found and how many
- Can replace a two letter country code that some websites put in their urls so `pl` would turn `uk.website.com` to `pl.website.com` or `website.uk` to `pl.website.pl`
- Can start saving the urls after a specified regex string is encountered

## Configuration

You have configure the script with the variables:
- `input_path`                    : string with a path to your bookmarks html file
- `output_path`                   : string with a path where the output urls should be saved
- OPTIONAL `desired_country_code` : string with the desired two letter country code
- OPTIONAL `start_string`         : regex string that starts the process so any urls before it will be omitted
- OPTIONAL `end_string`           : regex string that end the process so any urls after it will be omitted

## Quick Start

```console
$ python3 preparse.py
```
