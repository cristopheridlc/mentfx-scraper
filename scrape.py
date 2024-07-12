import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

# URL of the iframe containing the table
iframe_url = 'https://mentfx.com/sentiment-viewer/index.php'

# Send a GET request to the iframe URL
response = requests.get(iframe_url)
response.raise_for_status()  # Raise an exception for HTTP errors

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Find the table with sentiment data
table = soup.find('table', {'class': 'sentiment-table'})

# Debug print to check if the table was found
if table:
    print("Table found!")
else:
    print("Table not found.")

# Parse the sentiment data from the table if the table exists
if table:
    def parse_sentiment_data(table):
        sentiment_data = []
        rows = table.find_all('tr')[1:]  # Skip the header row
        for row in rows:
            cols = row.find_all('td')
            symbol = cols[0].text.strip()
            intraday_bearish = int(cols[1].find('div', class_='bearish').text.strip('%')) / 100
            intraday_bullish = int(cols[1].find('div', class_='bullish').text.strip('%')) / 100
            daily_bearish = int(cols[2].find('div', class_='bearish').text.strip('%')) / 100
            daily_bullish = int(cols[2].find('div', class_='bullish').text.strip('%')) / 100
            sentiment_data.append({
                'Symbol': symbol,
                'Intraday Bearish': intraday_bearish,
                'Intraday Bullish': intraday_bullish,
                'Daily Bearish': daily_bearish,
                'Daily Bullish': daily_bullish,
                'Report Date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
        return sentiment_data

    sentiment_data = parse_sentiment_data(table)
    
    # Specify the CSV file to write to
    csv_file = 'sentiment_data.csv'
    
    # Write the data to a CSV file
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['Symbol', 'Intraday Bearish', 'Intraday Bullish', 'Daily Bearish', 'Daily Bullish', 'Report Date'])
        writer.writeheader()
        for data in sentiment_data:
            writer.writerow(data)
    
    print(f"Sentiment data has been written to {csv_file}")
else:
    print("No table to parse.")