import json
import os
import sys
from fetch_emails import fetch_emails
from extract_insights import extract_insights

def main():
    print("Starting Daily Insight Dashboard Backend...")
    
    # 1. Fetch Emails
    print("Fetching emails...")
    emails = fetch_emails()
    print(f"Fetched {len(emails)} emails.")
    
    if not emails:
        print("No emails found. Generating empty report.")
        # Save empty data to ensure frontend loads
        output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend')
        output_path = os.path.join(output_dir, 'data.js')
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("const DAILY_INSIGHTS = [];")
        return

    # 2. Extract Insights
    print("Extracting insights...")
    enriched_data = extract_insights(emails)
    
    # 3. Save Data as JS (to avoid CORS issues)
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend')
    output_path = os.path.join(output_dir, 'data.js')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json_content = json.dumps(enriched_data, indent=4, ensure_ascii=False)
        f.write(f"const DAILY_INSIGHTS = {json_content};")
        
    print(f"Successfully saved {len(enriched_data)} insights to {output_path}")

if __name__ == "__main__":
    main()
