
import os
import json
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from scraper import scrape_linkedin_profile
from extractor import extract_profile_data
from website_scraper import scrape_generic_website
from website_extractor import extract_website_data

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='public')
CORS(app)

@app.route('/')
def index():
    return send_from_directory('public', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('public', path)

@app.route('/api/scrape', methods=['POST'])
def scrape():
    data = request.json
    url = data.get('url')
    
    if not url:
        return jsonify({"error": "URL is required"}), 400
        
    print(f"Received scrape request for: {url}")
    
    try:
        # Check for LI_AT cookie
        li_at = os.getenv("LI_AT")
        if not li_at:
            print("WARNING: LI_AT cookie missing")
            return jsonify({"error": "Configuration error: LinkedIn session cookie (LI_AT) missing from server environment."}), 500
            
        # Step 1: Scrape
        text = scrape_linkedin_profile(url, headless=True, li_at_cookie=li_at)
        
        if not text:
            return jsonify({"error": "Failed to scrape profile. Ensure the URL is correct and the server has access."}), 500
            
        # Step 2: Extract
        profile_data = extract_profile_data(text)
        
        if not profile_data:
             return jsonify({"error": "Failed to extract data from the scraped text."}), 500
             
        return jsonify(profile_data)
        
    except Exception as e:
        print(f"Server error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/scrape-website', methods=['POST'])
def scrape_website():
    data = request.json
    url = data.get('url')
    
    if not url:
        return jsonify({"error": "URL is required"}), 400
        
    print(f"Received website scrape request for: {url}")
    
    try:
        text = scrape_generic_website(url, headless=True)
        if not text:
            return jsonify({"error": "Failed to scrape website."}), 500
            
        # Extract data using AI
        site_data = extract_website_data(text)
        
        if not site_data:
             return jsonify({"error": "Failed to extract insights from website text."}), 500

        return jsonify(site_data)
        
    except Exception as e:
         import traceback
         traceback.print_exc()
         print(f"Website scrape error: {repr(e)}")
         return jsonify({"error": f"Server Error: {str(e)}"}), 500

if __name__ == '__main__':
    print("Starting Flask server on http://localhost:5000")
    app.run(debug=True, port=5000)
