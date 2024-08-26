import json
import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_relevance(text1, text2):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([text1, text2])
    cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return cosine_sim[0][0]

def get_title_from_url(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.title.string if soup.title else url
    except:
        return url

def get_content_from_url(url):
    try:
        response = requests.get(url)
        return response.text
    except:
        return ""

# Read existing JSON files
with open('links.json', 'r') as f:
    links_data = json.load(f)['links']

with open('questions.json', 'r') as f:
    questions_data = json.load(f)['questions']

final_output = {
    "questions": questions_data,
    "urls": []
}

for url in links_data:
    content = get_content_from_url(url)
    
    relevant_links = []
    for other_url in links_data:
        if other_url != url:
            other_content = get_content_from_url(other_url)
            relevance_score = calculate_relevance(content, other_content)
            relevant_links.append((other_url, relevance_score))
    
    # Sort by relevance and take top 5
    relevant_links.sort(key=lambda x: x[1], reverse=True)
    top_5_links = relevant_links[:5]
    
    formatted_links = [
        {
            "url": link[0],
            "title": get_title_from_url(link[0])
        }
        for link in top_5_links
    ]
    
    webpage_data = {
        "url": url,
        "relevant_links": formatted_links
    }
    
    final_output["urls"].append(webpage_data)

# Save the final output
with open('final_output.json', 'w') as f:
    json.dump(final_output, f, indent=4)

print("Final output has been saved to final_output.json")