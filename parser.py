import io
import re

input_path  = 'bookmarks.html'
output_path = 'links.txt'
desired_country_code = 'pl'
start_string = r".*Xd.*"

def replace_country(link):
    if not desired_country_code == '':
        country_match = re.search(r"//..\.", link)
        if country_match:
            old_code = link[country_match.start() + 2:country_match.end() - 1]
            return link.replace(old_code,desired_country_code,1)
    return link

input_file  = io.open(input_path , mode="r", encoding="utf-8")
output_file = io.open(output_path, mode="w+", encoding="utf-8")
started = False

sites = {}

for line in input_file:
    if not started:
        match = re.search(start_string, line)
        if match:
            started = True
        else:
            print("SKIPPED : " + line[:len(line) - 1])
    
    if started:
        match = re.search(r"\"http[^\"]*\"", line)
        if not match:
            print("SKIPPED : " + line[:len(line) - 1])
            continue

        link = line[match.start() + 1:match.end() - 1]

        link = replace_country(link)
        print("ADDED   : " + link)
        
        site_match = re.search(r"//[^/]*", link)
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

for site,count in sites.items():
    site = site.replace("www.","",1)
    better_sites[site] = count

sorted_sites = dict(sorted(better_sites.items(),reverse=True , key=lambda item: item[1]))

for site,count in sorted_sites.items():
    print(f"SITE COUNT: {str(count).ljust(4,' ')} URL: {site} ")
