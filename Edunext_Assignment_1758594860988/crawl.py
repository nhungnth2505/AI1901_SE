# import requests
# from bs4 import BeautifulSoup
# from urllib.parse import urljoin, urlparse
# import threading
# import queue
# import time
# import json
# import csv
# import os
# from datetime import datetime

# BASE_URL = "https://www.vinamilk.com.vn/" #"https://fpt.com/vi"
# DOMAIN = "www.vinamilk.com.vn" #"fpt.com"
# MAX_THREADS = 5
# CRAWL_DELAY = 1  

# visited = set()
# q = queue.Queue()

# SAVE_FORMAT = "json"  # json, csv, txt, all
# OUTPUT_DIR = "crawled_data"
# os.makedirs(OUTPUT_DIR, exist_ok=True)

# crawled_data = []
# lock = threading.Lock()

# def check_robots(url, user_agent='*'):
#     robots_url = urljoin(url, "/robots.txt")
    
#     try:
#         res = requests.get(robots_url, timeout=5)
#         if res.status_code != 200:
#             return True
#         return is_url_allowed_by_robots(url, res.text, user_agent)
#     except Exception as e:
#         print("Error checking robots.txt:", e)
#         return True

# def is_url_allowed_by_robots(url, robots_content, user_agent='*'):
#     lines = robots_content.split('\n')
#     user_agent_rules = {}
#     current_ua = None
    
#     for line in lines:
#         line = line.strip()
#         if not line or line.startswith('#'):
#             continue
            
#         if line.lower().startswith('user-agent:'):
#             current_ua = line.split(':', 1)[1].strip()
#             user_agent_rules[current_ua] = {'disallow': [], 'allow': []}
#         elif line.lower().startswith('disallow:') and current_ua is not None:
#             path = line.split(':', 1)[1].strip()
#             user_agent_rules[current_ua]['disallow'].append(path)
#         elif line.lower().startswith('allow:') and current_ua is not None:
#             path = line.split(':', 1)[1].strip()
#             user_agent_rules[current_ua]['allow'].append(path)
    
#     rules = user_agent_rules.get(user_agent, user_agent_rules.get('*', {'disallow': [], 'allow': []}))
    
#     parsed_url = urlparse(url)
#     path = parsed_url.path
#     query = parsed_url.query
    
#     for disallow_rule in rules['disallow']:
#         if matches_rule(path, query, disallow_rule):
#             allowed_by_exception = False
#             for allow_rule in rules['allow']:
#                 if matches_rule(path, query, allow_rule) and len(allow_rule) > len(disallow_rule):
#                     allowed_by_exception = True
#                     break
#             if not allowed_by_exception:
#                 print(f"URL disallowed by robots.txt rule: {disallow_rule}")
#                 return False
#     return True

# def matches_rule(path, query, rule):
#     if '?' in rule:
#         rule_path, rule_query = rule.split('?', 1)
#         if rule_query.endswith('*'):
#             query_prefix = rule_query[:-1]
#             return path == rule_path and query.startswith(query_prefix)
#         else:
#             return path == rule_path and query == rule_query
#     else:
#         if rule.endswith('*'):
#             return path.startswith(rule[:-1])
#         else:
#             return path == rule

# def is_valid_link(href):
#     if not href:
#         return False
#     parsed = urlparse(href)
#     return DOMAIN in parsed.netloc and parsed.path.startswith("/vi")

# def extract_page_data(soup, url):
#     try:
#         title = soup.find('title')
#         title_text = title.text.strip() if title else "No title"
        
#         main_content = soup.find('main') or soup.find('article') or soup.find('div', class_='content')
#         if main_content:
#             text_content = main_content.get_text(separator=' ', strip=True)
#         else:
#             for script in soup(["script", "style"]):
#                 script.decompose()
#             text_content = soup.get_text(separator=' ', strip=True)
        
#         meta_desc = soup.find('meta', attrs={'name': 'description'})
#         description = meta_desc['content'] if meta_desc else ""
        
