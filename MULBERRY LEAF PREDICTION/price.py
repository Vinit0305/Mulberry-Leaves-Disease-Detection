'''
import requests
from bs4 import BeautifulSoup
from urllib.request import unquote

url='https://sericulture.karnataka.gov.in/info-4/Daily+Cocoon+Rates/Commercial+Cocoons+Rates/en'

response=requests.get(url)

content=BeautifulSoup(response.text,'lxml')
all_urls=content.find_all('a')



for url in all_urls:
    try:
        if 'pdf' in url['href']:
           
            if 'https' not in url['href']:
                pdf_url=url['href']
            else:
                pdf_url=url['href']

            pdf_response=requests.get(url['href'])

            filename=unquote(pdf_response.url).split('/')[-1].replace(' ','_')

            with open('./pdf/'+filename,'wb') as f:
                f.write(pdf_response.content)
            
           
            print(pdf_url)
         


           
    except :
        pass
'''
'''
import requests
from bs4 import BeautifulSoup
import datetime

# URL of the website containing the PDF files
url='https://sericulture.karnataka.gov.in/info-4/Daily+Cocoon+Rates/Commercial+Cocoons+Rates/en'


# Get the dates of the current week in the format used in the PDF filenames
today = datetime.date.today()
start_of_week = today - datetime.timedelta(days=today.weekday())
dates = [(start_of_week + datetime.timedelta(days=i)).strftime('%d-%#m-%y') for i in range(7)]

# Send a GET request to the website and parse the HTML content
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Find all links on the website
links = soup.find_all('a')

# Filter the links to include only those that have a filename matching one of the dates of the current week
pdf_links = []
for link in links:
    try:
        href = link['href']
        if href.endswith('.pdf') and any(date in href for date in dates):
            pdf_links.append(href)
    except KeyError:
        pass

# Download the PDF files that match one of the dates of the current week
for pdf_link in pdf_links:
    response = requests.get(pdf_link)
    filename = pdf_link.split('/')[-1]
    if any(date in filename for date in dates):
        with open(filename, 'wb') as f:
            f.write(response.content)
            print('Downloaded:', filename)
'''
'''

import datetime
import os
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, url_for

app = Flask(__name__)

# Define the URL of the website to scrape
url='https://sericulture.karnataka.gov.in/info-4/Daily+Cocoon+Rates/Commercial+Cocoons+Rates/en'

# Define the directory where the downloaded PDF files will be stored
downloads_dir = "static/pdf"

# Define the start date of the week to scrape
today = datetime.date.today()
start_of_week = today - datetime.timedelta(days=today.weekday())

# Define the list of dates for the current week
dates = [(start_of_week + datetime.timedelta(days=i)).strftime('%d-%m-%y') for i in range(7)]

# Scrape the website for PDF links and download the PDF files
pdf_links = []
for date in dates:
    filename = date + ".pdf"
    response = requests.get(url + "/" + filename)
    if response.status_code == 200:
        with open(os.path.join(downloads_dir, filename), 'wb') as f:
            f.write(response.content)
        pdf_links.append((date, filename))

# Render the webpage with the PDF files in a table
@app.route('/')
def index():
    return render_template('index.html', pdf_links=pdf_links)

if __name__ == '__main__':
    app.run(debug=True)
    '''
