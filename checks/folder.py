import os
import time

#import cmt_globals as cmt
from cmt_shared import Check, CheckItem


s_dirs = 0

def scanRecurse(path):
    global s_dirs
    try:
        for entry in os.scandir(path):
            if entry.is_file(follow_symlinks=False):
                yield entry
            elif entry.is_dir(follow_symlinks=False):
                s_dirs += 1
                yield from scanRecurse(entry.path)
    except:
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
    except:
        pass

def check_folder(c):

    '''Check for various folder attributes '''

    global s_dirs
    s_dirs = 0

    path = c.conf['path']

    name = c.name

    recursive = c.conf.get("recursive",False) == True

    no_store = c.conf.get("no_store",False) == True


    targets = []
    if 'target' in c.conf:
        targets = c.conf['target']

    ci = CheckItem('folder_path',path)
    c.add_item(ci)
    ci = CheckItem('folder_name',name)
    c.add_item(ci)

    if not os.path.exists(path):      
        c.alert += 1
        c.add_message("folder {} missing".format(path))       
        return c

    # scan
    # ----
    s_count = 0
    s_size = 0
    s_minage = -1
    s_maxage = 0
    s_files = []
    
    if os.path.isfile(path):
        statinfo = os.stat(path)
        s_size = statinfo.st_size
        s_count = 1
        s_maxage = statinfo.st_mtime
        s_minage = statinfo.st_mtime

    elif os.path.isdir(path):
        #for entry in os.scandir(path):
        if recursive:
            for entry in scanRecurse(path):
                    s_count += 1
                    if not no_store:
                        s_files.append(entry.name)
                    statinfo = os.stat(entry.path)
                    s_size += statinfo.st_size
                    if statinfo.st_mtime > s_maxage:
                        s_maxage = statinfo.st_mtime
                    if statinfo.st_mtime < s_minage or s_minage == -1 :
                        s_minage = statinfo.st_mtime
        else:
            for entry in scanNoRecurse(path):
                    s_count += 1
                    if not no_store:
                        s_files.append(entry.name)
                    statinfo = os.stat(entry.path)
                    s_size += statinfo.st_size
                    if statinfo.st_mtime > s_maxage:
                        s_maxage = statinfo.st_mtime
                    if statinfo.st_mtime < s_minage or s_minage == -1 :
                        s_minage = statinfo.st_mtime

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
    if s_maxage > 0:
        ci = CheckItem('folder_age_min',"","Min age (seconds)", unit="sec")
        ci.value = int(now - s_maxage)
        c.add_item(ci)
    if s_minage != -1:
        ci = CheckItem('folder_age_max',"","Max age (seconds)", unit="sec")
        ci.value = int(now - s_minage)
        c.add_item(ci)



    # Target checks
    # --------------
    tgcount = 0
    tgtotal = len(targets)

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
    if 'age_max' in targets:
        tgcount += 1
        if s_minage != -1:
            if int(now - s_minage) > targets ['age_max']:
                c.alert += 1
                c.add_message("folder {} : some files too old ({} sec)".format(path,int(now - s_minage)))
                return c                

    # target : age_min: 
    if 'age_min' in targets:
        tgcount += 1
        if s_maxage != 0:
            if int(now - s_maxage) < targets ['age_min']:
                c.alert += 1
                c.add_message("folder {} : some files too young ({} sec)".format(path,int(now - s_maxage)))
                return c   

    if no_store:
        c.add_message("folder {} ({}) OK - {} files, {} dirs, {} bytes [{}] - targets {}/{}".format(
            name, path, s_count, s_dirs, s_size, h_size, tgcount, tgtotal ))
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

    c.add_message("folder {} ({}) OK - {} files, {} dirs, {} bytes - targets {}/{}".format(
        name, path, s_count, s_dirs, s_size, tgcount, tgtotal))
    return c
