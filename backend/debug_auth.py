import imaplib
import json
import os

def check_auth():
    print("--- Naver IMAP Debug Tool ---")
    
    # Load Config
    try:
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except Exception as e:
        print(f"[ERROR] Could not load config.json: {e}")
        return

    email = config['imap']['email']
    password = config['imap']['password']
    server = config['imap']['server']
    port = config['imap']['port']

    print(f"Target: {server}:{port}")
    print(f"Email: {email}")
    print(f"Password: {password[:2]}******{password[-2:]} (Length: {len(password)})")
    
    try:
        print("\n1. Connecting to server...")
        mail = imaplib.IMAP4_SSL(server, port)
        print("   -> Connection successful.")
        
        print("\n2. Attempting login...")
        mail.login(email, password)
        print("   -> Login successful! (Credentials are correct)")
        
        print("\n3. Listing folders...")
        status, folders = mail.list()
        if status == 'OK':
            print("   -> Found folders:")
            vip_folder_exists = False
            for folder in folders:
                decoded = folder.decode('utf-8')
                print(f"      - {decoded}")
                if "VIP_In" in decoded or "VIP_In" in decoded.replace('"', ''):
                    vip_folder_exists = True
            
            if vip_folder_exists:
                print("\n   [OK] 'VIP_In' folder found.")
            else:
                print("\n   [WARNING] 'VIP_In' folder NOT found. Please check folder name in Naver Mail.")
        else:
            print("   -> Failed to list folders.")
            
        mail.logout()
        
    except imaplib.IMAP4.error as e:
        print(f"\n[LOGIN FAILED] {e}")
        print("Possible causes:")
        print("1. IMAP is disabled in Naver Mail settings (Settings > IMAP/POP3).")
        print("2. Password is incorrect.")
        print("   - If 2-Step Verification is ON: You MUST use an 'App Password'.")
        print("   - If 2-Step Verification is OFF: Use your main Naver password.")
    except Exception as e:
        print(f"\n[ERROR] {e}")

if __name__ == "__main__":
    check_auth()
