# coding: utf-8
# This file is part of https://github.com/marcus67/gitsynchista

import six

import log
import config
import sync_config

if six.PY3:
	from importlib import reload
	
reload(log)
reload(config)
reload(sync_config)

global logger

logger = log.open_logging(__name__)

def test():
  global logger
  
  logger.info("Start test")
  config_handler = config.ConfigHandler(sync_config.SyncConfig())
  sample_config = config_handler.read_config_file('etc/sample_gitsynchista_config')
  sample_config.dump()
  logger.info("End test")
  
if __name__ == '__main__':
  test()
