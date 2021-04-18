import os
import time
import re

# import globals as cmt
from checkitem import CheckItem

s_dirs = 0
conf_filter_extension = []
conf_filter_regexp = None

VALID_TARGET_LIST = [
        'files_min','files_max',
        'size_min','size_max',
        'age_min','age_max',
        'has_old', 'has_recent',
        'has_files',
        ]

def scanRecurse(path):
    global s_dirs
    try:
        for entry in os.scandir(path):
            if entry.is_file(follow_symlinks=False):
                yield entry
            elif entry.is_dir(follow_symlinks=False):
                s_dirs += 1
                yield from scanRecurse(entry.path)
    except Exception:
        pass

def scanNoRecurse(path):
    global s_dirs
    try:
        for entry in os.scandir(path):
            if entry.is_file(follow_symlinks=False):
                yield entry
            elif entry.is_dir(follow_symlinks=False):
                s_dirs += 1
                #yield from scanRecurse(entry.path)
    except Exception:
        pass

def filter_extension(entry):
    for e in conf_filter_extension:
        if entry.name.endswith(e):    
            return True
    return False

def filter_regexp(entry):
    if re.match(conf_filter_regexp, entry.name):
        return True
    return False

def get_file_content(path):
    r = ""
    try:
        with open(path,"r") as f:
            for line in f.readlines():
                r = r + line
                if len(r) > 100:
                    break
    except:
        pass
    if len(r) > 100:
        r = r[:100] + "(...)"
    #print("r=",r)
    return r

