import os
import csv
import json
from datetime import datetime

def process_json_to_csv(json_file_path, archive_dir):
    # Read the JSON file
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Get the input file name and current date
    input_file_name = os.path.splitext(os.path.basename(json_file_path))[0]
    current_date = datetime.now().strftime("%Y-%m-%d")
    csv_filename = f"{input_file_name}_{current_date}.csv"
    csv_file_path = os.path.join(archive_dir, csv_filename)

    # Check if CSV file already exists
    file_exists = os.path.exists(csv_file_path)

    # Prepare the CSV fieldnames
    fieldnames = [
        "author", "content", "engagement", "image_urls", "international", "keywords",
        "last_scraped", "media_type", "meta_description", "news_score", "news_subcategory",
        "news_type", "old", "published_date", "rating", "sentiment", "source", "title",
        "updated_date", "url", "views"
    ]

    # Create CSV if not exists, or append if exists
    if not file_exists:
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            # Write data to CSV
            for item in data:
                writer.writerow(item)
    else:
        # If file exists, read the existing URLs from CSV
        existing_urls = set()
        with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                existing_urls.add(row['url'])

        # Append only unique data
        with open(csv_file_path, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            # Write only the unique entries
            for item in data:
                if item['url'] not in existing_urls:
                    writer.writerow(item)
                    existing_urls.add(item['url'])

    print(f"Data has been processed and stored in: {csv_file_path}")


# Example usage
json_file_path = '/home/Ahmed001/airflow/scraper/validated/bss_news_data.json'
archive_dir = '/home/Ahmed001/airflow/scraper/archive/bss_news'
process_json_to_csv(json_file_path, archive_dir)