import requests
from bs4 import BeautifulSoup
import re

# TODO: output methods 1 and 2 into separate files with the org name
# TODO: take query list from csv file or something

# Define the search query
query = "ESCAPE THEATRE LTD."

# Build the Google search URL
url = f"https://www.google.com/search?q={query}"

# Send a request to the URL and retrieve the HTML content
response = requests.get(url)
html_content = response.text

# Use BeautifulSoup to parse the HTML content
soup = BeautifulSoup(html_content, "html.parser")

# Find all the search result links
links = [link.get("href") for link in soup.find_all("a")]

# Filter the links
urls = [link for link in links if link.startswith("/url?q=")]
urls = [url.split("?q=")[1] for url in urls]
urls = [url.split("&")[0] for url in urls]

# Use a regular expression pattern to search for email addresses in the HTML
email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

# Loop over the URLs and extract any email addresses
for url in urls:
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")

    # Method 1
    emails = re.findall(email_pattern, soup.text)
    for email in emails:
        print(email)

    # Method 2
    mailtos = soup.select('a[href]')
    for i in mailtos:
        href = i['href']
        if "mailto:" in href:
            print(href[7:])

# individual link testing
# url = "https://www.apsarasarts.com/contact-us/&sa=U&ved=2ahUKEwi25fjwtvL8AhVkXmwGHaOBCQgQjBB6BAgDEAk&usg=AOvVaw0fVa-nuw16f6Q2O-oipcUr"
# response = requests.get(url)
# html_content = response.text
# soup = BeautifulSoup(html_content, "html.parser")
# print(soup)
