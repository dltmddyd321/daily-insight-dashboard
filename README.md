# Daily Insight Dashboard

AI-powered dashboard to extract and visualize insights from your emails (Naver Mail, etc.).

## Features
- **Email Fetching:** Automatically fetches latest emails via IMAP.
- **AI Analysis:** Uses Gemini AI to categorize and summarize emails.
- **Visual Dashboard:** Clean, modern UI to view your daily insights.

## Prerequisites
- Python 3.9+
- Gemini API Key

## Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/dltmddyd321/daily-insight-dashboard.git
   cd daily-insight-dashboard
   ```

2. **Configure Credentials:**
   Create a `config.json` file in the root directory with the following structure:
   ```json
   {
       "imap": {
           "server": "imap.naver.com",
           "port": 993,
           "email": "your-email@naver.com",
           "password": "your-app-password"
       },
       "gemini": {
           "api_key": "your-gemini-api-key",
           "model": "gemini-flash-latest"
       }
   }
   ```

3. **Run the Application:**
   ```bash
   python run.py
   ```
   This will install dependencies, fetch emails, and open the dashboard in your browser.

## Compatibility
Supported on Windows, macOS, and Linux.

## License
MIT