#         links = []
#         for a in soup.find_all('a', href=True):
#             link_text = a.get_text(strip=True)
#             link_url = urljoin(url, a['href'])
#             if link_text and len(link_text) < 1000: 
#                 links.append({'text': link_text, 'url': link_url})
        
#         headings = {}
#         for i in range(1, 4):
#             heading_tags = soup.find_all(f'h{i}')
#             headings[f'h{i}'] = [h.get_text(strip=True) for h in heading_tags if h.get_text(strip=True)]
        
#         return {
#             'url': url,
#             'title': title_text,
#             'description': description,
#             'content': text_content[:10000],  
#             'links_count': len(links),
#             'sample_links': links[:10],  
#             'headings': headings,
#             'crawled_at': datetime.now().isoformat(),
#             'content_length': len(text_content)
#         }
#     except Exception as e:
#         print(f"Error extracting data from {url}: {e}")
#         return {
#             'url': url,
#             'title': 'Error extracting data',
#             'content': '',
#             'crawled_at': datetime.now().isoformat(),
#             'error': str(e)
#         }

# def save_data():
#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
#     with lock:
#         data_to_save = crawled_data.copy()
    
#     if SAVE_FORMAT == "json" or SAVE_FORMAT == "all":
#         json_file = os.path.join(OUTPUT_DIR, f"crawled_data_{timestamp}.json")
#         with open(json_file, 'w', encoding='utf-8') as f:
#             json.dump(data_to_save, f, ensure_ascii=False, indent=2)
#         print(f"Data saved to {json_file}")
    
#     if SAVE_FORMAT == "csv" or SAVE_FORMAT == "all":
#         csv_file = os.path.join(OUTPUT_DIR, f"crawled_data_{timestamp}.csv")
#         with open(csv_file, 'w', newline='', encoding='utf-8') as f:
#             if data_to_save:
#                 writer = csv.writer(f)
#                 writer.writerow(['URL', 'Title', 'Description', 'Content Length', 'Links Count', 'Crawled At'])
#                 for item in data_to_save:
#                     writer.writerow([
#                         item['url'],
#                         item['title'][:1000], 
#                         item['description'][:1000],
#                         item.get('content_length', 0),
#                         item.get('links_count', 0),
#                         item['crawled_at']
#                     ])
#         print(f"Data saved to {csv_file}")
    
#     if SAVE_FORMAT == "txt" or SAVE_FORMAT == "all":
#         txt_file = os.path.join(OUTPUT_DIR, f"crawled_data_{timestamp}.txt")
#         with open(txt_file, 'w', encoding='utf-8') as f:
#             for item in data_to_save:
#                 f.write(f"URL: {item['url']}\n")
#                 f.write(f"Title: {item['title']}\n")
#                 f.write(f"Description: {item['description']}\n")
#                 f.write(f"Content Length: {item.get('content_length', 0)}\n")
#                 f.write(f"Links Count: {item.get('links_count', 0)}\n")
#                 f.write(f"Crawled At: {item['crawled_at']}\n")
#                 f.write("-" * 80 + "\n")
#         print(f"Data saved to {txt_file}")

# def crawl(url):
#     try:
#         time.sleep(CRAWL_DELAY)
#         print(f"Crawling: {url}")
        
#         if not check_robots(url):
#             print(f"Skipping {url} - disallowed by robots.txt")
#             return
            
#         res = requests.get(url, timeout=10)
#         if res.status_code != 200:
#             print(f"Failed to crawl {url}: Status code {res.status_code}")
#             return
            
#         soup = BeautifulSoup(res.text, "html.parser")
        
#         page_data = extract_page_data(soup, url)
        
#         with lock:
#             crawled_data.append(page_data)
        
#         for a in soup.find_all("a", href=True):
#             link = urljoin(BASE_URL, a["href"])
#             if is_valid_link(link) and link not in visited:
#                 visited.add(link)
#                 q.put(link)
                
#     except Exception as e:
#         print(f"Error crawling {url}: {e}")