'''
import requests
from datetime import datetime, timedelta

# URL to scrape the PDF file from
base_url = "https://sericulture.karnataka.gov.in/info-4/Daily+Cocoon+Rates/Commercial+Cocoons+Rates/en"
# Date format of the PDF file
file_format = "%d-%#m-%y.pdf"
# Number of days before the current date to get the PDF file from
days_back = 2

# Calculate the date to get the PDF file from
two_days_back = datetime.now() - timedelta(days=days_back)
date_format = two_days_back.strftime(file_format)

# Get the PDF file URL
url = base_url + date_format

# Download the PDF file
response = requests.get(url)
filename = date_format.replace('.pdf', '.pdf')
with open('./pdf/' + filename, 'wb') as f:
    f.write(response.content)
print(f"Downloaded file: {filename}")
'''
'''
import os
import requests
from bs4 import BeautifulSoup
import datetime
from flask import Flask, render_template



app = Flask(__name__)


url = 'https://sericulture.karnataka.gov.in/info-4/Daily+Cocoon+Rates/Commercial+Cocoons+Rates/en'

# Directory where the downloaded PDF files will be stored
pdf_dir = './static/pdf'

# Get the dates of the current week in the format used in the PDF filenames
today = datetime.date.today()
start_of_week = today - datetime.timedelta(days=today.weekday())
dates = [(start_of_week + datetime.timedelta(days=i)).strftime('%d-%#m-%y') for i in range(7)]

# Download the PDF files that match one of the dates of the current week
for date in dates:
    pdf_filename = os.path.join(pdf_dir, f'{date}.pdf')
    if not os.path.exists(pdf_filename):
        # Send a GET request to the website and parse the HTML content
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all links on the website
        links = soup.find_all('a')

        # Filter the links to include only those that have a filename matching the current date
        pdf_links = []
        for link in links:
            try:
                href = link['href']
                if href.endswith('.pdf') and date in href:
                    pdf_links.append(href)
            except KeyError:
                pass

        # Download the first PDF file that matches the current date
        if pdf_links:
            pdf_link = pdf_links[0]
            response = requests.get(pdf_link)
            with open(pdf_filename, 'wb') as f:
                f.write(response.content)

@app.route('/')
def index():
    # Get a list of all downloaded PDF files and their corresponding dates
    pdf_files = []
    for pdf_filename in os.listdir(pdf_dir):
        pdf_date = pdf_filename.split('.')[0]
        pdf_date = datetime.datetime.strptime(pdf_date, '%d-%m-%y').strftime('%d-%b-%Y')
        pdf_files.append((pdf_date, pdf_filename))

    # Render the template with the list of PDF files
    return render_template('price.html', pdf_files=pdf_files)

if __name__ == '__main__':
    app.run(debug=True)

'''
'''




url = 'https://sericulture.karnataka.gov.in/info-4/Daily+Cocoon+Rates/Commercial+Cocoons+Rates/en'

# Directory where the downloaded PDF files will be stored


# Get the dates of the current week in the format used in the PDF filenames
today = datetime.date.today()
start_of_week = today - datetime.timedelta(days=today.weekday())
dates = [(start_of_week + datetime.timedelta(days=i)).strftime('%d-%#m-%y') for i in range(7)]

# Download the PDF files that match one of the dates of the current week
for date in dates:
    pdf_filename = os.path.join(pdf_dir, f'{date}.pdf')
    if not os.path.exists(pdf_filename):
        # Send a GET request to the website and parse the HTML content
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all links on the website
        links = soup.find_all('a')

        # Filter the links to include only those that have a filename matching the current date
        pdf_links = []
        for link in links:
            try:
                href = link['href']
                if href.endswith('.pdf') and date in href:
                    pdf_links.append(href)
            except KeyError:
                pass

        # Download the first PDF file that matches the current date
        if pdf_links:
            pdf_link = pdf_links[0]
            response = requests.get(pdf_link)
            with open(pdf_filename, 'wb') as f:
                f.write(response.content)
'''
import os
import requests
from bs4 import BeautifulSoup
import datetime
from flask import Blueprint, render_template
price_app = Blueprint('price', __name__)
pdf_dir = './static/pdf'
@price_app.route('/price')
def index():
    # Get a list of all downloaded PDF files and their corresponding dates
    pdf_files = []
    for pdf_filename in os.listdir(pdf_dir):
        pdf_date = pdf_filename.split('.')[0]
        pdf_date = datetime.datetime.strptime(pdf_date, '%d-%m-%y').strftime('%d-%b-%Y')
        pdf_files.append((pdf_date, pdf_filename))

    # Render the template with the list of PDF files
    return render_template('price.html', pdf_files=pdf_files)
