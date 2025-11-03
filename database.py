import sqlite3
import hashlib
from pathlib import Path
from cryptography.fernet import Fernet
import os
import uuid
import requests

# ✅ RENDER COMPATIBLE PATHS
BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / 'users.db'
ENCRYPTION_KEY_FILE = BASE_DIR / '.encryption_key'

# GitHub Approval Configuration
GITHUB_APPROVAL_URL = "https://raw.githubusercontent.com/f4h4dusk/Approvel/main/approval.txt"

def get_encryption_key():
    """Get or create encryption key for cookie storage"""
    try:
        if ENCRYPTION_KEY_FILE.exists():
            with open(ENCRYPTION_KEY_FILE, 'rb') as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(ENCRYPTION_KEY_FILE, 'wb') as f:
                f.write(key)
            return key
    except Exception as e:
        # ✅ RENDER FALLBACK: Use environment variable for encryption key
        env_key = os.environ.get('ENCRYPTION_KEY')
        if env_key:
            return env_key.encode()
        else:
            # ✅ Generate deterministic key for Render
            return Fernet.generate_key()

ENCRYPTION_KEY = get_encryption_key()
cipher_suite = Fernet(ENCRYPTION_KEY)

def check_github_approval(user_key):
    """Check if user key is approved via GitHub"""
    try:
        response = requests.get(GITHUB_APPROVAL_URL, timeout=10)
        if response.status_code == 200:
            approved_keys = response.text.split('\n')
            approved_keys = [key.strip().upper() for key in approved_keys if key.strip()]
            return user_key.upper() in approved_keys
        return False
    except:
        return False

def get_db_connection():
    """Get database connection with error handling"""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        raise

def init_db():
    """Initialize database with tables"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                user_key TEXT UNIQUE,
                approved INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_configs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                chat_id TEXT,
                name_prefix TEXT,
                delay INTEGER DEFAULT 30,
                cookies_encrypted TEXT,
                messages TEXT,
                automation_running INTEGER DEFAULT 0,
                message_count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        conn.commit()
        print("✅ Database initialized successfully!")
        
    except Exception as e:
        print(f"❌ Database initialization error: {e}")
        conn.rollback()
    finally:
        conn.close()

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def encrypt_cookies(cookies):
    """Encrypt cookies for secure storage"""
    if not cookies:
        return None
    try:
        return cipher_suite.encrypt(cookies.encode()).decode()
    except Exception:
        return cookies

def decrypt_cookies(encrypted_cookies):
    """Decrypt cookies"""
    if not encrypted_cookies:
        return ""
    try:
        return cipher_suite.decrypt(encrypted_cookies.encode()).decode()
    except Exception:
        return encrypted_cookies

def save_user_key(user_key):
    """Save user key to database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Check if user key already exists
        cursor.execute('SELECT id FROM users WHERE user_key = ?', (user_key,))
        existing_user = cursor.fetchone()
        
        if not existing_user:
            # Create a new user with this key
            cursor.execute('''
                INSERT INTO users (username, password_hash, user_key, approved)
                VALUES (?, ?, ?, ?)
            ''', (f'user_{user_key}', '', user_key, 0))
            
            user_id = cursor.lastrowid
            
            # Create config for this user
            cursor.execute('''
                INSERT INTO user_configs (user_id, chat_id, name_prefix, delay, messages)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, '', '', 30, ''))
        
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"Save user key error: {e}")
        return False
    finally:
        conn.close()

def is_user_approved(user_key):
    """Check if user key is approved via GitHub"""
    return check_github_approval(user_key)

def create_user(username, password):
    """Create new user"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        password_hash = hash_password(password)
        user_key = str(uuid.uuid4())[:12].upper()
        
        cursor.execute('INSERT INTO users (username, password_hash, user_key, approved) VALUES (?, ?, ?, ?)', 
                      (username, password_hash, user_key, 1))
        
        user_id = cursor.lastrowid
        
        cursor.execute('''
            INSERT INTO user_configs (user_id, chat_id, name_prefix, delay, messages)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, '', '', 30, ''))
        
        conn.commit()
        return True, "Account created successfully!"
    except sqlite3.IntegrityError:
        return False, "Username already exists!"
    except Exception as e:
        conn.rollback()
        return False, f"Error: {str(e)}"
    finally:
        conn.close()

