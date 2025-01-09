import os
import time
import re
import json
from datetime import datetime, timedelta
from transformers import pipeline

# Initialize sentiment analysis pipeline
sentiment_analyzer = pipeline("sentiment-analysis")

# Function to safely parse the keywords
def safe_parse_keywords(keywords_str):
    keywords = re.findall(r"[\u0980-\u09FFa-zA-Z0-9\-]+", keywords_str)
    return keywords

# Function to chunk text and analyze sentiment on each chunk
def analyze_text_in_chunks(text, chunk_size=512):
    # Split the text into chunks based on the character limit
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    
    # Analyze sentiment for each chunk
    sentiments = []
    for chunk in chunks:
        sentiment_result = sentiment_analyzer(chunk)[0]
        sentiments.append(sentiment_result['label'])
    
    # Combine the chunk results (you can adjust this logic based on how you want to combine sentiments)
    combined_sentiment = 'POSITIVE' if 'POSITIVE' in sentiments else 'NEGATIVE' if 'NEGATIVE' in sentiments else 'NEUTRAL'
    
    return combined_sentiment

# Function to generate news score, international flag, and suggested keywords
def generate_news_score(news_description):
    # Prepare the text for sentiment analysis
    content = f"Title: {news_description['title']} Description: {news_description['description']} Meta_description: {news_description['meta_description']} Keywords: {news_description['keywords']} News_type: {news_description['news_type']} Published_date: {news_description['published_date']}"
    
    # Perform sentiment analysis using the chunked approach
    sentiment = analyze_text_in_chunks(content)
    
    # Set sentiment map
    sentiment_map = {'POSITIVE': 1, 'NEGATIVE': -1, 'NEUTRAL': 0}
    sentiment_score = sentiment_map.get(sentiment, 0)

    # Suggest keywords based on some condition (example check for TCB keywords)
    suggested_keywords = []
    relevant_keywords = ["অনিয়ম", "কেনাকাটা", "পণ্য বিক্রয়", "কার্ড বিতরণ", "টিসিবি স্মার্ট ফ্যামিলি কার্ড", "টিসিবি ভবন"]
    for keyword in relevant_keywords:
        if keyword not in news_description['keywords']:
            suggested_keywords.append(keyword)

    # News score: Basic implementation (modify as per your requirement)
    news_score = sentiment_score * 50  # You can adjust the scale if needed

    # Determine if the news is international
    international = "international" in " ".join(news_description['keywords']).lower()

    return [news_score, international, sentiment, suggested_keywords]

# Function to update the first n non-updated news items
def update_news_data(news_data, n):
    counter = 0
    for news in news_data:
        # Stop after updating n news items
        if counter >= n:
            break

        # Check if the news item has been updated by looking for a non-zero score
        if 'news_score' in news and news['news_score'] != 0:
            continue

        try:
            news_score, international, sentiment, generated_keywords = generate_news_score({
                "title": news['title'],
                "meta_description": news['meta_description'],
                "description": news['content'],
                "keywords": news['keywords'],
                "news_type": news['news_type'],
                "published_date": news['published_date']
            })
        except Exception as e:
            print(f"Error processing news: {e}")
            continue

        print(f"News score: {news_score}, Sentiment: {sentiment}, International: {international}, Title: {news['title']}")

        # Merge original and generated keywords, avoiding duplicates
        all_keywords = list(set(news.get('keywords', []) + generated_keywords))

        # Update the news item with new properties
        news['keywords'] = all_keywords
        news['news_score'] = news_score
        news['international'] = international
        news['sentiment'] = sentiment
        news['views'] = 0
        news['rating'] = 0
        news['engagement'] = 0
        news.setdefault('updated_date', None)
        
        # Determine if news is older than 4 days
        published_date = datetime.fromisoformat(news["published_date"])
        news['old'] = (datetime.now() - published_date) > timedelta(days=4)
        
        counter += 1
        # Save the updated data back to JSON file
        with open('C:\\Users\\arwen\\Desktop\\TCB\\JagoNews\\jago_tcb_data.json', 'w', encoding='utf-8') as file:
            json.dump(news_data, file, ensure_ascii=False, indent=4)
        print(f"Processed {counter} news items.")
        time.sleep(1)

    print("News data updated successfully!")

# Load JSON file and update news items
n = int(input("Enter the number of news items to update: "))

with open('C:\\Users\\arwen\\Desktop\\TCB\\JagoNews\\jago_tcb_data.json', 'r', encoding='utf-8') as file:
    news_data = json.load(file)

update_news_data(news_data, n)
