import asyncio
from playwright.async_api import async_playwright
import json
import pandas as pd

async def get_company_tickers_with_playwright(url="https://www.sec.gov/files/company_tickers.json"):
    """
    Uses Playwright Async API to fetch content from the SEC company tickers JSON URL and returns the data as a DataFrame.

    Args:
        url (str): The URL of the SEC company tickers JSON file.

    Returns:
        pandas.DataFrame: A DataFrame containing the company ticker data, or None if an error occurs.
    """
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False) # has to be false. otherwise 403
            page = await browser.new_page()
            response = await page.goto(url)

            if response.status != 200:
                print(f"Failed to fetch URL: {url}, status code: {response.status}")
                await browser.close()
                return None

            content = await response.body()
            await browser.close()
            
            # Convert bytes to string, then parse JSON
            data = json.loads(content.decode('utf-8'))
            
            # Convert the dictionary to a list of dictionaries
            # Data is in a strange format (index number -> data dict). Let's reformat it
            data_list = []
            for key in data:
                data_list.append(data[key])
            
            df = pd.DataFrame(data_list)
            return df

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

async def main():
    tickers_df = await get_company_tickers_with_playwright()
    if tickers_df is not None:
        print("Company Tickers DataFrame:")
        print(tickers_df.head())
        print(tickers_df.info())
    else:
        print("Failed to retrieve company ticker data.")

if __name__ == "__main__":
    asyncio.run(main())
