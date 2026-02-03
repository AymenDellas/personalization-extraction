
import urllib.request

def test_urllib():
    try:
        print("Testing google.com with urllib...")
        with urllib.request.urlopen("https://www.google.com", timeout=10) as response:
            print(f"Success: {response.status}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_urllib()
