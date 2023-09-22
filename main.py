import os
import re
import yaml
import csv

def extract_metadata_fields(file_content):
    # Load the metadata section as YAML
    metadata = yaml.safe_load(file_content)

    # Extract the desired fields
    title = metadata.get("title", None)
    slug = "https://loft.sh/blog/" + metadata.get("slug", None)
    lastmod = metadata.get("lastmod", None)
    authors = ', '.join(metadata.get("authors", []))

    return title, slug, lastmod, authors

def iterate_files_and_extract_info(directory):
    post_info_list = []

    for filename in os.listdir(directory):
        if filename.endswith(".md"):
            file_path = os.path.join(directory, filename)
            with open(file_path, "r") as file:
                file_content = file.read()

            # Check if the file has the specified metadata structure
            if "---" in file_content:
                metadata_section = file_content.split("---")[1]
                title, slug, lastmod, authors = extract_metadata_fields(metadata_section)

                if title and slug:
                    post_info_list.append({
                        "title": title,
                        "slug": slug,
                        "lastmod": lastmod,
                        "authors": authors
                    })

    return post_info_list

# Specify the directory containing the files
directory_path = "/workspace/markdown-posts-data"

# Iterate through the files and extract metadata
post_info_list = iterate_files_and_extract_info(directory_path)

csv_file_path = "/workspace/markdown-posts-data/data.csv"

# Write the extracted information to a CSV file
with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Title', 'Slug', 'Last Modified', 'Authors'])
    for post_info in post_info_list:
        writer.writerow([post_info['title'], post_info['slug'], post_info['lastmod'], post_info['authors']])

print("CSV file written successfully.")
