# pip install playwright
# playwright install
# python -m playwright codegen --target python -o 'zz.py' -b ff https://www.bbc.com
from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.firefox.launch(headless=False)
    context = browser.new_context()

    # Open new page
    page = context.new_page()

    # Go to https://www.bbc.com/
    page.goto("https://www.bbc.com/")

    # Go to https://www.bbc.co.uk/
    page.goto("https://www.bbc.co.uk/")

    # Click text=Yes, I agree
    page.click("text=Yes, I agree")

    # Click [data-testid="header-content"] >> :nth-match(:text("Home"), 2)
    page.click("[data-testid=\"header-content\"] >> :nth-match(:text(\"Home\"), 2)")
    # assert page.url == "https://www.bbc.co.uk/"

    # Click text=News
    page.click("text=News")
    # assert page.url == "https://www.bbc.co.uk/news"

    # Click text=Business
    page.click("text=Business")
    # assert page.url == "https://www.bbc.co.uk/news/business"

    # Click a:has-text("Easing delay to have 'critical impact' on business")
    page.click("a:has-text(\"Easing delay to have 'critical impact' on business\")")
    # assert page.url == "https://www.bbc.co.uk/news/business-57467449"

    # Close page
    page.close()

    # ---------------------
    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)