import asyncio
import json
import os
from playwright.async_api import async_playwright
from dotenv import load_dotenv

# --- Load credentials safely from .env file ---
load_dotenv()
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
LOGIN_URL = os.getenv("LOGIN_URL", "https://example.com/login")

SESSION_FILE = "storage_state.json"
OUTPUT_FILE = "products.json"


async def login_and_save_session(page):
    """
    Log in with provided credentials and save session state.
    """
    print("Logging in...")
    await page.goto(LOGIN_URL)

    # --- Replace selectors with your app's login form selectors ---
    await page.fill("input[name='username']", USERNAME)
    await page.fill("input[name='password']", PASSWORD)
    await page.click("button[type='submit']")

    # Smart wait until Menu button is visible (proof login success)
    await page.wait_for_selector("#menuButton")
    print("Login successful, saving session...")
    await page.context.storage_state(path=SESSION_FILE)


async def load_session(playwright):
    """
    Try to load existing session. If not available, login and save new session.
    """
    browser = await playwright.chromium.launch(headless=False)

    if os.path.exists(SESSION_FILE):
        print("Using existing session...")
        context = await browser.new_context(storage_state=SESSION_FILE)
    else:
        print("No session found, logging in...")
        context = await browser.new_context()
        page = await context.new_page()
        await login_and_save_session(page)

    page = await context.new_page()
    await page.goto(LOGIN_URL)
    return browser, context, page


async def navigate_to_products(page):
    """
    Navigate the hidden menu path to the product table.
    """
    print("📂 Navigating to product table...")

    # --- Replace these selectors with actual DOM from your app ---
    await page.click("#menuButton")
    await page.wait_for_selector("a[data-id='dataMgmt']")
    await page.click("a[data-id='dataMgmt']")

    await page.wait_for_selector("a[data-id='inventory']")
    await page.click("a[data-id='inventory']")

    await page.wait_for_selector("a[data-id='viewProducts']")
    await page.click("a[data-id='viewProducts']")

    # Wait until product table is visible
    await page.wait_for_selector(".product-table tbody tr")
    print("Product table loaded.")


async def scrape_products(page):
    """
    Scrape product table with pagination handling.
    Returns a list of structured records.
    """
    products = []
    page_num = 1

    while True:
        print(f"📄 Scraping page {page_num}...")
        await page.wait_for_selector(".product-table tbody tr")
        rows = await page.query_selector_all(".product-table tbody tr")

        for row in rows:
            cols = await row.query_selector_all("td")
            values = [await col.inner_text() for col in cols]

            if len(values) >= 8:
                record = {
                    "Item #": values[0],
                    "Cost": values[1],
                    "SKU": values[2],
                    "Details": values[3],
                    "Product": values[4],
                    "Dimensions": values[5],
                    "Weight": values[6],
                    "Type": values[7],
                }
                products.append(record)

        # Try to go to next page
        try:
            next_button = page.locator("button.next-page")  # update if needed
            if await next_button.is_enabled():
                await next_button.click()
                await page.wait_for_selector(".product-table tbody tr")
                page_num += 1
            else:
                break
        except Exception:
            break

    print(f"✅ Scraping complete. Collected {len(products)} records.")
    return products


async def save_to_json(data):
    """
    Save scraped product data into structured JSON file.
    """
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"💾 Data saved to {OUTPUT_FILE}")


async def main():
    try:
        async with async_playwright() as playwright:
            browser, context, page = await load_session(playwright)

            await navigate_to_products(page)
            product_data = await scrape_products(page)
            await save_to_json(product_data)

            await browser.close()
    except Exception as e:
        print(f"❌ Error occurred: {e}")


if __name__ == "__main__":
    asyncio.run(main())
