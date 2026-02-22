import imaplib
import email
import json
import os

def load_config():
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def inspect_headers():
    config = load_config()
    imap_config = config['imap']
    
    try:
        mail = imaplib.IMAP4_SSL(imap_config['server'], imap_config['port'])
        mail.login(imap_config['email'], imap_config['password'])
        
        print("--- Folders ---")
        status, folders = mail.list()
        for f in folders:
            print(f.decode('utf-8'))

        folder = "INBOX"
        mail.select(folder)
        
        # Use UID instead of sequence numbers
        status, response = mail.uid('search', None, 'ALL')
        uids = response[0].split()
        
        if not uids:
            print("No emails found.")
            return

        # Fetch last email headers and UID
        latest_uid = uids[-1]
        status, data = mail.uid('fetch', latest_uid, '(RFC822.HEADER)')
        
        print(f"\n--- UID for last email: {latest_uid.decode('utf-8')} ---")
        
        for response_part in data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                print(f"Subject: {msg['Subject']}")
                print(f"Message-ID: {msg['Message-ID']}")
                
        mail.logout()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    inspect_headers()