def check(c):

    '''Check for various folder attributes '''

    global s_dirs
    s_dirs = 0

    path = c.conf['path']
    name = c.check
    recursive = c.conf.get("recursive",False) is True
    no_store = c.conf.get("no_store",False) is True
    send_content = c.conf.get("send_content",False) is True

    global conf_filter_extension
    conf_filter_extension = c.conf.get("filter_extension","").split()
    if len(conf_filter_extension) > 0:
        has_filter_extension = True
    else:
        has_filter_extension = False

    global conf_filter_regexp
    if "filter_regexp" in c.conf:
        conf_filter_regexp = re.compile(c.conf.get("filter_regexp"))
        has_filter_regexp = True
    else:
        has_filter_regexp = False

    targets = []
    if 'target' in c.conf:
        targets = c.conf['target']
    
    c.add_item(CheckItem('folder_path',path))
    c.add_item(CheckItem('folder_name',name))

    if not os.path.exists(path):      
        c.alert += 1
        c.add_message("folder {} missing".format(path))       
        return c

    # scan
    # ----
    s_count = 0      # total file count
    s_size = 0       # total size sum
    s_mintime = -1    # oldest file (minimal unix timestamp)
    s_maxtime = 0     # most recent file (maximal unix timestamp)
    s_files = []

    # single file
    if os.path.isfile(path):
        statinfo = os.stat(path)
        s_size = statinfo.st_size
        s_count = 1
        s_mintime = statinfo.st_mtime
        s_maxtime = statinfo.st_mtime

        # option : send_content
        if send_content:
            fico = get_file_content(path)
            ci = CheckItem('file_content',fico,"file content")
            c.add_item(ci)


    # directory
    elif os.path.isdir(path):
        #for entry in os.scandir(path):
        if recursive:
            for entry in scanRecurse(path):

                if has_filter_extension:
                    if not filter_extension(entry):
                        continue
                if has_filter_regexp:
                    if not filter_regexp(entry):
                        continue

                s_count += 1
                if not no_store:
                    s_files.append(entry.name)
                statinfo = os.stat(entry.path)
                s_size += statinfo.st_size
                if statinfo.st_mtime > s_maxtime:
                    s_maxtime = statinfo.st_mtime
                if statinfo.st_mtime < s_mintime or s_mintime == -1 :
                    s_mintime = statinfo.st_mtime
        else:
            for entry in scanNoRecurse(path):
                if has_filter_extension:
                    if not filter_extension(entry):
                        continue                
                s_count += 1
                if not no_store:
                    s_files.append(entry.name)
                statinfo = os.stat(entry.path)
                s_size += statinfo.st_size
                if statinfo.st_mtime > s_maxtime:
                    s_maxtime = statinfo.st_mtime
                if statinfo.st_mtime < s_mintime or s_mintime == -1 :
                    s_mintime = statinfo.st_mtime

    else:
        c.warn = 1
        c.add_message("folder {} ({}) is not a dir / nor a file".format(name, path))
        return c

    # file count
    ci = CheckItem('folder_files', s_count, "Number of files in folder " + name, unit="files")
    c.add_item(ci)

    # dirs count
    ci = CheckItem('folder_dirs',s_dirs,"Number of dirs/subdirs in folder " + name, unit="dirs")
    c.add_item(ci)

    # size
    ci = CheckItem('folder_size',s_size,"Total Size (bytes)", unit="bytes")
    h_size = ci.human()
    c.add_item(ci)

    # age
    now = time.time()
    if s_maxtime > 0:
        ci = CheckItem('folder_youngest',"","most recent file (seconds)", unit="sec")
        ci.value = int(now - s_maxtime)
        c.add_item(ci)
    if s_mintime != -1:
        ci = CheckItem('folder_oldest',"","oldest file (seconds)", unit="sec")
        ci.value = int(now - s_mintime)
        c.add_item(ci)


    # Target checks
    # --------------
    tgcount = 0
    tgtotal = len(targets)

    # check valid target name
    for t in targets:
        if not t in VALID_TARGET_LIST:
            c.warn = 1
            c.add_message("folder {} : unknown target {}".format(path,t))
            return c 

    # target : files_min: 4
    if 'files_min' in targets:
        tgcount += 1
        if s_count < targets['files_min']:
            c.alert += 1
            c.add_message ("folder {} :  too few files ({})".format(path,s_count))
            return c

    # target : files_max: 23
    if 'files_max' in targets:
        tgcount += 1
        if s_count > targets['files_max']:
            c.alert += 1
            c.add_message ("folder {} : too many files ({})".format(path,s_count))
            return c

    # target : size_max (folder max bytes)
    if 'size_max' in targets:
        tgcount += 1
        if s_size > targets['size_max']:
            c.alert += 1
            c.add_message("folder {} : too big ({})".format(path,s_size))
            return c            

    # target : size_min (folder min bytes)
    if 'size_min' in targets:
        tgcount += 1
        if s_size < targets['size_min']:
            c.alert += 1
            c.add_message("folder {} : too small ({})".format(path,s_size))
            return c            

    # target : age_max: 
    # all files must be more recent than age_max seconds
    if 'age_max' in targets:
        tgcount += 1
        if s_mintime != -1:
            if int(now - s_mintime) > targets ['age_max']:
                c.alert += 1
                c.add_message("folder {} : some files are too old ({} sec)".format(path,int(now - s_mintime)))
                return c                

    # target : age_min: 
    # all files must be older than age_min
    if 'age_min' in targets:
        tgcount += 1
        if s_maxtime != 0:
            if int(now - s_maxtime) < targets ['age_min']:
                c.alert += 1
                c.add_message("folder {} : some files are too young ({} sec)".format(path,int(now - s_maxtime)))
                return c   

    # target : has_recent: 
    # some files must be recent (more than has_recent)
    if 'has_recent' in targets:
        tgcount += 1
        if s_maxtime != 0:
            if int(now - s_maxtime) > targets ['has_recent']:
                c.alert += 1
                c.add_message("folder {} : missing young file (min {} sec)".format(path,int(now - s_maxtime)))
                return c   

    # target : has_old: 
    # some files must be older than has_old
    if 'has_old' in targets:
        tgcount += 1
        if s_mintime != -1:
            if int(now - s_mintime) < targets ['has_old']:
                c.alert += 1
                c.add_message("folder {} : missing old file (max {} sec)".format(path,int(now - s_mintime)))
                return c   


    if no_store:
        c.add_message("folder {} OK - {} files, {} dirs, {} bytes [{}] - targets {}/{}".format(
            path, s_count, s_dirs, s_size, h_size, tgcount, tgtotal ))
        return c

    # NEED flist to be stored at scan time
    # target : has_file: filename
    if 'has_files' in targets:
        tgcount += 1
        flist = targets['has_files']
        for f in flist:
            if f not in s_files:
                c.alert += 1
                c.add_message("folder {} : expected file not found ({})".format(path,f))
                return c

    c.add_message("folder {} OK - {} files, {} dirs, {} bytes - targets {}/{}".format(
        path, s_count, s_dirs, s_size, tgcount, tgtotal))
    return c
