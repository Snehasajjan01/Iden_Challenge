import json
import os
import time
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeoutError

SESSION_FILE = "session.json"
PRODUCTS_FILE = "products.json"

EMAIL = "sneha.g.s@campusuvce.in"
PASSWORD = "8D2g2xCT"
APP_URL = "https://hiring.idenhq.com/"

HEADERS = [
    "item_#", "cost", "sku", "details", "product",
    "dimensions", "weight_(kg)", "type"
]

# -------------------------
# Save session state
# -------------------------
def save_session(context):
    context.storage_state(path=SESSION_FILE)
    print(f"✅ Session saved to {SESSION_FILE}")

# -------------------------
# Load session or login
# -------------------------
def get_page_with_session(p):
    browser = p.chromium.launch(headless=False)
    context = None

    if os.path.exists(SESSION_FILE):
        print("✅ Using existing session")
        context = browser.new_context(storage_state=SESSION_FILE)
    else:
        print("❌ No session found, logging in...")
        context = browser.new_context()

    page = context.new_page()
    page.goto(APP_URL)
    page.wait_for_load_state("domcontentloaded")

    if not os.path.exists(SESSION_FILE):
        login(page)
        save_session(context)

    return page, context, browser

# -------------------------
# Login function
# -------------------------
def login(page):
    try:
        page.locator("input[type='email']").wait_for(state="visible", timeout=10000)
        page.fill("input[type='email']", EMAIL)
        page.locator("input[type='password']").wait_for(state="visible", timeout=10000)
        page.fill("input[type='password']", PASSWORD)
        page.locator("button:has-text('Login')").nth(0).click()
        page.wait_for_selector("text=Menu", timeout=15000)
        print("✅ Login successful")
    except PWTimeoutError:
        raise RuntimeError("❌ Login failed. Check credentials or selectors.")

# -------------------------
# Navigate to product table
# -------------------------
def navigate_to_products(page):
    page.locator("text=Menu").nth(0).click()
    page.wait_for_timeout(1000)
    page.locator("text=Data Management").nth(0).click()
    page.wait_for_timeout(1000)
    page.locator("text=Inventory").nth(0).click()
    page.wait_for_timeout(1000)
    page.locator("text=View All Products").nth(0).click()
    page.wait_for_timeout(3000)
    page.wait_for_selector("table, div[role='table']", timeout=15000)
    page.screenshot(path="after_navigation.png")
    print("📸 Screenshot saved as after_navigation.png")
    print("✅ Reached product table")

# -------------------------
# Load existing products
# -------------------------
def load_existing_products(filename=PRODUCTS_FILE):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            products = json.load(f)
            print(f"✅ Loaded {len(products)} existing products")
            return products
    return []

# -------------------------
# Save products to JSON
# -------------------------
def save_products_to_json(products, filename=PRODUCTS_FILE):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=4, ensure_ascii=False)
    print(f"✅ Saved {len(products)} products to {filename}")

# -------------------------
# Robust scraper with progress display
# -------------------------
def scrape_products(page, existing_products):
    products = existing_products.copy()
    seen_skus = set(p["sku"] for p in products)
    table_body = page.locator("table tbody")
    table_body.locator("tr").first.wait_for(state="visible", timeout=10000)

    MAX_RETRIES = 3
    scroll_pause = 0.3
    page_num = 1

    while True:
        rows = table_body.locator("tr")
        total_rows = rows.count()
        any_new = False

        for i in range(total_rows):
            for attempt in range(MAX_RETRIES):
                try:
                    row = rows.nth(i)
                    cells = [cell.inner_text().strip() for cell in row.locator("td").all()]
                    if len(cells) != len(HEADERS):
                        raise ValueError("Incomplete row")
                    row_dict = dict(zip(HEADERS, cells))

                    if row_dict["sku"] not in seen_skus:
                        seen_skus.add(row_dict["sku"])
                        products.append(row_dict)
                        any_new = True

                    # Dynamic one-line progress
                    print(f"\r➡️ Page {page_num} | Row {i+1}/{total_rows} | Total products: {len(products)}", end="", flush=True)

                    if len(products) % 100 == 0:
                        save_products_to_json(products)

                    break
                except Exception:
                    time.sleep(scroll_pause)
                    table_handle = table_body.element_handle()
                    if table_handle:
                        page.evaluate("table => table.scrollTop += 50", table_handle)
                    if attempt == MAX_RETRIES - 1:
                        print(f"\n⚠️ Skipped row {i+1} after {MAX_RETRIES} attempts")

        # Scroll to bottom for lazy-loading
        table_handle = table_body.element_handle()
        if table_handle:
            prev_height = -1
            while True:
                scroll_height = page.evaluate("table => table.scrollHeight", table_handle)
                if scroll_height == prev_height:
                    break
                prev_height = scroll_height
                page.evaluate("table => table.scrollTop = table.scrollHeight", table_handle)
                time.sleep(scroll_pause)
                rows = table_body.locator("tr")
                total_rows = rows.count()

        # Pagination handling
        next_btn = page.locator("button:has-text('Next')").first
        if next_btn.count() > 0 and next_btn.get_attribute("aria-disabled") != "true":
            next_btn.click()
            page.wait_for_timeout(1500)
            table_body.locator("tr").first.wait_for(state="visible", timeout=10000)
            page_num += 1
        else:
            break

        if not any_new:
            break

    print(f"\n✅ Scraped {len(products)} products in total")
    return products

# -------------------------
# MAIN
# -------------------------
def main():
    try:
        with sync_playwright() as p:
            page, context, browser = get_page_with_session(p)
            navigate_to_products(page)
            existing_products = load_existing_products()
            products = scrape_products(page, existing_products)
            save_products_to_json(products)
            browser.close()
    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    main()
