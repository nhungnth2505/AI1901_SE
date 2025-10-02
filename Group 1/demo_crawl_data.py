
import requests 
from bs4 import BeautifulSoup  
import nltk
# nltk.download('punkt')
# nltk.download('punkt_tab')  
import re  
import csv

def download_and_tokenize_wikipedia_pages(urls):

    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        print("Đang tải gói 'punkt' của NLTK...")
        nltk.download('punkt')
        print("Tải xong!")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    all_cleaned_tokens = []

    for url in urls:
        print(f"\nĐang xử lý URL: {url}")
        
        try:
            response = requests.get(url, headers= headers, timeout=10)
            response.raise_for_status() 
            
            soup = BeautifulSoup(response.text, 'html.parser')
            raw_text = soup.get_text()
            
            # Kết quả là một danh sách các từ và dấu câu. Vd: ['Python', 'is', 'an', 'interpreted', ',', 'high-level', ...]
            tokens = nltk.word_tokenize(raw_text)
            
            cleaned_tokens_for_page = []
            for token in tokens:
                if re.fullmatch('[a-zA-Z]+', token):
                    cleaned_tokens_for_page.append(token.lower())
            
            print(f"Tìm thấy {len(cleaned_tokens_for_page)} token hợp lệ trên trang này.")
            all_cleaned_tokens.extend(cleaned_tokens_for_page)

        except requests.exceptions.RequestException as e:
            print(f"Lỗi khi tải URL {url}: {e}")

    return all_cleaned_tokens

def save_tokens_to_csv(tokens, filename='cleaned_tokens.csv'):
    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['token'])
            for token in tokens:
                writer.writerow([token])
        print(f"\nSuccessed: saved {len(tokens)} token to file '{filename}'")
    except IOError as e:
        print(f"\nErrol when save file: {e}")

if __name__ == "__main__":
    
    wikipedia_urls = [
        'https://en.wikipedia.org/wiki/Python_(programming_language)',
        'https://en.wikipedia.org/wiki/Java_(programming_language)',
        'https://en.wikipedia.org/wiki/JavaScript'
    ]
    
    final_tokens = download_and_tokenize_wikipedia_pages(wikipedia_urls)
    
    print("\n--------------------------------------------------")
    print(f"Tổng cộng đã thu thập và làm sạch được {len(final_tokens)} tokens.")
    
    print("99 TOKEN đầu tiên:")
    print(final_tokens[:99])
    if final_tokens:
        save_tokens_to_csv(final_tokens)