from flask import Flask
import requests
import nltk
from bs4 import BeautifulSoup
import requests
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from heapq import nlargest



app = Flask(__name__)

api_key = "1674766aa2074ae9b134228fe71f9b93"

@app.route("/")

def getArticles():
    main_url = "https://newsapi.org/v2/everything?domains=techcrunch.com,thenextweb.com/&sortBy=top&apiKey=1674766aa2074ae9b134228fe71f9b93"
    open_page = requests.get(main_url).json()
    articles = open_page["articles"]

    results = []

    html_response = "<h1>Article Summarizer</h1><ul>"
    for i, article in enumerate(articles):
        if i == 10:
            break

        article_title = article["title"]
        article_url = article["url"]
        article_content = getHTMLdocument(article_url)
        summary = generate_summary(article_content)

        html_response += f"<li><a href='{article_url}'>{article_title}</a></li>"
        html_response += f"<p>Summary: {summary}</p>"

    html_response += "</ul>"
    
    return html_response

def getHTMLdocument(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    text_content = soup.get_text()
    return text_content

def tokenize_content(content):
    words = word_tokenize(content)
    sentences = sent_tokenize(content)
    return words, sentences

def generate_summary(content):
    sentences = sent_tokenize(content)
    
    words = word_tokenize(content)
    
    # Remove stopwords
    stop_words = set(stopwords.words("english"))
    words = [word for word in words if word.lower() not in stop_words]
    
    # Calculate word frequency
    word_freq = {}
    for word in words:
        if word in word_freq:
            word_freq[word] += 1
        else:
            word_freq[word] = 1
    
    # Calculate sentence scores
    sent_scores = {}
    for sentence in sentences:
        for word in word_tokenize(sentence.lower()):
            if word in word_freq:
                if len(sentence.split(" ")) < 30:
                    if sentence not in sent_scores:
                        sent_scores[sentence] = word_freq[word]
                    else:
                        sent_scores[sentence] += word_freq[word]
    
    # Get top sentences
    summary_sentences = nlargest(5, sent_scores, key=sent_scores.get)
    
    # Generate summary
    summary = " ".join(summary_sentences)
    return summary

if __name__ == "__main__":
    app.run(debug=True)