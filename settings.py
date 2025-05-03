# settings.py
BASE_URL = "https://www.tori.fi"
SEARCH_TERMS_FILE = "search_terms.txt"
CSV_OUTPUT_FILE = "new_listings.csv"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
}

# runtime settings

CHECK_INTERVAL_SECONDS = 30
SlEEP_TIME_SECONDS = 5  # Sleep time between requests to avoid being blocked

# Email settings
EMAIL_ENABLED = True  # Set to False to disable email notifications
EMAIL_SENDER = "your_email@gmail.com"
EMAIL_RECEIVER = "recipient_email@gmail.com"
EMAIL_PASSWORD = "your_app_password"  # Use a Gmail app password


EMAIL_INTERVAL_SECONDS = 300  # 10 minutes = 600
