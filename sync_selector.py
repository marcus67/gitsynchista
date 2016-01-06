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
    
  def select(self, sync_tools):

    global logger

    self.sync_tools = sync_tools        

    items = []

    for tool in self.sync_tools:
     
      logger.debug("add tool '%s' to list" % tool.get_name())
      entryMap = { 'title' : tool.get_name() }


#      if mode.isImmutable: 
#        entryMap['image'] = 'ionicons-ios7-locked-32'
#      else:
#        entryMap['image'] = 'ionicons-ios7-unlocked-outline-32'
#        
#      if len(mode.comment) > 0:
#        entryMap['accessory_type'] = 'detail_button'
#        logger.debug("add accessory for mode '%s'" % mode.name)
        
      items.append(entryMap)
        
    self.list_data_source = ui.ListDataSource(items)
    #self.list_data_source.highlight_color = defaults.COLOR_LIGHT_GREEN
    self.selected_index = None
    self.tableview_sync_selector = self.find_subview_by_name('tableview_sync_selector')
    self.tableview_sync_selector.data_source = self.list_data_source
    
    self.button_sync = self.find_subview_by_name('button_sync')

    self.present()
    
    if not self.parent_view:
      self.view.wait_modal()
    
    
  def handle_action(self, sender):
    
    global logger
    
    close = False
    if type(sender).__name__ == 'ListDataSource':
      self.selected_index = sender.selected_row
      logger.debug("handle_action from ListDataSource: selected_index=%d" % self.selected_index)
      close = True
        
    elif sender.name == 'button_cancel':
      logger.debug("handle_action from cancel button")
      close =True
      
    if close:
      self.view.close()
      if self.parent_view:
        self.parent_view.handle_action(self)
        
  def handle_accessory(self, sender):
    
    global logger
    
    logger.debug("handle_accessory row=%d" % sender.tapped_accessory_row)
    comment = self.modes[sender.tapped_accessory_row].comment
         
    if not self.popup_vc:
      self.popup_vc = popup.PopupViewController()

    self.popup_vc.present(comment, close_label=self.close_label)

