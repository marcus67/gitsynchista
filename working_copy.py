# coding: utf-8
# This file is part of https://github.com/marcus67/gitsynchista

import webbrowser as wb
import urllib
import time
import keychain
import console
import six

import log
import util
import sync_config
import url_scheme_support

if six.PY3:
	from importlib import reload
	
reload(log)
reload(util)
reload(sync_config)
reload(url_scheme_support)

PARAM_IGNORE_WAKEUP = 'IGNORE_WAKEUP'

KEYCHAIN_SERVICE = 'Working Copy'
KEYCHAIN_ACCOUNT = 'X-URL-Callback'

global logger

logger = log.open_logging(__name__)

class WorkingCopySupport (url_scheme_support.UrlSchemeSupport):
  
  def __init__(self):
    super(WorkingCopySupport, self).__init__('working-copy')
    self.key = util.get_password_from_keychain(KEYCHAIN_SERVICE, KEYCHAIN_ACCOUNT)
    
  def wakeup_webdav_server(self):
    pythonista_url = 'pythonista' if six.PY2 else 'pythonista3'
    payload = { 'cmd' : 'start', 'x-success' : '%s://gitsynchista/gitsynchista?action=run&argv=%s' % (pythonista_url, PARAM_IGNORE_WAKEUP)}
    self._send_to_app(action='webdav', payload=payload, x_callback_enabled=True)
    #time.sleep(1)
    
  def open_repository(self, repository_config):
    payload = { 'repo' : repository_config.remote_path[1:]}
    self._send_to_app(action='open', payload=payload)    
    
def remove_key_from_chain():
	global logger
	
	logger.info("Removing password from keychain for service '%s' and account '%s'" % (KEYCHAIN_SERVICE, KEYCHAIN_ACCOUNT))
	util.keychain.delete_password(KEYCHAIN_SERVICE, KEYCHAIN_ACCOUNT)
	
if __name__ == '__main__':
	remove_key_from_chain()
	
