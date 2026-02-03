
from playwright.sync_api import sync_playwright

def scrape_generic_website(url: str, headless: bool = True) -> str | None:
    """
    Opens a generic website and extracts the visible text from the body.
    """
    with sync_playwright() as p:
        # Use simple chromium launch
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )
        
        page = context.new_page()

        try:
            print(f"Navigating to {url}...")
            page.goto(url, timeout=30000)
            
            # Handle LinkedIn "Safety/External Link" Redirect
            try:
                # Wait for load
                page.wait_for_load_state("domcontentloaded")
                
                # Check for the specific warning header
                # Selector based on: <h1 class="...">This link will take you to a page that’s not on LinkedIn</h1>
                warning_header = page.locator("h1", has_text="not on LinkedIn")
                
                if warning_header.count() > 0 and warning_header.is_visible():
                    print("Detected LinkedIn redirect warning. Attempting to follow link...")
                    
                    # The actual link is usually the first link in <main>
                    redirect_btn = page.locator("main a").first
                    
                    if redirect_btn.is_visible():
                        actual_url = redirect_btn.get_attribute("href")
                        print(f"Found actual URL: {actual_url}")
                        
                        if actual_url:
                            page.goto(actual_url, timeout=30000)
                            page.wait_for_load_state("domcontentloaded")
                            
            except Exception as e:
                print(f"Redirect handling warning: {e}")

            # Helper: scroll minimal amount to trigger lazy elements
            page.mouse.wheel(0, 500)
            page.wait_for_timeout(1000)

            # Extract text
            content = page.locator("body").inner_text()
            return content

        except Exception as e:
            print(f"Website scrape error: {e}")
            return None
        finally:
            browser.close()
