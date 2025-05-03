# 🕵️‍♂️ Tori.fi Scraper & Email Notifier

This Python project monitors [Tori.fi](https://www.tori.fi) for new listings based on search terms defined in a configuration file. It sends grouped email notifications about new listings and saves results to a CSV file.

## 📦 Features

- Scrapes Tori.fi for new ads based on custom search filters.
- Filters out sponsored ads ("Paalupaikka").
- Groups new listings and sends email notifications periodically.
- Saves results to a CSV file.
- Configurable via `search_terms.txt` and `settings.py`.

## 📁 Project Structure

```
.
├── tori_watcher.py         # Main scraper and loop logic
├── email_sender.py         # Email sending functionality
├── settings.py             # Configurable settings (timing, email, paths)
├── search_terms.txt        # Define search parameters (keywords, categories)
├── new_listings.csv        # Output file for new listings (auto-generated)
├── requirements.txt        # List of required depensies
```

## ⚙️ Configuration

### 1. Search Terms

Edit `search_terms.txt`:

```txt
q:
ryzen, iphone

sub_category:
1.93.3217,

product_category:
2.93.3217.39,
```

Supported sections: `q`, `category`, `sub_category`, `product_category`

> ❗ Non-supported sections like `muistio:` are ignored.

### 2. Settings

Edit `settings.py` to adjust runtime behavior:

```python
EMAIL_SENDER = "your_email@gmail.com"
EMAIL_RECEIVER = "recipient_email@gmail.com"
EMAIL_PASSWORD = "your_app_password"  # Gmail app password required

CHECK_INTERVAL_SECONDS = 30
EMAIL_INTERVAL_SECONDS = 300
SlEEP_TIME_SECONDS = 5
```

## 🚀 How to Run

### Requirements

- Python 3.8+
- `requests`, `beautifulsoup4`, `pandas`

Install dependencies:

```bash
pip install -r requirements.txt
```

### Run the Scraper

```bash
python tori_watcher.py
```

The script will:
1. Load and parse your search terms.
2. Check Tori.fi for new listings.
3. Skip already seen or sponsored ads.
4. Send an email summary every 5 minutes (configurable).
5. Log new listings to `new_listings.csv`.



## 📬 Email Setup Notes

- Use a Gmail App Password: [Enable 2FA & generate an app password](https://support.google.com/accounts/answer/185833?hl=en).
- Ensure "Less secure apps" is disabled and SMTP is allowed.

## 🛑 Notes

- First run will not trigger email sending or file saving (prevents spam).
- Duplicate URLs are filtered out when saving.
- Emails can be disabled from settings.py
- The checking of new listings will start anew when starting the program, so 
the first run of searches will not be flagged as new listings.
- if `new_listings.csv` is not found, the program will create one.