import client
import os
import time
import logging
import re
import tempfile

reload(client)
reload(logging)

LOCAL_DIR = '../Rechtschreibung'
REMOTE_DIR = '/rechtschreibung'

GIT_IGNORE_FILE = '.gitignore'
BITSYNCHISRA_IGNORE_FILE = 'bitsynchista_ignore'

global logger

logger = logging.getLogger('bitsynchista')  
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

class File(object):
  
  def __init__(self, name, base_name, mtime, sub_files = None):
    
    self.name = name
    self.base_name = base_name
    self.mtime = mtime
    self.sub_files = sub_files
    
  def is_directory(self):

    return self.sub_files != None
    
  def __str__(self):
    return "%s %s %d %s" % (self.name, self.is_directory(), self.mtime, time.ctime(self.mtime))
  
class IgnoreInfo(object):
  
  def __init__(self, file_string):
    
    global logger
    
    pattern_string = ('^' + file_string.replace('*', '.*').replace('\n','$|^') + '$').replace('|^$', '')
    logger.info("Created IgnoreInfo with pattern regex '%s'" % pattern_string)
    self.regex = re.compile(pattern_string)        
    
  def is_ignored(self, name):
    
    return self.regex.match(name)
    
class FileAccess(object):
  
  def load_directory(self, base_path, root_path=None):
    
    logger.info("Loading file directory '%s'" % base_path)
    if not root_path:
      root_path = base_path
    files = []
    github_ignore_info = self.load_ignore_info(os.path.join(base_path, GIT_IGNORE_FILE))
    bitsynchista_ignore_info = self.load_ignore_info(os.path.join(base_path, BITSYNCHISRA_IGNORE_FILE))
    for f in os.listdir(base_path):
      if (github_ignore_info and github_ignore_info.is_ignored(f)) or (bitsynchista_ignore_info and bitsynchista_ignore_info.is_ignored(f)):
        continue
      path = os.path.join(base_path, f)
      attr = os.stat(path)
      isDirectory = os.path.isdir(path)
      if isDirectory:
        sub_files = self.load_directory(base_path=path, root_path=root_path)
      else:
        sub_files = None
      
      file = File(name=path.replace(root_path, '.', 1), base_name=f, mtime=attr.st_mtime, sub_files=sub_files)
      files.append(file)
    
    return files
       
  def file_exists(self, path):
    
    return os.path.exists(path)
    
  def load_ignore_info(self, ignore_file):

    global logger
  
    if self.file_exists(ignore_file):
      ignore_patterns = self.load_into_string(ignore_file)
      logger.info("Loading ignore file '%s'" % ignore_file)    
      return IgnoreInfo(ignore_patterns)
    else:
      return None
   
  def save_from_string(self, path, string):
    
    with open(path, "wb") as file:
      file.write(string)
  
  def load_into_string(self, path):
    
    return open(path, "rb").read()
  
class WebDavFileAccess(FileAccess):
  
  def __init__(self, webdav_client):
    
    #super(WebDavFileAccess, self).__init()
    self.webdav_client = webdav_client
    
  def file_exists(self, path):
    base_name = os.path.basename(path)
    if base_name[0] == '.':
      return False
    else:
      return self.webdav_client.exists(path)
    
  def load_directory(self, base_path, root_path=None):
  
    global logger
    
    logger.info("Loading WebDav directory '%s'" % base_path)
    if not root_path:
      root_path = base_path
    files = []
    ignore_info = self.load_ignore_info(os.path.join(base_path, GIT_IGNORE_FILE))
    for f in self.webdav_client.ls(base_path):
      if base_path == f.name:
        continue 
      #print f.name
      if f.mtime == '':
        sub_files = self.load_directory(base_path=f.name, root_path=root_path)
        mtime = 0
      else:
        sub_files = None
        struct_time = time.strptime(f.mtime, '%a, %d %b %Y %H:%M:%S %Z')
        mtime = time.mktime(struct_time)
      file = File(name=f.name.replace(root_path, '.', 1), base_name=os.path.basename(f.name), mtime=mtime, sub_files=sub_files)
      files.append(file)
    
    return files
    
  def save_from_string(self, path, string):
    
    bstring = basestring(string)
    self.webdav_client.upload(path, bstring)
  
  def load_into_string(self, path):
  
    bstring = basestring()  
    webdav_client.download(path, bstring)
    return str(bstring)
        
        
def compare_file_sets(file_dict1, file_dict2, change_info):
  for (file_name1, file1) in file_dict1.items():
      if not file_name1 in file_dict2:
        change_info.new_files.append(file1)
      elif (not file1.is_directory()) and file1.mtime > file_dict2[file_name1].mtime:
        change_info.modified_files.append(file1)

class ChangeInfo(object):
  
  def __init__(self):
    
    self.new_files = []
    self.modified_files = []

class CompareInfo(object):
  
  def __init__(self, local_file_access, remote_file_access, local_root_path, remote_root_path):
    
    global logger
    
    self.local_file_access = local_file_access
    self.remote_file_access = remote_file_access
    logger.info("Loading local directory structure")
    self.local_files = local_file_access.load_directory(local_root_path)
    logger.info("Loading remote directory structure")
    self.remote_files = remote_file_access.load_directory(remote_root_path)
    self.local_change_info = ChangeInfo()
    self.remote_change_info = ChangeInfo()
    self.compare()

    
  def compare(self):
  
    self.local_file_dict = make_file_dictionary(self.local_files)
    self.remote_file_dict = make_file_dictionary(self.remote_files)
  
    compare_file_sets(self.local_file_dict, self.remote_file_dict, self.local_change_info)
    compare_file_sets(self.remote_file_dict, self.local_file_dict, self.remote_change_info)

    
def make_file_dictionary(files, file_dict=None):
  
  if not file_dict:
    file_dict = {}
  for file in files:
    file_dict[file.name] = file
    if file.sub_files:
      make_file_dictionary(file.sub_files, file_dict)
      
  return file_dict
    

def dump_files(files, indent=0):
  
  global logger

  for f in files:
    logger.info("%s %s" % (" " * indent, str(f)))
    if f.is_directory():
      dump_files(f.sub_files, indent = indent + 4)
  
def test():

  global logger

  webdav_client = client.Client('localhost', port=8080,
                 protocol='http', verify_ssl=False, cert=None)
  local_file_access = FileAccess()
  remote_file_access = WebDavFileAccess(webdav_client)    
  
  compare_info = CompareInfo(local_file_access, remote_file_access, LOCAL_DIR, REMOTE_DIR)
  
  logger.info("Local files:")
  dump_files(compare_info.local_files)
  logger.info("Remote files:")
  dump_files(compare_info.remote_files)
  
  logger.info("Local new files:")
  for file in compare_info.local_change_info.new_files:
    logger.info("    %s" % str(file))
  logger.info("Local modified files:")
  for file in compare_info.local_change_info.modified_files:
    logger.info("    %s" % str(file))
  logger.info("Remote new files:")
  for file in compare_info.remote_change_info.new_files:
    logger.info("    %s" % str(file))
  logger.info("Remote modified files:")
  for file in compare_info.remote_change_info.modified_files:
    logger.info("    %s" % str(file))
    
  
if __name__ == '__main__':
  test()

  
