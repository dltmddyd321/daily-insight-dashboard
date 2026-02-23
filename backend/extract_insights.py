import json
import os
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

def load_config():
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def extract_insights(emails):
    config = load_config()
    
    # Check for Gemini Config
    gemini_config = config.get('gemini', {})
    api_key = gemini_config.get('api_key')
    
    if not api_key or api_key == "YOUR_GEMINI_API_KEY":
        print("Warning: Gemini API Key not found. Skipping insight generation.")
        return emails 
        
    # Configure Gemini
    genai.configure(api_key=api_key)
    
    model_name = gemini_config.get('model', 'gemini-1.5-flash')
    model = genai.GenerativeModel(model_name)
    
    processed_emails = []

    for email_data in emails:
        print(f"Processing email with Gemini: {email_data['subject']}...")
        
        prompt = f"""
        You are a helpful assistant that summarizes newsletters into daily insights.
        Analyze the following email newsletter and extract the most important key insights in KOREAN (한국어). 
        Extract between 1 and 5 key insights, depending on how much meaningful content the email contains. Make them concise.
        
        Return the response in strictly valid JSON format with the following structure:
        {{
            "summary": "A one-sentence summary of the email in Korean.",
            "key_points": [
                "Key finding 1 in Korean",
                "Key finding 2 in Korean (if applicable)",
                "...up to 5 key findings maximum"
            ],
            "actionable_item": "One actionable takeaway if applicable in Korean, else null",
            "category": "Tech / Business / Design / General"
        }}

        Email Subject: {email_data['subject']}
        Email Sender: {email_data['sender']}
        Email Body (truncated):
        {email_data['body_text'][:3000]}
        """

        try:
            # Set safety settings to block nothing for newsletter content
            safety_settings = {
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            }

            response = model.generate_content(
                prompt, 
                generation_config={"response_mime_type": "application/json"},
                safety_settings=safety_settings
            )
            
            content = response.text
            insights = json.loads(content)
            
            # Merge insights into email data
            email_data.update(insights)
            processed_emails.append(email_data)
            
        except Exception as e:
            print(f"Error processing email {email_data['subject']}: {e}")
            # Inject error details into the summary so the user sees it in the dashboard
            email_data['summary'] = f"AI Analysis Failed: {str(e)}"
            email_data['key_points'] = ["Could not generate insights.", "Check your API Key.", "Check backend logs."]
            email_data['category'] = "Error"
            email_data['error'] = str(e)
            processed_emails.append(email_data)
            
    return processed_emails

if __name__ == "__main__":
    # Test with dummy data
    dummy_emails = [{
        "subject": "Test Email", 
        "sender": "test@example.com", 
        "body_text": "This is a test email about AI advances. Key point 1: AI is growing. Key point 2: Python is popular."
    }]
    print(json.dumps(extract_insights(dummy_emails), indent=2, ensure_ascii=False))
