import requests 
from bs4 import BeautifulSoup 

url = 'http://quotes.toscrape.com/'
all_quotes = []
all_authors = []
while url:
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        quotes = soup.find_all('span', class_='text')
        authors = soup.find_all('small', class_='author')
        all_authors.extend(authors)
        all_quotes.extend(quotes)
        next_button = soup.find('li', class_ = 'next')
        url = next_button.find('a')['href'] if next_button else None
        if url:
            url = 'http://quotes.toscrape.com' + url
    else:
        print("Errol when load page: ", response.status_code)
        break

print(f"Total quotes: {len(all_quotes)}")
with open('quotes.txt', 'w', encoding='utf-8') as f:
            for i in range(len(all_quotes)):
                line = f'Quote {i+1}: {all_quotes[i].text} - {all_authors[i].text}\n'
                f.write(line)
                print(line.strip())
print("Saved to quotes.txt")