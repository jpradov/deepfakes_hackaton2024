from flask import Flask, Response, send_from_directory
import requests
import json
import re
from bs4 import BeautifulSoup


app = Flask(__name__)

# Step 1: Download content from a given URL
def fetch_url_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        return response.text  # Return the HTML content of the page
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

def split_sentences(text):
    # Define common abbreviations to protect
    abbreviations = ["e.g.", "i.e.", "Dr.", "Mr.", "Ms.", "Mrs.", "Jr.", "Sr.", "Prof."]
    
    # Create a unique placeholder for each abbreviation
    placeholders = {abbr: f"__{i}__" for i, abbr in enumerate(abbreviations)}
    
    # Replace abbreviations with placeholders
    for abbr, placeholder in placeholders.items():
        text = text.replace(abbr, placeholder)
    
    # Split the text by period followed by space or end of string
    sentences = re.split(r'\.\s+(?!__\d+__)', text)
    
    # Restore abbreviations
    for abbr, placeholder in placeholders.items():
        sentences = [sentence.replace(placeholder, abbr) for sentence in sentences]
    
    # Remove any leading/trailing spaces and filter out empty strings
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
    
    return sentences


def replace_paragraphs_with_placeholder(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Replace body with paragraphs
    with open("article_content.json", 'r') as json_file:
        data = json.load(json_file)
    
    # Remove any leading/trailing spaces and filter out empty strings
    sentences = split_sentences(data["article_body"])

    for i, p_tag in enumerate(soup.find_all('p', class_="sc-eb7bd5f6-0 fYAfXe")):
        if i < len(sentences):
            p_tag.string = sentences[i]
        else:
            p_tag.string = ""

    # Replace favicon with local icon
    # <link href="/media/sites/cnn/favicon.ico" rel="icon" type="image/x-icon">
    iconlink = soup.find('link', {"rel" : "shortcut icon"})
    if iconlink:
        iconlink.href = "/media/cnn.ico"
    
    # Replace headline with text
    headline = soup.find('h1')
    if headline:
        headline.string = data["title"]

    # Replace title with text
    title = soup.find('title')
    if title:
        title.string = data["title"]

    # Replace image with new iamge
    imgs = soup.find_all("img")
    for img in imgs:
        if img:
            img["srcset"] = "media/conspiracy_image.png"
            img["src"] = "media/conspiracy_image.png"
    
    # Replace legend with new legend
    legends = soup.find_all('figcaption')
    for legend in legends:
        legend.string = data["image_caption"]
    
    # Return the modified HTML
    return str(soup)

# Serve media files from the 'media' folder
@app.route('/media/<path:filename>')
def media_files(filename):
    return send_from_directory('media', filename)

# Step 2: Define a route to serve the content at localhost:8080
@app.route('/')
def serve_content():
    url = 'https://www.bbc.com/news/articles/cj9l9dlgpmno'  # Replace with the URL you want to fetch
    original_content = fetch_url_content(url)
    

    
    modified_content = replace_paragraphs_with_placeholder(original_content)
    return Response(modified_content, mimetype='text/html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