# def worker():
#     while True:
#         try:
#             url = q.get(timeout=10) 
#             crawl(url)
#             q.task_done()
#         except queue.Empty:
#             break

# def main():
#     if not check_robots(BASE_URL):
#         print(f"Cannot crawl {BASE_URL} - disallowed by robots.txt")
#         return
        
#     visited.add(BASE_URL)
#     q.put(BASE_URL)
    
#     print(f"Starting crawl of {BASE_URL} with {MAX_THREADS} threads")
#     print(f"Data will be saved in {SAVE_FORMAT.upper()} format to {OUTPUT_DIR}/")
    
#     threads = []
#     for _ in range(MAX_THREADS):
#         t = threading.Thread(target=worker)
#         t.daemon = True
#         t.start()
#         threads.append(t)
    
#     q.join()
    
#     save_data()
    
#     print(f"Crawling completed. Crawled {len(crawled_data)} pages.")
#     print(f"Unique URLs found: {len(visited)}")

# if __name__ == "__main__":
#     main()

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import threading
import queue
import time
import json
import csv
import os
import re
from datetime import datetime

MAX_THREADS = 5
CRAWL_DELAY = 1
SAVE_FORMAT = "json"
OUTPUT_DIR = "crawled_data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

visited = set()
q = queue.Queue()
crawled_data = []
lock = threading.Lock()

class RobotsParser:
    def __init__(self, robots_url, user_agent='*'):
        self.user_agent = user_agent
        self.rules = {}
        self.sitemaps = []
        self._parse(robots_url)

    def _parse(self, robots_url):
        try:
            res = requests.get(robots_url, timeout=10)
            if res.status_code != 200:
                return
            content = res.text
            lines = content.split('\n')
            current_agents = []
            for line in lines:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if line.lower().startswith('user-agent:'):
                    agent = line.split(':', 1)[1].strip()
                    current_agents = [agent]
                    if agent not in self.rules:
                        self.rules[agent] = []
                elif line.lower().startswith('allow:'):
                    path = line.split(':', 1)[1].strip()
                    for agent in current_agents:
                        self.rules.setdefault(agent, []).append(('allow', path))
                elif line.lower().startswith('disallow:'):
                    path = line.split(':', 1)[1].strip()
                    for agent in current_agents:
                        self.rules.setdefault(agent, []).append(('disallow', path))
                elif line.lower().startswith('sitemap:'):
                    sitemap_url = line.split(':', 1)[1].strip()
                    self.sitemaps.append(sitemap_url)

        except Exception as e:
            print("Error parsing robots.txt:", e)

    def is_allowed(self, url, user_agent=None):
        ua = user_agent or self.user_agent
        parsed_url = urlparse(url)
        path = parsed_url.path
        query = parsed_url.query
        # Get rules for specific agent, else fallback to '*'
        rules = self.rules.get(ua, self.rules.get('*', []))
        matched_rule = None
        matched_len = -1
        for rule_type, rule_path in rules:
            # Convert robots.txt pattern to regex
            pattern = self._pattern_to_regex(rule_path)
            target = path
            if '?' in rule_path:
                # robots.txt rule with query string
                rule_path_split = rule_path.split('?', 1)
                pattern = self._pattern_to_regex(rule_path_split[0])
                if not re.match(pattern, path):
                    continue
                if not query.startswith(rule_path_split[1].replace('*', '')):
                    continue
            elif not re.match(pattern, path):
                continue
            # Longest rule wins
            if len(rule_path) > matched_len:
                matched_rule = rule_type
                matched_len = len(rule_path)
        # Default allow if no rule matched
        return matched_rule != 'disallow'

    def _pattern_to_regex(self, pattern):
        # Convert robots.txt wildcard pattern to regex
        pattern = re.escape(pattern)
        pattern = pattern.replace('\\*', '.*')
        pattern = '^' + pattern
        return pattern

