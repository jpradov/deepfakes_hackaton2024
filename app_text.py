from flask import Flask, Response, send_from_directory
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

    # Replace favicon with local icon
    # <link href="/media/sites/cnn/favicon.ico" rel="icon" type="image/x-icon">
    iconlink = soup.find('link', {"rel" : "shortcut icon"})
    if iconlink:
        iconlink.href = "/media/cnn.ico"
    
    # Replace headline with text
    headline = soup.find('h1')
    if headline:
        with open('title.txt') as f:
            headline.string = f.read()

    # Replace title with text
    title = soup.find('title')
    if title:
        with open('title.txt') as f:
            title.string = f.read() + " | BBC"

    # Replace image with new iamge
    imgs = soup.find_all("img")
    for img in imgs:
        if img:
            img["srcset"] = "media/hackathon_images_base/mr_bean.jpg"
            img["src"] = "media/hackathon_images_base/mr_bean.jpg"

    # Replace legend with new legend
    legend = [tag for tag in soup.find_all('span', class_="inline-placeholder") if tag.string == "A car leaves Britain's embassy in Moscow on Friday."]
    if len(legend) > 0:
        legend[0].string = "Awesome new legend"
    
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
