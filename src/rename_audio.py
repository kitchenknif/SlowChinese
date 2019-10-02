import os



workingdir = "./websites/slow-chinese.com/podcasts/"

for dirpath, dnames, fnames in os.walk(workingdir):
    for fname in fnames:
        for i in range(300):
            if "_{:d}.mp3".format(i) in fname and "Slow_Chinese" in fname:
                os.rename(os.path.join(dirpath, fname), os.path.join(dirpath, "Slow_Chinese_{:03d}.mp3".format(i)))

            if "_{:d}.mp3".format(i) in fname and "Reading_China" in fname:
                os.rename(os.path.join(dirpath, fname), os.path.join(dirpath, "Reading_China_{:03d}.mp3".format(i)))