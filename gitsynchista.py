import sys
import os

import log
import config
import sync_config
import sync
import sync_selector

reload(log)
reload(config)
reload(sync_config)
reload(sync)
reload(sync_selector)
  
def load_config_file_and_sync(config_filename):
  
  global logger
  
  config_handler = config.ConfigHandler(sync_config.SyncConfig())
  tool_sync_config = config_handler.read_config_file(config_filename)
  
  sync_tool = sync.SyncTool(tool_sync_config)
  
  try:
    
    sync_tool.scan()
    
  except Exception as e:
    
    logger.error("Exception %s during scan" % str(e))
    return
  
  try:
    
    sync_tool.sync()
    
  except Exception as e:
    
    logger.error("Exception %s during sync" % str(e))
  

def start_gui():
  
  global logger
  
  sync_tools = []
  logger.info("Starting GUI...")
  configs = sync.find_sync_configs()
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
  
  if len(sys.argv) == 2:  
    load_config_file_and_sync(sys.argv[1])
  else:
    start_gui()
  
if __name__ == '__main__':
  main()
  