def verify_user(username, password):
    """Verify user credentials using SHA-256"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('SELECT id, password_hash FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        
        if user and user['password_hash'] == hash_password(password):
            return user['id']
        return None
    except Exception as e:
        print(f"Verify user error: {e}")
        return None
    finally:
        conn.close()

def get_user_config(user_id):
    """Get user configuration"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            SELECT chat_id, name_prefix, delay, cookies_encrypted, messages, automation_running, message_count
            FROM user_configs WHERE user_id = ?
        ''', (user_id,))
        
        config = cursor.fetchone()
        
        if config:
            return {
                'chat_id': config['chat_id'] or '',
                'name_prefix': config['name_prefix'] or '',
                'delay': config['delay'] or 30,
                'cookies': decrypt_cookies(config['cookies_encrypted']),
                'messages': config['messages'] or '',
                'automation_running': config['automation_running'] or 0,
                'message_count': config['message_count'] or 0
            }
        return None
    except Exception as e:
        print(f"Get user config error: {e}")
        return None
    finally:
        conn.close()

def update_user_config(user_id, chat_id, name_prefix, delay, cookies, messages):
    """Update user configuration"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        encrypted_cookies = encrypt_cookies(cookies)
        
        cursor.execute('''
            UPDATE user_configs 
            SET chat_id = ?, name_prefix = ?, delay = ?, cookies_encrypted = ?, 
                messages = ?, updated_at = CURRENT_TIMESTAMP
            WHERE user_id = ?
        ''', (chat_id, name_prefix, delay, encrypted_cookies, messages, user_id))
        
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"Update user config error: {e}")
        return False
    finally:
        conn.close()

def get_username(user_id):
    """Get username by user ID"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('SELECT username FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        return user['username'] if user else None
    except Exception as e:
        print(f"Get username error: {e}")
        return None
    finally:
        conn.close()

def set_automation_running(user_id, is_running):
    """Set automation running state for a user"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            UPDATE user_configs 
            SET automation_running = ?, updated_at = CURRENT_TIMESTAMP
            WHERE user_id = ?
        ''', (1 if is_running else 0, user_id))
        
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"Set automation running error: {e}")
        return False
    finally:
        conn.close()

def get_automation_running(user_id):
    """Get automation running state for a user"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('SELECT automation_running FROM user_configs WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        return bool(result['automation_running']) if result else False
    except Exception as e:
        print(f"Get automation running error: {e}")
        return False
    finally:
        conn.close()

def set_admin_e2ee_thread_id(user_id, thread_id, cookies=None, chat_type='REGULAR'):
    """Set admin E2EE thread ID for notifications"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        encrypted_cookies = encrypt_cookies(cookies) if cookies else None
        
        cursor.execute('''
            UPDATE user_configs 
            SET admin_e2ee_thread_id = ?, admin_cookies = ?, chat_type = ?, updated_at = CURRENT_TIMESTAMP
            WHERE user_id = ?
        ''', (thread_id, encrypted_cookies, chat_type, user_id))
        
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"Set admin thread ID error: {e}")
        return False
    finally:
        conn.close()

def get_admin_e2ee_thread_id(user_id):
    """Get admin E2EE thread ID for notifications"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('SELECT admin_e2ee_thread_id FROM user_configs WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        return result['admin_e2ee_thread_id'] if result and result['admin_e2ee_thread_id'] else None
    except Exception as e:
        print(f"Get admin thread ID error: {e}")
        return None
    finally:
        conn.close()

def clear_admin_e2ee_thread_id(user_id):
    """Clear admin E2EE thread ID"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            UPDATE user_configs 
            SET admin_e2ee_thread_id = NULL, admin_cookies = NULL, updated_at = CURRENT_TIMESTAMP
            WHERE user_id = ?
        ''', (user_id,))
        
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"Clear admin thread ID error: {e}")
        return False
    finally:
        conn.close()

def update_message_count(user_id, count):
    """Update message count for a user"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            UPDATE user_configs 
            SET message_count = ?, updated_at = CURRENT_TIMESTAMP
            WHERE user_id = ?
        ''', (count, user_id))
        
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"Update message count error: {e}")
        return False
    finally:
        conn.close()

# ✅ Initialize database when module loads
init_db()
