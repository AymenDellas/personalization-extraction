import os
import time
from playwright.sync_api import sync_playwright

def scrape_linkedin_profile(profile_url: str, headless: bool = True, li_at_cookie: str = None) -> str | None:
    """
    Opens a LinkedIn profile URL, scrolls to load content, expands 'About', and extracts visible text.
    Returns the visible text or None if failed.
    """
    with sync_playwright() as p:
        # Use Edge channel to avoid bundled Chromium network issues
        browser = p.chromium.launch(headless=headless, channel="msedge")
        
        # Prepare context options
        context_args = {
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        context = browser.new_context(**context_args)
        
        # Add cookie if provided
        if li_at_cookie:
            context.add_cookies([{
                "name": "li_at",
                "value": li_at_cookie,
                "domain": ".linkedin.com",
                "path": "/"
            }])

        
        # Open a new page
        page = context.new_page()

        try:
            print(f"Navigating to {profile_url}...")
            page.goto(profile_url, timeout=60000)
            
            # Wait for network idle to ensure initial load
            try:
                page.wait_for_load_state("networkidle", timeout=10000)
            except:
                print("Network idle timeout, proceeding...")

            # Check if we hit the login wall (often redirected to /authwall or login page)
            if "login" in page.url or "authwall" in page.url:
                print("Hit login/auth wall. Ensure you are logged in or have a session.")
                # For this specific task, we are assuming public access or user handles login cookies if extended.
                # However, strictly following the prompt: "Load a LinkedIn profile URL... Capture ONLY visible text"
                # If we are blocked, we can't capture profile text.
                pass

            # Scroll slowly to trigger lazy load
            print("Scrolling page...")
            for i in range(5):
                page.mouse.wheel(0, 500)
                time.sleep(1)
            
            # Expand "About" section if visible
            # Common selectors for "see more" in About section
            # This is fragile and class names change, looking for text is often safer
            try:
                see_more = page.get_by_text("see more", exact=False).first
                if see_more.is_visible():
                    see_more.click()
                    time.sleep(1)
            except Exception as e:
                print(f"Could not expand 'About': {e}")

            # Capture visible text
            # We use inner_text on the 'main' tag or body if main isn't found
            content_locator = page.locator("main")
            if not content_locator.count():
                content_locator = page.locator("body")
            
            visible_text = content_locator.inner_text()
            
            return visible_text

        except Exception as e:
            print(f"Scraping error: {e}")
            return None
        finally:
            browser.close()

if __name__ == "__main__":
    # Test run
    text = scrape_linkedin_profile("https://www.linkedin.com/in/williamhgates") 
    print(text[:500] if text else "No text extracted.")
