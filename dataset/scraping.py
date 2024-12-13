import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import os

BASE_URL = "https://www.onecle.com/contracts"

def fetch_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def get_contract_links(base_url):
    html_content = fetch_html(base_url)
    if html_content is None:
        return []
    
    soup = BeautifulSoup(html_content, 'html.parser')
    contract_links = []
    
    for link in soup.find_all('a', href=True):
        href = link.get('href')
        if href and href.startswith('/contracts'):
            contract_links.append(BASE_URL + href)  # Prepend base URL to relative link
    return contract_links

def extract_contract_content(content_url): 
    html_content = fetch_html(content_url)
    if html_content is None: 
        return None
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Refine the scraping to target specific elements (adjust if needed)
    content = soup.find('div', class_='content')  # Example: replace 'div.content' with the correct tag/class
    if content:
        return content.get_text(strip=True)
    return soup.get_text(strip=True)  # Fallback to full text

def scrap_contracts(base_url, max_contracts=10):
    contracts_links = get_contract_links(base_url)
    all_contracts = []
    
    for idx, link in enumerate(contracts_links[:max_contracts]):
        print(f"Scraping contract {idx + 1}/{max_contracts}: {link}")
        contract_text = extract_contract_content(link)
        if contract_text: 
            all_contracts.append({
                "url": link,    
                "text": contract_text
            })
            
        time.sleep(random.uniform(1, 2))
    
    return all_contracts

# Scraping contracts
scraped_contracts = scrap_contracts(BASE_URL, max_contracts=10)

# Save results to a CSV
if scraped_contracts:
    os.makedirs('./dataset/generated', exist_ok=True)  # Ensure directories exist
    df = pd.DataFrame(scraped_contracts)
    df.to_csv('./dataset/generated/scraped_contracts.csv', index=False)
    print(scraped_contracts[0]['text'][:1000])  # Print a preview of the first contract
else:
    print("No contracts scraped")
