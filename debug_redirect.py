
from playwright.sync_api import sync_playwright

def inspect_redirect(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            print(f"Navigating to {url}...")
            page.goto(url)
            page.wait_for_load_state("networkidle")
            
            title = page.title()
            print(f"Page Title: {title}")
            
            # Save HTML to file for inspection
            with open("redirect_page.html", "w", encoding="utf-8") as f:
                f.write(page.content())
            print("Saved page content to redirect_page.html")
            
        except Exception as e:
            print(f"Error: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    inspect_redirect("https://lnkd.in/eiy7ahhn")
