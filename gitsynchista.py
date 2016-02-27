# coding: utf-8
# This file is part of https://github.com/marcus67/gitsynchista

import platform
import sys
import os

import log
import config
import sync_config
import sync
import sync_selector
import working_copy

py_majversion, py_minversion, py_revversion = platform.python_version_tuple()

if py_majversion == '3':
	from importlib import reload	
	
reload(log)
reload(config)
reload(sync_config)
reload(sync)
reload(sync_selector)
reload(working_copy)

#Use this switch to temporarily disable support for app "working copy"
ENABLE_WORKING_COPY_SUPPORT = False

def load_config_file_and_sync(config_filename):
  global logger
  
  config_handler = config.ConfigHandler(sync_config.SyncConfig())
  tool_sync_config = config_handler.read_config_file(config_filename)
  
  sync_tool = sync.SyncTool(tool_sync_config)
  
  try:
    sync_tool.scan()
    
  except Exception as e:
    logger.exception("Exception during scan: %s" % str(e))
    return
  
  try:
    sync_tool.sync()
    
  except Exception as e:
    logger.exception("Exception during sync: %s" % str(e))
  
def wakeup_webdav_server(config):
  
    working_copy_support = working_copy.WorkingCopySupport()
    working_copy_support.wakeup_webdav_server()

def start_gui(check_wakeup):
  
  global logger
  
  if check_wakeup:
  	logger.info("Checking if wakeup is required...")
  sync_tools = []
  configs = sync.find_sync_configs()
  working_copy_configs = []
  working_copy_configs.extend(filter(lambda config:config.repository.working_copy_wakeup, configs))
  working_copy_active = ENABLE_WORKING_COPY_SUPPORT and len(working_copy_configs) > 0
  
  if working_copy_active and check_wakeup:
    wakeup_webdav_server(working_copy_configs[0])
    logger.info("Exiting to await callback from Working Copy...")
    return 
    
  logger.info("Starting GUI...")
  
  for config in configs:
    logger.info("Found configuration '%s'..." % config.repository.name)
    
    try:
      sync_tool = sync.SyncTool(config)
      sync_tools.append(sync_tool)
      
    except Exception as e:
      logger.error("Error '%s' while processing configuration '%s'" % ( str(e), config.repository.name) )
    
  selector = sync_selector.SyncSelector()
  selector.select(sync_tools, working_copy_active=working_copy_active)
  
def main():
  global logger
  logger = log.open_logging('gitsynchista', True)
  logger.info('Starting gitsynchista')
  
  if len(sys.argv) == 2:  
    if (sys.argv[1].startswith(working_copy.PARAM_IGNORE_WAKEUP)):
      start_gui(False)
      
    else:
      load_config_file_and_sync(sys.argv[1])
      
  else:
    start_gui(ENABLE_WORKING_COPY_SUPPORT)
    
  logger.info('Terminating gitsynchista')
  
if __name__ == '__main__':
  main()
  
