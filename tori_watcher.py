import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
from datetime import datetime

from email_sender import send_grouped_email
from settings import BASE_URL, CHECK_INTERVAL_SECONDS, EMAIL_ENABLED, EMAIL_INTERVAL_SECONDS, SEARCH_TERMS_FILE, HEADERS, CSV_OUTPUT_FILE, SlEEP_TIME_SECONDS


SEEN_IDS = set()
FIRST_RUN = True



def load_search_terms(filename=SEARCH_TERMS_FILE):
    queries = []
    current_section = None
    allowed_sections = {"q", "category", "product_category", "sub_category"}

    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("//"):
                    continue  # Skip empty lines and comment lines

                # Section headers
                if line.lower().endswith(":"):
                    section_name = line[:-1].lower()
                    if section_name in allowed_sections:
                        current_section = section_name
                        continue
                    else:
                        break  # Stop reading when reaching unknown section like "muistio:"
                
                if current_section not in allowed_sections:
                    break

                # Parse comma-separated values
                parts = [part.strip() for part in line.split(",") if part.strip()]
                if current_section == "q":
                    queries.extend([f"q={term}" for term in parts])
                elif current_section == "category":
                    queries.extend([f"category={term}" for term in parts])
                elif current_section == "sub_category":
                    queries.extend([f"sub_category={term}" for term in parts])
                elif current_section == "product_category":
                    queries.extend([f"product_category={term}" for term in parts])

        return queries

    except FileNotFoundError:
        print(filename, "not found.")
        return []



def check_new_items(query, first_run=False):
    search_url = f"{BASE_URL}/recommerce/forsale/search?{query}&dealer_segment=1&sort=PUBLISHED_DESC"
    try:
        response = requests.get(search_url, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"Request failed for '{query}': {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    items = soup.select("article.sf-search-ad")

    new_items = []
    for item in items:

        badge = item.find("span", class_="badge--info")
        if badge and "Paalupaikka" in badge.text:
            continue  # Skippaa tämä ilmoitus


        link_tag = item.find("a", class_="sf-search-ad-link", href=True)
        if not link_tag:
            continue

        link = link_tag["href"]
        full_url = link if link.startswith("http") else BASE_URL + link
        ad_id = link.split("/")[-1]

        title = link_tag.get_text(strip=True)

        # Extract price if available
        price_tag = item.select_one("div.font-bold span")
        price = price_tag.get_text(strip=True) if price_tag else "N/A"

        # Extract timestamp (e.g., "minuutti sitten")
        time_tag = item.select_one("div.text-xs span:last-child")
        timestamp = time_tag.get_text(strip=True) if time_tag else "N/A"

        if ad_id not in SEEN_IDS:
            SEEN_IDS.add(ad_id)
            if not first_run:
                new_items.append({
                    "search_query": query,
                    "title": title,
                    "price": price,
                    "url": full_url,
                    "posted_time": timestamp,
                    "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })

    return new_items


def save_to_excel(items):
    if not items:
        return
    df = pd.DataFrame(items)
    try:
        existing_df = pd.read_csv(CSV_OUTPUT_FILE)
        df = pd.concat([existing_df, df], ignore_index=True)
    except FileNotFoundError:
        pass
    df.drop_duplicates(subset="url", inplace=True)
    df.to_csv(CSV_OUTPUT_FILE, index=False)
    print(f"Saved {len(items)} new items to {CSV_OUTPUT_FILE}")


def main_loop():
    global FIRST_RUN

    time_since_last_email = time.time()
    collected_items = []

    while True:
        search_queries = load_search_terms()
        all_new_items = []

        for query in search_queries:
            print(f"Checking: {query}")
            new_ads = check_new_items(query, first_run=FIRST_RUN)
            for ad in new_ads:
                print(f"Uusi ilmoitus: {ad['url']}")
            all_new_items.extend(new_ads)
            time.sleep(SlEEP_TIME_SECONDS)

        if not FIRST_RUN:
            save_to_excel(all_new_items)
            collected_items.extend(all_new_items)
        else:
            print("First run — not saving to file.")

        FIRST_RUN = False

        if EMAIL_ENABLED:
            # Check if it's time to send grouped email
            if time.time() - time_since_last_email >= EMAIL_INTERVAL_SECONDS:
                if collected_items:
                    send_grouped_email(collected_items)
                    collected_items = []
                time_since_last_email = time.time()

        print(f"Waiting {CHECK_INTERVAL_SECONDS} seconds...\n")
        time.sleep(CHECK_INTERVAL_SECONDS)




if __name__ == "__main__":
    main_loop()
