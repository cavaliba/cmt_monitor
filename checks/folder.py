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

    #c = Check(module='folder') 

    path = c.conf['path']

    name = path
    if 'name' in c.conf:
        name = c.conf['name']

    recursive = c.conf.get("recursive",False) == True

    targets = []
    if 'target' in c.conf:
        targets = c.conf['target']
        #print(targets)

    ci = CheckItem('folder_path',path)
    c.add_item(ci)
    ci = CheckItem('folder_name',name)
    c.add_item(ci)

    if not os.path.exists(path):
        ci = CheckItem('folder_status',"","ok/nok", unit="")
        ci.value="nok"
        c.add_item(ci)        
        c.alert += 1
        c.add_message("{} missing".format(path))       
        return c

    # scan
    # ----
    s_count = 0
    s_size = 0
    s_minage = -1
    s_maxage = 0
    s_files = []
    
    #for entry in os.scandir(path):
    if recursive:
        for entry in scanRecurse(path):
                s_files.append(entry.name)
                s_count += 1
                statinfo = os.stat(entry.path)
                s_size += statinfo.st_size
                if statinfo.st_mtime > s_maxage:
                    s_maxage = statinfo.st_mtime
                if statinfo.st_mtime < s_minage or s_minage == -1 :
                    s_minage = statinfo.st_mtime
    else:
        for entry in scanNoRecurse(path):
                s_files.append(entry.name)
                s_count += 1
                statinfo = os.stat(entry.path)
                s_size += statinfo.st_size
                if statinfo.st_mtime > s_maxage:
                    s_maxage = statinfo.st_mtime
                if statinfo.st_mtime < s_minage or s_minage == -1 :
                    s_minage = statinfo.st_mtime


    # file count
    ci = CheckItem('folder_files', s_count, "Number of files in folder " + name, unit="files")
    c.add_item(ci)

    # dirs count
    ci = CheckItem('folder_dirs',s_dirs,"Number of dirs/subdirs in folder " + name, unit="dirs")
    c.add_item(ci)

    # size
    ci = CheckItem('folder_size',s_size,"Total Size (bytes)", unit="bytes")
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
    ci = CheckItem('folder_status',"","ok/nok", unit="")
    tgcount = 0

    # target : files_min: 4
    if 'files_min' in targets:
        tgcount += 1
        if s_count < targets['files_min']:
            ci.value="nok"
            c.add_item(ci)
            c.alert += 1
            c.add_message ("{} :  too few files ({})".format(path,s_count))
            return c

    # target : files_max: 23
    if 'files_max' in targets:
        tgcount += 1
        if s_count > targets['files_max']:
            ci.value="nok"
            c.add_item(ci)
            c.alert += 1
            c.add_message ("{} : too many files ({})".format(path,s_count))
            return c

    # target : size_max (folder max bytes)
    if 'size_max' in targets:
        tgcount += 1
        if s_size > targets['size_max']:
            ci.value="nok"
            c.add_item(ci)
            c.alert += 1
            c.add_message("{} : too big ({})".format(path,s_size))
            return c            

    # target : size_min (folder min bytes)
    if 'size_min' in targets:
        tgcount += 1
        if s_size < targets['size_min']:
            ci.value="nok"
            c.add_item(ci)
            c.alert += 1
            c.add_message("{} : too small ({})".format(path,s_size))
            return c            

    # target : age_max: 
    if 'age_max' in targets:
        tgcount += 1
        if s_minage != -1:
            if int(now - s_minage) > targets ['age_max']:
                ci.value="nok"
                c.add_item(ci)
                c.alert += 1
                c.add_message("{} : some files too old ({} sec)".format(path,int(now - s_minage)))
                return c                

    # target : age_min: 
    if 'age_min' in targets:
        tgcount += 1
        if s_maxage != 0:
            if int(now - s_maxage) < targets ['age_min']:
                ci.value="nok"
                c.add_item(ci)
                c.alert += 1
                c.add_message("{} : some files too young ({} sec)".format(path,int(now - s_maxage)))
                return c   

    # target : has_file: filename
    if 'has_files' in targets:
        tgcount += 1
        flist = targets['has_files']
        for f in flist:
            if f not in s_files:
                ci.value="nok"
                c.add_item(ci)
                c.alert += 1
                c.add_message("{} : expected file not found ({})".format(path,f))
                return c

    ci = CheckItem('folder_status',"ok","check if targets are met.", unit="ok/nok")
    c.add_item(ci)

    c.add_message("{} ({}) ok - {} files, {} dirs, {} bytes - {} targets OK".format(name, path, s_count, s_dirs, s_size, tgcount))
    return c
