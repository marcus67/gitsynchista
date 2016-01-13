import sys
import os

import log
import config
import sync_config
import sync
import sync_selector
import working_copy

reload(log)
reload(config)
reload(sync_config)
reload(sync)
reload(sync_selector)
reload(working_copy)
  

def load_config_file_and_sync(config_filename):
  
  global logger
  
  config_handler = config.ConfigHandler(sync_config.SyncConfig())
  tool_sync_config = config_handler.read_config_file(config_filename)
  
  sync_tool = sync.SyncTool(tool_sync_config)
  
  try:
    
    sync_tool.scan()
    
  except Exception as e:
    
    logger.exception("Exception %s during scan" % str(e))
    return
  
  try:
    
    sync_tool.sync()
    
  except Exception as e:
    
    logger.exception("Exception %s during sync" % str(e))
  
def wakeup_webdav_server(webdav_config):
  
    working_copy_support = working_copy.WorkingCopySupport(webdav_config)
    working_copy_support.wakeup_webdav_server()

def start_gui(check_wakeup):
  
  global logger
  
  sync_tools = []
  configs = sync.find_sync_configs()
  working_copy_configs = filter(lambda config:config.repository.working_copy_wakeup, configs)
  
  if len(working_copy_configs) > 0 and check_wakeup:
    wakeup_webdav_server(working_copy_configs[0].webdav)
    logger.info("Exiting to await callback from Working Copy...")
    return 
    
  logger.info("Starting GUI...")
  for config in configs:
    
    logger.info("Found configuration '%s'..." % config.repository.name)
    
    try:
      
      sync_tool = sync.SyncTool(config)
      #sync_tool.scan()
      sync_tools.append(sync_tool)
      
    except Exception as e:
      
      logger.info("Error '%s' while processing configuration '%s'" % ( str(e), config.repository.name) )
    
  selector = sync_selector.SyncSelector()
  
  selector.select(sync_tools)
  
def main():
  
  global logger
  
  logger = log.open_logging()
  
  logger.info('Starting gitsynchista')
  if len(sys.argv) == 2:  
    if (sys.argv[1].startswith(working_copy.PARAM_IGNORE_WAKEUP)):
      start_gui(False)
    else:
      load_config_file_and_sync(sys.argv[1])
  else:
    start_gui(True)
  logger.info('Terminating gitsynchista')
  
if __name__ == '__main__':
  main()
  