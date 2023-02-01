import requests
from bs4 import BeautifulSoup
import re

# TODO: clean up
# TODO: progress bar

# TODO: complete blacklist
# List of websites that the scraper seems to have trouble with but emails very likely won't be there
blacklist = ["tripadvisor.com"]

def extractEmailAddresses(url, emailsSet):
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")

    # Method 1: commented out for now as method 2 gets all its results + more accurate
    # emails = re.findall(email_pattern, soup.text)
    # for email in emails:
    #     print(email)

    # Method 2
    mailtos = soup.select('a[href]')
    for i in mailtos:
        href = i['href']
        if "mailto:" in href:
            #print(href[7:])
            emailsSet.add(href[7:])
    
    return emailsSet

def getEmail(query):
    emailsSet = set()
    # TODO: some timeout i guess

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
    urls = [url for url in urls if notInBlacklist(url)]

    # Use a regular expression pattern to search for email addresses in the HTML
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

    # Loop over the URLs and extract any email addresses
    for url in urls:
        try:
            emailsSet = extractEmailAddresses(url, emailsSet)
        except:
            print("Following URL is a problem:")
            print(url)
        

    return emailsSet
        
        
def notInBlacklist(url):
    for blockedStr in blacklist:
        if blockedStr in url:
            return False
    return True

# Get the input file
input = open("input.txt", "r")

# Read data from the file and close it
data = input.read()
input.close()

# Get the search queries
queries = data.splitlines()

# Get emails for each search query
numQueries = len(queries)
i = 1
orgEmailsDict = {}
maxEmails = 0
for query in queries:
    print("On query " + str(i) + " out of " + str(numQueries))
    emails = getEmail(query)
    orgEmailsDict[query] = emails
    if len(emails) > maxEmails:
        maxEmails = len(emails)
    i += 1

# Set up the CSV string header
csvString = "ORG"
for i in range(1, maxEmails+1):
    csvString += ",EMAIL" + str(i)
csvString += "\n"

# Add each query and email to the CSV string
for org, orgEmails in orgEmailsDict.items():
    orgCleaned = org.replace(',', '')
    csvString += orgCleaned
    i = 0
    for email in orgEmails:
        csvString += "," + email
        i += 1
    # Add empty cells to conform to CSV format
    for j in range(0, maxEmails - i):
        csvString += ", "
    csvString += "\n"

# Write output to file
output = open("output.csv", "w")
output.writelines(csvString)
output.close()



# individual link testing
# url = "https://www.apsarasarts.com/contact-us/&sa=U&ved=2ahUKEwi25fjwtvL8AhVkXmwGHaOBCQgQjBB6BAgDEAk&usg=AOvVaw0fVa-nuw16f6Q2O-oipcUr"
# response = requests.get(url)
# html_content = response.text
# soup = BeautifulSoup(html_content, "html.parser")
# print(soup)
