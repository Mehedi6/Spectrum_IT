import os
import time
import re
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv
import google.generativeai as genai

# Load the API key from the .env file
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Function to safely parse the keywords
def safe_parse_keywords(keywords_str):
    keywords = re.findall(r"[\u0980-\u09FFa-zA-Z0-9\-]+", keywords_str)
    return keywords

model = genai.GenerativeModel(
    model_name= 'gemini-1.5-flash'
    
    )
# Function to generate news score, international flag, and suggested keywords
def generate_news_score(news_description):
    prompt = f"""
        Suppose you are the most senior {news_description['news_type']} news analyst in a top-rated news publication company. Your task is:
        
        1. To provide a score to the news based on its properties out of 100. Score the most critical and important news, particularly those with significant relevance to national policy, societal impact, or crises, with higher scores.
        
        2. To determine whether the news has a **national** or **international** perspective in terms of Bangladesh. If the news is related to Bangladesh, it should be classified as **national**.

        3. To analyze the **tone of the news** carefully, considering all perspectives, and determine whether it is **positive**, **negative**, or **neutral** based on its societal impact:
            - **Positive**:  
              The news highlights societal benefits, successful interventions, or major achievements, such as dismantling a major criminal network, unprecedented enforcement success, or impactful community efforts. 

            - **Negative**:  
              The news emphasizes harm, danger, or societal challenges, such as ongoing criminal activities, trafficking, or persistent societal issues. Even if there are positive developments (e.g., arrests or confiscation), the tone may lean negative if the broader problem remains prominent.

            - **Neutral**:  
              The news provides factual, balanced reporting with no strong positive or negative emphasis. It is descriptive and avoids projecting either harm or benefits to society.

        **Contextual Guidance**:  
        - If the news includes both positive and negative elements, assess the sentiment based on the dominant tone in the content. Avoid bias and focus on the most critical aspect of the societal impact.
        - Evaluate **neutral** sentiment equally and avoid presuming positivity or negativity unless clearly supported by the content.

        You will be provided with:
        1. Title: {news_description['title']}
        2. Description: {news_description['description']}
        3. Meta_description: {news_description['meta_description']}
        4. Keywords: {news_description['keywords']}
        5. News_type: {news_description['news_type']}
        6. Published_date: {news_description['published_date']}
        7. Current_time: {datetime.today().strftime('%Y-%m-%d %H:%M:%S')}

        Analyze them carefully. Check whether the following keywords - "অনিয়ম, নিষিদ্ধ, পাচার, আদালত, রায়, পুলিশ, মামলা, গ্রেপ্তার" are relevant to the news. 
        
        If these keywords or any other significant keywords according to you, that are applicable but not included in {news_description['keywords']} , suggest additional keywords; otherwise, respond with **Keywords: <[]>**. Be careful about the language while adding additional keywords. As all the news contents are for bangla language, you are recommended to use bangla for implementing keywords.

        # Please respond with the following format only (without extra explanations or suggestions):
        News_Score: <Score>
        International: <True or False>
        Sentiment: <Positive or Neutral or Negative>
        Keywords: <[Keyword1, Keyword2, ...]> 
        if no keyword suggestion then 
        Keywords: <[]> 
        """



    # Use model.generate_text() for generating content, updated to handle response properly
    response = model.generate_content(prompt,
                                      generation_config = genai.GenerationConfig(
                                        max_output_tokens=1024,
                                        temperature=0.1,
                                    ) )
    text = response.candidates[0].content.parts[0]
    print(text.text,"======")

    generated_text = text.text  # Access the result properly

    match = re.search(r'News_Score:\s*(\d+)', generated_text)
    
    international_match = re.search(r'International:\s*(True|False)', generated_text)
    international_bool = True if international_match and international_match.group(1) == 'True' else False

    sentiment_match = re.search(r'Sentiment:\s*(Positive|Neutral|Negative)', generated_text)
    sentiment = sentiment_match.group(1) if sentiment_match else 'Neutral'

    keywords_match = re.search(r'Keywords:\s*(\[.*?\])', generated_text)
    keywords_str = keywords_match.group(1) if keywords_match else '[]'
    keywords = safe_parse_keywords(keywords_str)

    return [int(match.group(1)) if match else 0, international_bool, sentiment, keywords]

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

        original_keywords = list(set(news.get('keywords', [])))

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
            print(f"An error occurred: {e}")
            continue

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
        print(f"Processed {counter} news items.")
        time.sleep(1)

    # Save the updated data back to JSON file
    with open('all_bdtribune_data.json', 'w', encoding='utf-8') as file:
        json.dump(news_data, file, ensure_ascii=False, indent=4)
    print("News data updated successfully!")

# Load JSON file and update news items
n = int(input("Enter the number of news items to update: "))

with open('all_bdtribune_data.json', 'r', encoding='utf-8') as file:
    news_data = json.load(file)

update_news_data(news_data, n)