
from website_scraper import scrape_generic_website

def test_fix():
    url = "https://lnkd.in/eiy7ahhn"
    print(f"Testing redirect fix for: {url}")
    
    content = scrape_generic_website(url, headless=True)
    
    if content:
        print("Success! Content length:", len(content))
        print("Snippet:", content[:200])
    else:
        print("Failed to scrape.")

if __name__ == "__main__":
    test_fix()
