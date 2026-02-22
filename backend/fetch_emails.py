import imaplib
import email
from email.header import decode_header
import json
import datetime
import os
from bs4 import BeautifulSoup
import chardet

def load_config():
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def clean_text(text):
    if not text:
        return ""
    return " ".join(text.split())

def get_email_body(msg):
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            try:
                payload = part.get_payload(decode=True)
                if payload:
                    charset = part.get_content_charset()
                    if not charset:
                        charset = chardet.detect(payload)['encoding']
                    if not charset: 
                        charset = 'utf-8' # fallback
                    decoded_payload = payload.decode(charset, errors="replace")
                    
                    if content_type == "text/plain" and "attachment" not in content_disposition:
                        body += decoded_payload
                    elif content_type == "text/html" and "attachment" not in content_disposition:
                        soup = BeautifulSoup(decoded_payload, "html.parser")
                        body += soup.get_text()
            except Exception as e:
                print(f"Error decoding part: {e}")
    else:
        content_type = msg.get_content_type()
        payload = msg.get_payload(decode=True)
        if payload:
            charset = msg.get_content_charset()
            if not charset:
                charset = chardet.detect(payload)['encoding']
            if not charset: 
                charset = 'utf-8'
            decoded_payload = payload.decode(charset, errors="replace")
            
            if content_type == "text/plain":
                body = decoded_payload
            elif content_type == "text/html":
                soup = BeautifulSoup(decoded_payload, "html.parser")
                body = soup.get_text()
    return clean_text(body)

def fetch_emails(target_date=None):
    config = load_config()
    imap_config = config['imap']
    pref_config = config['preferences']

    if target_date is None:
        target_date = datetime.date.today()
    elif isinstance(target_date, str):
        target_date = datetime.date.fromisoformat(target_date)

    try:
        # Connect to IMAP
        mail = imaplib.IMAP4_SSL(imap_config['server'], imap_config['port'])
        mail.login(imap_config['email'], imap_config['password'])
        
        # Select folder
        folder = "INBOX"
        if pref_config.get('vip_mode') == 'folder':
            folder = pref_config.get('vip_folder_name', 'INBOX')
        
        status, messages = mail.select(folder)
        if status != 'OK':
            print(f"Failed to select folder: {folder}")
            return []

        # Search for emails on the target date
        # IMAP "SINCE" is inclusive, "BEFORE" is exclusive
        date_since = target_date.strftime("%d-%b-%Y")
        date_before = (target_date + datetime.timedelta(days=1)).strftime("%d-%b-%Y")
        
        search_criteria = f'(SINCE "{date_since}" BEFORE "{date_before}")'
        status, response = mail.search(None, search_criteria)
        
        email_ids = response[0].split()
        emails_data = []
        
        count = 0
        vip_senders = [s.lower() for s in pref_config.get('vip_senders', [])]
        max_emails = pref_config.get('max_emails_per_day', 10)

        for e_id in reversed(email_ids):
            if count >= max_emails:
                break
                
            status, data = mail.fetch(e_id, '(RFC822)')
            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    
                    # Helper function for robust decoding
                    def decode_mime_str(header_val):
                        if not header_val:
                            return ""
                        decoded_parts = decode_header(header_val)
                        result = ""
                        for content, encoding in decoded_parts:
                            if isinstance(content, bytes):
                                try:
                                    result += content.decode(encoding if encoding else "utf-8", errors="replace")
                                except LookupError:
                                    result += content.decode("utf-8", errors="replace")
                            else:
                                result += str(content)
                        return result

                    # Decode Subject and Sender
                    subject = decode_mime_str(msg["Subject"])
                    from_header = msg.get("From")
                    # Parse address first to separate name and email
                    sender_name, sender_email = email.utils.parseaddr(from_header)
                    
                    # Decode the name part if it's encoded
                    if "=?" in sender_name:
                        sender_name = decode_mime_str(sender_name)
                    
                    # If name is empty, use email part
                    if not sender_name:
                        sender_name = sender_email

                    # Filter by VIP Sender if mode is 'sender_list'
                    if pref_config.get('vip_mode') == 'sender_list':
                        is_vip = False
                        for vip in vip_senders:
                            if vip in sender_email.lower() or vip in sender_name.lower():
                                is_vip = True
                                break
                        if not is_vip:
                            continue

                    body = get_email_body(msg)
                    
                    emails_data.append({
                        "id": str(e_id, 'utf-8'),
                        "subject": subject,
                        "sender": sender_name,
                        "email_address": sender_email,
                        "date": msg.get("Date"),
                        "body_text": body[:10000] # Increased limit for better context
                    })
                    count += 1
                    
        mail.logout()
        return emails_data

    except Exception as e:
        print(f"An error occurred: {e}")
        return []

if __name__ == "__main__":
    emails = fetch_emails()
    print(json.dumps(emails, indent=4, ensure_ascii=False))
