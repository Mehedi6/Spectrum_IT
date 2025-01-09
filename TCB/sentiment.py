import os
import time
import re
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from groq import Groq

# Load the API key from the .env file for Groq API
load_dotenv()
client = Groq(api_key=os.getenv('GROQ_API_KEY'))

# Function to safely parse the keywords
def safe_parse_keywords(keywords_str):
    keywords = re.findall(r"[\u0980-\u09FFa-zA-Z0-9\-]+", keywords_str)
    return keywords

# Function to generate news score, international flag, and suggested keywords
def generate_news_score(client, news_description):
    prompt = f"""
    Suppose you are the most senior {news_description['news_type']} news analyst in a top-rated news publication company.
    Your task is to provide a score to a news based on its properties out of 100. You have to score the most critical and important news higher scores. 
    Also, you have to determine whether the news has national or international perspective in terms of Bangladesh.
    
    You will be provided with:
    1. Title: {news_description['title']}
    2. Description: {news_description['description']}
    3. Meta_description: {news_description['meta_description']}
    4. Keywords: {news_description['keywords']}
    5. News_type: {news_description['news_type']}
    6. Published_date: {news_description['published_date']}
    7. Current_time: {datetime.today().strftime('%Y-%m-%d %H:%M:%S')}

    Analyze them carefully. Think whether the keywords - "অনিয়ম, কেনাকাটা, পণ্য বিক্রয়, কার্ড বিতরণ, টিসিবি স্মার্ট ফ্যামিলি কার্ড, টিসিবি ভবন" are applicable to the news. 
    If they are applicable but not in {news_description['keywords']}, then suggest the keywords otherwise Keywords: <[]>.
    
    # Please respond with the following format and do not generate any extra token or explanation or suggestion:
    News_Score: <Score>
    International: <True or False>
    Sentiment: <Positive or Neutral or Negative>
    Keywords: <[Keyword1, Keyword2, ..]> 
    if no keyword suggestion then 
    Keywords: <[]> 
    """

    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.1-70b-versatile",
    )

    response = chat_completion.choices[0].message.content
    match = re.search(r'News_Score:\s*(\d+)', response)
    international_match = re.search(r'International:\s*(True|False)', response)
    international_bool = True if international_match and international_match.group(1) == 'True' else False

    sentiment_match = re.search(r'Sentiment:\s*(Positive|Neutral|Negative)', response)
    sentiment = sentiment_match.group(1) if sentiment_match else 'Neutral'

    keywords_match = re.search(r'Keywords:\s*(\[.*?\])', response)
    keywords_str = keywords_match.group(1) if keywords_match else '[]'
    keywords = safe_parse_keywords(keywords_str)
    
    return [int(match.group(1)) if match else 0, international_bool, sentiment, keywords]

# Function to update the first n non-updated news items
def update_news_data(news_data, n):
    counter = 0
    api_keys = [
        "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",
        "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",
        "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",
        "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",
        "sk_r3X6UZC6BAQfPeST6KOIWGdyb3FYzObJKveHmyUiteVHyIuT79O5",
        "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",
        "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",
        "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",
        "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",
        "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",
       
    ]
    
    for news in news_data:
        # Stop after updating n news items
        if counter >= n:
            break

        # Check if the news item has been updated by looking for a non-zero score
        if 'news_score' in news and news['news_score'] != 0:
            continue

        original_keywords = list(set(news.get('keywords', [])))
        
        try:
            news_score, international, sentiment, generated_keywords = generate_news_score(client, {
                "title": news['title'],
                "meta_description": news['meta_description'],
                "description": news['content'],
                "keywords": news['keywords'],
                "news_type": news['news_type'],
                "published_date": news['published_date']
            })
        except:
            print("Switching API key...")
            
            client = Groq(api_key=api_keys.pop(0))
            continue

            # news_score, international, sentiment, generated_keywords = generate_news_score(client, {
            #     "title": news['title'],
            #     "meta_description": news['meta_description'],
            #     "description": news['content'],
            #     "keywords": news['keywords'],
            #     "news_type": news['news_type'],
            #     "published_date": news['published_date']
            # })
            
        print(news_score)
        # Merge original and generated keywords, avoiding duplicates
        all_keywords = list(set(original_keywords + generated_keywords))
        
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
        with open('BangladeshProtidin\news_tcb_data.json', 'w', encoding='utf-8') as file:
            json.dump(news_data, file, ensure_ascii=False, indent=4)
        print(f"Processed {counter} news items.")
        time.sleep(1)

    
    print("News data updated successfully!")

# Load JSON file and update news items
n = int(input("Enter the number of news items to update: "))

with open('BangladeshProtidin\news_tcb_data.json', 'r', encoding='utf-8') as file:
    news_data = json.load(file)

update_news_data(news_data, n)