
from playwright.sync_api import sync_playwright

def test_edge():
    with sync_playwright() as p:
        try:
            print("Launching Edge...")
            # Try to launch msedge. If not installed, this will fail.
            browser = p.chromium.launch(channel="msedge", headless=True)
            page = browser.new_page()
            
            print("Testing google.com with Edge...")
            page.goto("https://www.google.com", timeout=10000)
            print("Success!")
            
            browser.close()
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_edge()
