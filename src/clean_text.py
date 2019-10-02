import os
import shutil
#import re

workingdir = "./websites/slow-chinese.com/podcast/"

for dirpath, dnames, fnames in os.walk(workingdir):
    for dname in dnames:
        if "category" == dname:
            shutil.rmtree(os.path.join(dirpath, dname))
        if "tag" == dname:
            shutil.rmtree(os.path.join(dirpath, dname))
        elif "?" in dname:
            shutil.rmtree(os.path.join(dirpath, dname))
        elif "zh-hant" in dname:
            shutil.rmtree(os.path.join(dirpath, dname))
        elif "zh-hans" in dname:
            shutil.rmtree(os.path.join(dirpath, dname))
        elif "feed" in dname:
            shutil.rmtree(os.path.join(dirpath, dname))
        elif "comment-page" in dname:
            shutil.rmtree(os.path.join(dirpath, dname))
        elif "history-and-tradition" in dname:
            shutil.rmtree(os.path.join(dirpath, dname))
        elif "modern-china" in dname:
            shutil.rmtree(os.path.join(dirpath, dname))
        elif "pop-culture" in dname:
            shutil.rmtree(os.path.join(dirpath, dname))

