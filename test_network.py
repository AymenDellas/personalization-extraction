
from playwright.sync_api import sync_playwright

def test_network():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            print("Testing google.com...")
            page.goto("https://www.google.com", timeout=10000)
            print("Successfully reached google.com")
            
            print("Testing linkedin.com...")
            page.goto("https://www.linkedin.com", timeout=10000)
            print("Successfully reached linkedin.com")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    test_network()
