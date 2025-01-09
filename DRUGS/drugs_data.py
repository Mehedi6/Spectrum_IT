import json

try:
    with open("C:\\Users\\arwen\\Desktop\\Newspaper Scraping\\Spectrum_IT\\DRUGS\\Bangla_Tribune\\bdtribune_data.json", 'r', encoding='utf-8') as file:
        existing_data = json.load(file)
except FileNotFoundError:
    existing_data = []

try:
    with open("C:\\Users\\arwen\Desktop\\Newspaper Scraping\\Spectrum_IT\\DRUGS\\BD_Protidin\\bd_protidin_data.json", 'r', encoding='utf-8') as file:
        existing_data_1 = json.load(file)
except:
    existing_data_1 = []

existing_data.extend(existing_data_1)

try:
    with open("C:\\Users\\arwen\\Desktop\\Newspaper Scraping\\Spectrum_IT\\DRUGS\\Daily_Star_Bangla\\daily_star_bangla.json", 'r', encoding='utf-8') as file:
        existing_data_2 = json.load(file)
except FileNotFoundError:
    existing_data_2 = []

existing_data.extend(existing_data_2)

try:
    with open("C:\\Users\\arwen\\Desktop\\Newspaper Scraping\\Spectrum_IT\\DRUGS\\Jugantor\\jugantor_data.json", 'r', encoding='utf-8') as file:
        existing_data_3 = json.load(file)
except FileNotFoundError:
    existing_data_3 = []

existing_data.extend(existing_data_3)

try:
    with open("C:\\Users\\arwen\Desktop\\Newspaper Scraping\\Spectrum_IT\\DRUGS\\Samakal\\samakal_data.json", 'r', encoding='utf-8') as file:
        existing_data_4 = json.load(file)
except:
    existing_data_4 = []

existing_data.extend(existing_data_4)

with open("C:\\Users\\arwen\Desktop\\Newspaper Scraping\\Spectrum_IT\\DRUGS\\drugs_data.json", 'w', encoding='utf-8') as f:
    json.dump(existing_data, f, ensure_ascii=False, indent=4)