def extract_page_data(soup, url):
    try:
        title = soup.find('title')
        title_text = title.text.strip() if title else "No title"
        main_content = soup.find('main') or soup.find('article') or soup.find('div', class_='content')
        if main_content:
            text_content = main_content.get_text(separator=' ', strip=True)
        else:
            for script in soup(["script", "style"]):
                script.decompose()
            text_content = soup.get_text(separator=' ', strip=True)
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        description = meta_desc['content'] if meta_desc else ""
        links = []
        for a in soup.find_all('a', href=True):
            link_text = a.get_text(strip=True)
            link_url = urljoin(url, a['href'])
            if link_text and len(link_text) < 1000:
                links.append({'text': link_text, 'url': link_url})
        headings = {}
        for i in range(1, 4):
            heading_tags = soup.find_all(f'h{i}')
            headings[f'h{i}'] = [h.get_text(strip=True) for h in heading_tags if h.get_text(strip=True)]
        return {
            'url': url,
            'title': title_text,
            'description': description,
            'content': text_content[:10000],
            'links_count': len(links),
            'sample_links': links[:10],
            'headings': headings,
            'crawled_at': datetime.now().isoformat(),
            'content_length': len(text_content)
        }
    except Exception as e:
        print(f"Error extracting data from {url}: {e}")
        return {
            'url': url,
            'title': 'Error extracting data',
            'content': '',
            'crawled_at': datetime.now().isoformat(),
            'error': str(e)
        }

def save_data():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    with lock:
        data_to_save = crawled_data.copy()
    if SAVE_FORMAT == "json" or SAVE_FORMAT == "all":
        json_file = os.path.join(OUTPUT_DIR, f"crawled_data_{timestamp}.json")
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data_to_save, f, ensure_ascii=False, indent=2)
        print(f"Data saved to {json_file}")

def is_valid_link(href, domain, base_path=None):
    if not href:
        return False
    parsed = urlparse(href)
    if domain not in parsed.netloc:
        return False
    if base_path:
        return parsed.path.startswith(base_path)
    # else allow all paths within domain
    return True

def crawl(url, robots_parser, domain, base_path=None):
    try:
        time.sleep(CRAWL_DELAY)
        print(f"Crawling: {url}")
        if not robots_parser.is_allowed(url):
            print(f"Skipping {url} - disallowed by robots.txt")
            return
        res = requests.get(url, timeout=10)
        if res.status_code != 200:
            print(f"Failed to crawl {url}: Status code {res.status_code}")
            return
        soup = BeautifulSoup(res.text, "html.parser")
        page_data = extract_page_data(soup, url)
        with lock:
            crawled_data.append(page_data)
        for a in soup.find_all("a", href=True):
            link = urljoin(url, a["href"])
            if is_valid_link(link, domain, base_path) and link not in visited:
                visited.add(link)
                q.put(link)
    except Exception as e:
        print(f"Error crawling {url}: {e}")

def worker(robots_parser, domain, base_path=None):
    while True:
        try:
            url = q.get(timeout=10)
            crawl(url, robots_parser, domain, base_path)
            q.task_done()
        except queue.Empty:
            break

def main(BASE_URL, DOMAIN, BASE_PATH=None, USER_AGENT='*'):
    robots_url = urljoin(BASE_URL, "/robots.txt")
    robots_parser = RobotsParser(robots_url, user_agent=USER_AGENT)
    print("Sitemaps found:", robots_parser.sitemaps)
    visited.add(BASE_URL)
    q.put(BASE_URL)
    print(f"Starting crawl of {BASE_URL} with {MAX_THREADS} threads")
    threads = []
    for _ in range(MAX_THREADS):
        t = threading.Thread(target=worker, args=(robots_parser, DOMAIN, BASE_PATH))
        t.daemon = True
        t.start()
        threads.append(t)
    q.join()
    save_data()
    print(f"Crawling completed. Crawled {len(crawled_data)} pages.")
    print(f"Unique URLs found: {len(visited)}")

if __name__ == "__main__":
    # main(BASE_URL="https://fpt.com/vi", DOMAIN="fpt.com", BASE_PATH="/vi")
    main(BASE_URL="https://www.nvidia.com", DOMAIN="www.nvidia.com", BASE_PATH="/en-us")