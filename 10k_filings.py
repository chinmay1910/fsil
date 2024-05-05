from sec_edgar_downloader import Downloader
import os

# Initialize the downloader with your company name and email address
dl = Downloader("Chinmay", "chinmayawade21@gmail.com")

# Define the list of company tickers
company_tickers = ["AAPL", "MSFT", "GOOGL"]  # Example: Apple, Microsoft, Google

# Define the years range
start_year = 1995
end_year = 2023

# Create a directory to save the filings
output_dir = "10K_filings"
os.makedirs(output_dir, exist_ok=True)

# Download 10-K filings for each company and year
for ticker in company_tickers:
    for year in range(start_year, end_year + 1):
        try:
            dl.get("10-K", ticker)
            print(f"Downloaded 10-K filing for {ticker} in {year}")
        except Exception as e:
            print(f"Error downloading 10-K filing for {ticker} in {year}: {e}")
