import os
import eyed3
from operator import itemgetter
import datetime
import regex as re
from xpinyin import Pinyin
p = Pinyin()

audiodir = "./websites/slow-chinese.com/podcasts/"
externaltextdir = "./websites/external_transcripts/"
targetdir = "../_posts/"


for dirpath, dnames, fnames in os.walk(audiodir):
    for fname in fnames:
        if ".mp3" in fname and "Reading_China" in fname:
            song = eyed3.load(os.path.join(dirpath, fname))
            title = song.tag.title
            author = song.tag.artist
            date = song.tag.recording_date

            episode_num = int(fname[-6:-4])

            if title is None: title = str(episode_num)

            title = title.replace(":", " -")
            title = title.split("#")[-1]

            fnametitle = re.sub(r"\d+", "", title).replace(" ", "")
            outfname = p.get_pinyin(re.sub(r"\p{P}+", "", fnametitle)) + ".md"
            outfname = p.get_pinyin("中文天天读") + "-{:03d}-".format(episode_num) + outfname
            outfname = outfname.lower()

            title = "中文天天读 " + title

            transcript = []
            if os.path.exists(os.path.join(externaltextdir, "Reading_China_{:02d}.txt".format(episode_num))):
                with open(os.path.join(externaltextdir, "Reading_China_{:02d}.txt".format(episode_num))) as f:
                    transcript = f.readlines()
                    if "date:" in transcript[0]:
                        date = datetime.datetime.strptime(transcript[0].split(":")[1].strip(), "%Y-%m-%d")
                        transcript = transcript[1:]
                        transcript[0] = transcript[0][1:]

            for i in range(len(transcript)):
                if transcript[i].endswith("\n"):
                    transcript[i] = transcript[i][:-1] + "  \n"

            print(title, date, outfname)

            outlines = []

            outlines.append("---\n")
            outlines.append("layout: post\n")
            outlines.append("title: "+title+"\n")
            outlines.append("author: "+author+"\n")
            outlines.append("date: " + "{:04d}-{:02d}-{:02d}".format(date.year, date.month, date.day) + "\n")
            outlines.append("categories: []\n")
            outlines.append("tags: []\n")

            localaudiofname = os.path.join(audiodir, "Reading_China_{:02d}.mp3".format(episode_num))
            if os.path.exists(localaudiofname):
                audiosize = os.path.getsize(localaudiofname)
                audiolength = datetime.timedelta(seconds=eyed3.load(localaudiofname).info.time_secs)
                outlines.append(
                    "file: //archive.org/download/readingchina/Reading_China_{:02d}.mp3\n".format(
                        episode_num))
                outlines.append("summary: \"{}\"\n".format("".join(transcript)))
                outlines.append("duration: \"{}\"\n".format(audiolength))
                outlines.append("length: \"{}\"\n".format(audiosize))

            outlines.append("---\n\n")
            #

            #
            # Audio Embed
            #
            if os.path.exists(localaudiofname):
                embed = "<iframe src=\"https://archive.org/embed/readingchina/Reading_China_{:02d}.mp3\" width=\"500\" height=\"30\" frameborder=\"0\" webkitallowfullscreen=\"true\" mozallowfullscreen=\"true\" allowfullscreen></iframe>\n"
                embed = embed.format(episode_num)
                outlines.append(embed)

            with open(os.path.join(targetdir, "{:04d}-{:02d}-{:02d}".format(date.year, date.month, date.day) +
                                   "--" + outfname), "w") as f:

                f.writelines(outlines)
                f.writelines(transcript)