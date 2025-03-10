import asyncio
from playwright.async_api import async_playwright, expect

async def test_has_title(page):
    await page.goto("https://playwright.dev/")

    # Expect a title "to contain" a substring.
    await expect(page).to_have_title(r"Playwright")

async def test_get_started_link(page):
    await page.goto("https://playwright.dev/")

    # Click the get started link.
    await page.get_by_role("link", name="Get started").click()

    # Expects page to have a heading with the name of Installation.
    await expect(page.get_by_role("heading", name="Installation")).to_be_visible()


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            executable_path=r'C:\Users\kaizh\AppData\Local\ms-playwright\chromium_headless_shell-1161\chrome-win\headless_shell.exe',
            headless=True
        )  # You can change the browser type here

        page = await browser.new_page()

        # Run the tests
        # await test_has_title(page) # this will cause error on line 8
        await test_get_started_link(page)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
