import ui

import ui_util
import log
import popup

reload(ui_util)
reload(log)
reload(popup)

global logger

logger = log.open_logging()

class SyncSelector(ui_util.ViewController):
  
  def __init__(self, parent_vc=None):
    
    super(SyncSelector, self).__init__(parent_vc)
    self.selected_index = None
    self.popup_vc = None
    self.load('sync_selector')
    self.popup_vc = None
         
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

    self.retrieve_tool_states()
    self.update_view_states()
    
    self.present(style)
    
    if not self.parent_view:
      self.view.wait_modal()
    
    
  def update_tool_state(self, selected_index):
    
    global logger
    
    logger.info("update_tool_state: selected_index=%s" % str(selected_index))
    items = []

    tool = self.sync_tools[selected_index]
    tool.auto_scan()
      
    logger.debug("build menu entry for sync config '%s' to list" % tool.get_name())
    line = "%s: %s" % (tool.get_name(), tool.get_sync_summary())
    entryMap = { 'title' : line }
      
    add_accessory = False
    if tool.has_error():
      entryMap['image'] = 'ionicons-ios7-bolt-outline-32'        
      add_accessory = True
    elif tool.is_scanned():
      if tool.is_sync_required():
        entryMap['image'] = 'ionicons-ios7-refresh-outline-32'
        add_accessory = True
      else:
        entryMap['image'] = 'ionicons-ios7-checkmark-outline-32'
    else:
      entryMap['image'] = 'ionicons-ios7-search-32'
        
    if add_accessory: 
        
      entryMap['accessory_type'] = 'detail_button'
      logger.debug("add accessory for sync config '%s'" % tool.get_name())
        
    self.tableview_sync_selector.data_source.items[selected_index] = entryMap
    
    
  def retrieve_tool_states(self):
    
    global logger
    
    logger.info("retrieve_tool_states")
    items = []
   
    for tool in self.sync_tools:
      items.append({})

    self.tableview_sync_selector.data_source.items = items
    i = 0
    for tool in self.sync_tools:
    
      self.update_tool_state(i) 
      i = i + 1
 
    
  def update_view_states(self):
    
    global logger
    
    logger.info("update_view_states: selected_index=%s" % str(self.selected_index))
    
    if self.selected_index != None:
      
      sync_tool = self.sync_tools[self.selected_index]
      if sync_tool.has_error():
        scan_active = True
        sync_active = False        
      elif sync_tool.is_scanned():
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

    if self.selected_index != None:
      self.tableview_sync_selector.data_source.selected_row = self.selected_index

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
      self.update_tool_state(self.selected_index)
      self.update_view_states()
      
    elif sender.name == 'button_scan':
      logger.debug("handle_action from scan button")
      self.execute_scan()
      self.update_tool_state(self.selected_index)
      self.update_view_states()
      
    if close:
      self.view.close()
      if self.parent_view:
        self.parent_view.handle_action(self)
        
  def handle_accessory(self, sender):
    
    global logger
    
    logger.info("handle_accessory row=%d" % sender.tapped_accessory_row)
    
             
    if not self.popup_vc:
      self.popup_vc = popup.PopupViewController()

    comment = self.sync_tools[sender.tapped_accessory_row].get_sync_details()
    self.popup_vc.present(comment)



  def execute_scan(self):
    
    if self.selected_index != None:
      sync_tool = self.sync_tools[self.selected_index]
      sync_tool.scan()
      
  def execute_sync(self):
    
    if self.selected_index != None:
      sync_tool = self.sync_tools[self.selected_index]
      sync_tool.sync()
      sync_tool.scan()
      
  
