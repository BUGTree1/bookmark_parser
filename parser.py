from url_parser import get_url
from pathlib import Path
from glob import glob
import io
import re

input_path  = 'bookmarks.html'
output_path = 'links.txt'
desired_country_code = 'pl'
excluded_country_codes = ['su','st','cr','ai','me','co','io','nz']
start_string = r".*Xd.*"
end_string = r""
replace_domains = {"xcancel":"x"}
sites_supported_files = ['downloaders/*']

DEBUG = True

def replace_string_range(string, replacement, start, end):
    return string[:start] + replacement + string[end:]

def replace_country_prefix(link):
    country_match = re.search(r"//..\.", link)
    if country_match:
        #old_code = link[country_match.start() + 2:country_match.end() - 1]
        return replace_string_range(link,desired_country_code,country_match.start() + 2,country_match.end() - 1)
    return link

def replace_country_suffix(link):
    country_match = re.search(r"\.([^./]*)(?=/)", link)
    if country_match:
        old_code = link[country_match.start() + 1:country_match.end()]
        if len(old_code) == 2 and not (old_code in excluded_country_codes):
            return replace_string_range(link,desired_country_code,country_match.start() + 1,country_match.end())
    return link

def replace_country(link):
    if desired_country_code == '':
        return link
    else:
        return replace_country_suffix(replace_country_prefix(link))
    
def replace_domain(link):
    if replace_domains == {}:
        return link
    else:
        for domain,replacement in replace_domains.items():
            if get_url(link).domain == domain:
                dom_match = re.search(domain,link)
                if not dom_match:
                    exit()
                return replace_string_range(link,replacement,dom_match.start(),dom_match.end())
                
        return link

input_file  = io.open(input_path , mode="r", encoding="utf-8")
output_file = io.open(output_path, mode="w+", encoding="utf-8")
started = False

if start_string == '':
    started = True

sites = {}
sites_supported = {}
links_count = 0

if sites_supported_files != [] and sites_supported_files != None:
    for glob_supporting in sites_supported_files:
        for downloader in glob(glob_supporting):
            downloader_stream = io.open(downloader,mode="r", encoding="utf-8")
            for line in downloader_stream:
                line_parsed = line[:len(line) - 1]
                sites_supported[line_parsed] = downloader
            downloader_stream.close()

for line in input_file:
    if not started:
        match = re.search(start_string, line)
        if match:
            started = True
        else:
            if DEBUG:
                print("SKIPPED : " + line[:len(line) - 1])
    
    if started:
        if not (end_string == r"") and re.search(end_string, line):
            break

        match = re.search(r"\"http[^\"]*\"", line)
        if not match:
            if DEBUG:
                print("SKIPPED : " + line[:len(line) - 1])
            continue

        link = line[match.start() + 1:match.end() - 1]

        link = replace_country(link)
        link = replace_domain(link)
        
        if DEBUG:
            print("ADDED   : " + link)
        links_count += 1
        
        site_match = re.search(r"//[^/]*", link)
        if not site_match:
            print("ERROR: Not Valid URL")
            exit(1)
        site = link[site_match.start() + 2:site_match.end()]

        if site in sites:
            sites[site] = sites[site] + 1
        else:
            sites[site] = 1

        output_file.write(link + '\n')

input_file.close()
output_file.close()

print()

better_sites = {}
longest_url = 0
longest_count = 0

for site,count in sites.items():
    site = site.replace("www.","",1)
    better_sites[site] = count
    if len(site) > longest_url:
        longest_url = len(site)
    if len(str(count)) > longest_count:
        longest_count = len(str(count))

sorted_sites = dict(sorted(better_sites.items(),reverse=True , key=lambda item: item[1]))
sites_count = 0
sites_no_support = []

for site,count in sorted_sites.items():
    site_name = get_url(site).domain
    
    supported_downloader = None
    for sup_site,downloader in sites_supported.items():
        if re.search(site_name,sup_site,re.IGNORECASE):
            supported_downloader = downloader
    
    if not supported_downloader:
        sites_no_support.append(site)
    
    print(f"SITE COUNT: {str(count).ljust(longest_count,' ')} URL: {site.ljust(longest_url,' ')} SUPPORTED BY: {supported_downloader}")
    sites_count += 1

if sites_no_support != []:
    print(f"DIDNT FIND SUPPORT FOR {len(sites_no_support)} DOMAINS")

print(f"FOUND {sites_count} DOMAINS IN {links_count} URLS")
