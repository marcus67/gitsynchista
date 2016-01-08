import ui

import ui_util
import log

reload(ui_util)
reload(log)

global logger

logger = log.open_logging()

class SyncSelector(ui_util.ViewController):
  
  def __init__(self, parent_vc=None):
    
    super(SyncSelector, self).__init__(parent_vc)
    self.selected_index = None
    self.popup_vc = None
    self.load('sync_selector')
         
  def get_selected_mode(self):
    
    if self.selected_index == None:
      return None
      
    else:
      return self.modes[self.selected_index]

  def is_my_action(self, sender):
    
    return sender == self
    
  def select(self, sync_tools, style = 'sheet'):

    global logger

    self.sync_tools = sync_tools        

    self.tableview_sync_selector = self.find_subview_by_name('tableview_sync_selector')
    self.button_scan = self.find_subview_by_name('button_scan')
    self.button_sync = self.find_subview_by_name('button_sync')

    self.selected_index = None
    self.list_data_source = ui.ListDataSource([])

    self.update_tool_states()
    self.update_view_states()
    
    self.present(style)
    
    if not self.parent_view:
      self.view.wait_modal()
    
    
  def update_tool_states(self):
    
    global logger
    
    logger.info("update_tool_states: selected_index=%s" % str(self.selected_index))
    items = []

    for tool in self.sync_tools:
     
      tool.auto_scan()
      
      logger.debug("add tool '%s' to list" % tool.get_name())
      line = "%s: %s" % (tool.get_name(), tool.get_sync_summary())
      
      logger.info("line=%s" % line)

      entryMap = { 'title' : line }
      
      if tool.has_error():
        entryMap['image'] = 'ionicons-ios7-bolt-outline-32'        
      elif tool.is_scanned():
        if tool.is_sync_required():
          entryMap['image'] = 'ionicons-ios7-refresh-outline-32'
        else:
          entryMap['image'] = 'ionicons-ios7-checkmark-outline-32'
      else:
        entryMap['image'] = 'ionicons-ios7-search-32'
        


#      if mode.isImmutable: 
#        
#      if len(mode.comment) > 0:
#        entryMap['accessory_type'] = 'detail_button'
#        logger.debug("add accessory for mode '%s'" % mode.name)
        
      items.append(entryMap)
        
    #self.list_data_source.highlight_color = defaults.COLOR_LIGHT_GREEN
    self.tableview_sync_selector.data_source.items = items
    
    if self.selected_index != None:
      self.tableview_sync_selector.data_source.selected_row = self.selected_index
    
    
  def update_view_states(self):
    
    global logger
    
    logger.info("update_view_states: selected_index=%s" % str(self.selected_index))
    
    if self.selected_index != None:
      
      sync_tool = self.sync_tools[self.selected_index]
      if sync_tool.is_scanned():
        scan_active = False
        sync_active = sync_tool.is_sync_required()
      else:
        scan_active = True
        sync_active = False
              
    else:
      
      scan_active = False
      sync_active = False
    
    self.button_scan.enabled = scan_active
    self.button_sync.enabled = sync_active

  def handle_action(self, sender):
    
    global logger
    
    close = False
    if type(sender).__name__ == 'ListDataSource':
      self.selected_index = sender.selected_row
      logger.debug("handle_action from ListDataSource: selected_index=%d" % self.selected_index)
      self.update_view_states()
        
    elif sender.name == 'button_sync':
      logger.debug("handle_action from sync button")
      self.execute_sync()
      self.update_tool_states()
      self.update_view_states()
      
    elif sender.name == 'button_scan':
      logger.debug("handle_action from scan button")
      self.execute_scan()
      self.update_tool_states()
      self.update_view_states()
      
    if close:
      self.view.close()
      if self.parent_view:
        self.parent_view.handle_action(self)
        
  def execute_scan(self):
    
    if self.selected_index != None:
      sync_tool = self.sync_tools[self.selected_index]
      sync_tool.scan()
      
  def execute_sync(self):
    
    if self.selected_index != None:
      sync_tool = self.sync_tools[self.selected_index]
      sync_tool.sync()
      sync_tool.scan()
      
  def handle_accessory(self, sender):
    
    global logger
    
    logger.debug("handle_accessory row=%d" % sender.tapped_accessory_row)
    comment = self.modes[sender.tapped_accessory_row].comment
         
    if not self.popup_vc:
      self.popup_vc = popup.PopupViewController()

    self.popup_vc.present(comment, close_label=self.close_label)

