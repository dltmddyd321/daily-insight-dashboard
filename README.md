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

### 2. Configure Credentials

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
    },
    "preferences": {
        "vip_mode": "folder",
        "vip_folder_name": "VIP_In",
        "max_emails_per_day": 10
    }
}
```

> [!IMPORTANT]
> **Naver 2-Step Verification (2FA):**
> If you have 2-step verification enabled, your regular password will not work. You **must** generate and use an **App Password**:
> 1. Go to [Naver Security Settings](https://nid.naver.com/user2/help/myInfo?m=viewSecurity).
> 2. Select **2-Step Verification** > **Generate App Password**.
> 3. Choose 'Other' for the device and copy the 12-character password into `config.json`.

> [!TIP]
> **Naver Mail Configuration:**
> 1. **Enable IMAP:** In Naver Mail, go to **Settings** > **POP3/IMAP Settings** and set IMAP to **Enable**.
> 2. **Categorization:** By default, this tool fetches from your inbox. If you want to process specific newsletters or important mails:
>    - Create a folder (e.g., `VIP_In`) in Naver Mail.
>    - Set up a **Mail Filter** in Naver Mail Settings to automatically move specific senders to that folder.
>    - In `config.json`, set `"vip_mode": "folder"` and `"vip_folder_name": "YourFolderName"`.

### 3. Run the Application
   ```bash
   python run.py
   ```
   This will install dependencies, fetch emails, and open the dashboard in your browser.

## Compatibility
Supported on Windows, macOS, and Linux.

## License
MIT
