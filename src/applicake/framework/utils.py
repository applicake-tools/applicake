'''
Created on Dec 14, 2010

@author: quandtan
'''

import logging,itertools,os,fcntl,time,random,xml.parsers.expat,sys
#import win32con, win32file, pywintypes,fcntl
from configobj import ConfigObj #easy_install configobj
from string import Template 
 
class Workflow():
    
    def get_jobid(self,dirname):
        'Return a unique job id'
        jobid = 1
        filename = os.path.join(dirname, 'jobid.txt')
        locker = FileLocker()
        if (os.path.exists(filename)):            
            fh = open(filename,'r') 
            locker.lock(fh,locker.LOCK_EX) 
            jobid= int(fh.read())   
            jobid += 1         
        fh = open(filename,'w')    
        fh.write(str(jobid))
        locker.unlock(fh)            
        return jobid  
    
class Extensions():
    """
    Bean that provides list of defined extensions 
    """
    def __init(self):
        self.param = ".params"
        self.template = ".tpl"
        self.result = ".result"
        self.ini = '.ini'      
    
# Python cookbook receipe 2.28 "File Locking Using a Cross-Platform API"
class FileLocker():
    
    # needs win32all to work on Windows (NT, 2K, XP, _not_ /95 or /98)
    if os.name == 'nt':
        import win32con, win32file, pywintypes
        LOCK_EX = win32con.LOCKFILE_EXCLUSIVE_LOCK
        LOCK_SH = 0 # the default
        LOCK_NB = win32con.LOCKFILE_FAIL_IMMEDIATELY
        _overlapped = pywintypes.OVERLAPPED( )
        def lock(self,file, flags):
            hfile = win32file._get_osfhandle(file.fileno( ))
            win32file.LockFileEx(hfile, flags, 0, 0xffff0000,self._overlapped)
        def unlock(self,file):
            hfile = win32file._get_osfhandle(file.fileno( ))
            win32file.UnlockFileEx(hfile, 0, 0xffff0000,self._overlapped)
    elif os.name == 'posix':
        from fcntl import LOCK_EX, LOCK_SH, LOCK_NB
        def lock(self,file, flags):
            fcntl.flock(file.fileno( ), flags)
        def unlock(self,file):
            fcntl.flock(file.fileno( ), fcntl.LOCK_UN)
    else:
        raise RuntimeError("PortaLocker only defined for nt and posix platforms")
                    
                
class Utilities():  
    
    def get_flatten_sequence(self,sequence):
        """get_flatten_sequence(sequence) -> list    
        Returns a single, flat list which contains all elements retrieved
        from the sequence and all recursively contained sub-sequences
        (iterables).
        Examples:
        >>> [1, 2, [3,4], (5,6)]
        [1, 2, [3, 4], (5, 6)]
        >>> get_flatten_sequence([[[1,2,3], (42,None)], [4,5], [6], 7, MyVector(8,9,10)])
        [1, 2, 3, 42, None, 4, 5, 6, 7, 8, 9, 10]"""    
        result = []
        for e in sequence:
            if hasattr(e, "__iter__") and not isinstance(e, basestring):
                result.extend(self.get_flatten_sequence(e))
            else:
                result.append(e)
        return result                
    
    def get_list_product(self,list_of_lists):
        # itertools.product() fails, when not all elements of the list are also lists.
        for idx, val in enumerate(list_of_lists):  
            if type(val) is not list:                
                list_of_lists[idx] = [val] 
        _list = []
        for element in itertools.product(*list_of_lists):
            _list.append(element)
        return _list       
           
    # http://www.peterbe.com/plog/uniqifiers-benchmark
    def get_sorted_unique_elements(self,seq, idfun=None):
        # order preserving 
        if idfun is None: 
            def idfun(x): return x 
        seen = {} 
        result = [] 
        for item in seq: 
            marker = idfun(item) 
            # in old Python versions: 
            # if seen.has_key(marker) 
            # but in new ones: 
            if marker in seen: continue 
            seen[marker] = 1 
            result.append(item) 
        return result  
                        

    def substitute_template(self,template_filename,dictionary,output_filename=None):
        fh = open(template_filename,'r')
        content = fh.read()
        fh.close()
        mod_content = Template(content).safe_substitute(dictionary)
        if output_filename is None:
            output_filename = template_filename    
        fh = open(output_filename,'w')
        fh.write(mod_content)
        fh.close()
        
        

    def get_cksum(self,filename, md5=True,exclude_line="", include_line=""):        
        """compute md5 for a file. allows to get md5 before including a line in the file or when excluding a specific line"""
        import hashlib
        cksum = None
        if md5:
            cksum = hashlib.md5()
        else:
            cksum = hashlib.sha224()
        for line in open(filename,"rb"):
            if exclude_line and line.startswith(exclude_line):
                continue
            cksum.update(line)
        cksum.update(include_line)
        return cksum.hexdigest()
              
class XmlValidator():    
    
    def __init__(self,xml_filename):
        self._filename = xml_filename

    def parsefile(self):
        parser = xml.parsers.expat.ParserCreate()
        parser.ParseFile(open(self._filename, "r"))

    def is_wellformatted(self): 
        try:
            self.parsefile()
            return True
        except Exception, e:
            print str(e)
            return False       

from Queue import Queue
from threading import Thread

class Worker(Thread):
    """Thread executing tasks from a given tasks queue"""
    def __init__(self, tasks):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()
    
    def run(self):
        while True:
            func, args, kargs = self.tasks.get()
            try: func(*args, **kargs)
            except Exception, e: print e
            self.tasks.task_done()

class ThreadPool(object):
    """Pool of threads consuming tasks from a queue"""
    def __init__(self, num_threads):
        self.tasks = Queue(num_threads)
        for _ in range(num_threads): Worker(self.tasks)

    def add_task(self, func, *args, **kargs):
        """Add a task to the queue"""
        self.tasks.put((func, args, kargs))

    def wait_completion(self):
        """Wait for completion of all the tasks in the queue"""
        self.tasks.join()
        
     
