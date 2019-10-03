import os
import eyed3
from operator import itemgetter
import datetime
import regex as re
from xpinyin import Pinyin
p = Pinyin()

audiodir = "./websites/slow-chinese.com/podcasts/"
targetdir = "../_posts/"


existing_posts = []
for dirpath, dnames, fnames in os.walk(targetdir):
    for fname in fnames:
        date, name = fname.split("--")
        date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        num = int(name[:3])
        name = name[3:]
        existing_posts.append((date, num, name))

existing_posts.sort(key=itemgetter(1))

for dirpath, dnames, fnames in os.walk(audiodir):
    for fname in fnames:
        if ".mp3" in fname and "Slow_Chinese" in fname:
            song = eyed3.load(os.path.join(dirpath, fname))
            title = song.tag.title
            author = song.tag.artist
            date = song.tag.recording_date
            #date.month = 0
            #date.day = 0

            episode_num = int(fname[-7:-4])

            if title is None: title = str(episode_num)

            title = title.replace(":", " -")
            title = title.split("#")[-1]

            create_dummy = True

            i = 0
            for d, num, ti in existing_posts:
                if num < episode_num:
                    i += 1
                if episode_num == num:
                    create_dummy = False

            if create_dummy:
                if i == len(existing_posts): i = -1
                date = existing_posts[i][0]

                fnametitle = re.sub(r"\d+", "", title).replace(" ", "")
                outfname = p.get_pinyin(re.sub(r"\p{P}+", "", fnametitle)) + ".md"
                # hack to fix one name
                outfname = outfname.replace("MadeinChina", "made-in-china")
                outfname = outfname.replace("TFboys", "tfboys")
                outfname = "{:03d}-".format(episode_num) + outfname
                outfname = outfname.lower()

                existing_posts.append((date, episode_num, outfname))
                existing_posts.sort(key=itemgetter(1))


                title_num = int(title[:3])
                if not title_num == episode_num:
                    title = str(episode_num) + title[3:]
                    print("broken title episode number fixed")


                print(title, date, outfname)

                outlines = []

                outlines.append("---\n")
                outlines.append("layout: post\n")
                outlines.append("title: "+title+"\n")
                outlines.append("author: "+author+"\n")
                outlines.append("date: " + "{:04d}-{:02d}-{:02d}".format(date.year, date.month, date.day) + "\n")
                outlines.append("categories: []\n")
                outlines.append("tags: []\n")

                localaudiofname = os.path.join(audiodir, "Slow_Chinese_{:03d}.mp3".format(episode_num))
                if os.path.exists(localaudiofname):
                    audiosize = os.path.getsize(localaudiofname)
                    audiolength = datetime.timedelta(seconds=eyed3.load(localaudiofname).info.time_secs)
                    outlines.append(
                        "file: //archive.org/download/slowchinese_201909/Slow_Chinese_{:03d}.mp3\n".format(
                            episode_num))
                    outlines.append("summary: \"\"\n")
                    outlines.append("duration: \"{}\"\n".format(audiolength))
                    outlines.append("length: \"{}\"\n".format(audiosize))

                outlines.append("---\n\n")
                #

                #
                # Audio Embed
                #
                if os.path.exists(localaudiofname):
                    embed = "<iframe src=\"https://archive.org/embed/slowchinese_201909/Slow_Chinese_{:03d}.mp3\" width=\"500\" height=\"30\" frameborder=\"0\" webkitallowfullscreen=\"true\" mozallowfullscreen=\"true\" allowfullscreen></iframe>\n"
                    embed = embed.format(episode_num)
                    outlines.append(embed)

                with open(os.path.join(targetdir, "{:04d}-{:02d}-{:02d}".format(date.year, date.month, date.day) +
                                       "--" + outfname), "w") as f:

                    f.writelines(outlines)