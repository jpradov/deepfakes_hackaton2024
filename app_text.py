from flask import Flask, Response
import requests
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


def replace_paragraphs_with_placeholder(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    main_content_div = soup.find('div', class_="article__content")

    if main_content_div:
        # Step 4: Find all <p> tags with the specific class within the main content div
        for p_tag in main_content_div.find_all('p', class_="paragraph inline-placeholder vossi-paragraph-primary-core-light"):
            p_tag.string = "Placeholder name"  # Replace content with the placeholder text
    headline = soup.find('h1', class_="headline__text inline-placeholder vossi-headline-primary-core-light", id="maincontent")
    if headline:
        headline.string = "New Headline Text"  # Replace the headline text
  
    # Return the modified HTML
    return str(soup)

# Step 2: Define a route to serve the content at localhost:8080
@app.route('/')
def serve_content():
    url = 'https://edition.cnn.com/2024/09/13/europe/russia-expels-diplomats-intl-hnk/index.html'  # Replace with the URL you want to fetch
    original_content = fetch_url_content(url)
    

    
    modified_content = replace_paragraphs_with_placeholder(original_content)
    print(modified_content)
    return Response(modified_content, mimetype='text/html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
