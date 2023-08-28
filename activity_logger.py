import datetime
import logging
import os
import sqlite3
import subprocess

logging.basicConfig(filename=os.path.expanduser('~/Documents/app_activity_errors.log'), level=logging.ERROR)
db_path = os.path.expanduser('~/Documents/app_activity_db.sqlite')

conn = sqlite3.connect(db_path)
c = conn.cursor()

c.execute('''
          CREATE TABLE if not exists app_activity 
          (timestamp text, app text, url text, title text)
          ''')

ascript = '''
    tell application "System Events"
        set frontApp to name of first application process whose frontmost is true
    end tell
    
    return frontApp
'''


p = subprocess.Popen(['osascript', '-'],
                    stdin=subprocess.PIPE, 
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True)

out, err = p.communicate(ascript)

if err:
    logging.error(err)
elif out:
    app = out.strip()
    
    if app == "Google Chrome":
        ascript = '''
            tell application "Google Chrome"
                set active_tab_url to URL of active tab of first window
                set active_tab_title to title of active tab of first window
            end tell
            
            return active_tab_url & linefeed & active_tab_title
        '''
        
        p = subprocess.Popen(['osascript', '-'],
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE,
                        text=True)
        
        out, err = p.communicate(ascript)
        
        if err:
            logging.error(err) 
        elif out:
            url, title = out.strip().split('\n')
    else:
        url = ""
        title = ""
        
    timestamp = datetime.datetime.now()
    c.execute('INSERT INTO app_activity VALUES (?, ?, ?, ?)', (timestamp, app, url, title))
    conn.commit()