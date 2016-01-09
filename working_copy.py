import webbrowser as wb
import urllib
import time
import keychain
import console

import log
import sync_config

reload(log)
reload(sync_config)

global logger

logger = log.open_logging()

class WorkingCopySupport (object):
  
  def __init__(self, webdav_config):
    
    self.webdav_config = webdav_config
    self.key = self._get_key()
    
  def _get_key(self):
    ''' Retrieve the working copy key or prompt for a new one. See https://github.com/ahenry91/wc_sync
    '''
  
    key = keychain.get_password('wcSync', 'xcallback')
    if not key:
      key = console.password_alert('Working Copy Key')
      keychain.set_password('wcSync', 'xcallback', key)
    return key  
  
  def _send_to_working_copy(self, action, payload, x_callback_enabled=True):
    
    # see https://github.com/ahenry91/wc_sync
    
    global logger
    
    x_callback = 'x-callback-url/' if x_callback_enabled else ''
    payload['key'] = self.key
    payload = urllib.urlencode(payload).replace('+', '%20')
    fmt = 'working-copy://{x_callback}{action}/?{payload}'
    url = fmt.format(x_callback=x_callback, action=action, payload=payload)
    
    logger.info("Issuing callback '%s'" % url)
    
    wb.open(url)  
    
  def wakeup_webdav_server(self):
    
    payload = { 'cmd' : 'start',
                'x-success' : 'pythonista:///' }
    self._send_to_working_copy(action='webdav', payload=payload)
    time.sleep(1)
    
