import os
import regex as re
import datetime

import bs4
from bs4 import BeautifulSoup
import eyed3

from xpinyin import Pinyin
p = Pinyin()

audiodir = "./websites/slow-chinese.com/podcasts/"
workingdir = "./websites/slow-chinese.com/podcast/"
targetdir = "../_posts/"

if not os.path.exists(targetdir):
    os.makedirs(targetdir)


for dirpath, dnames, fnames in os.walk(workingdir):
    for fname in fnames:
        if not ".html" in fname:
            continue

        with open(os.path.join(dirpath, fname)) as f:
            soup = BeautifulSoup(f, 'html5lib')
            if "中文天天读" in soup.head.title.get_text() or "podcast Archives" in soup.head.title.get_text():
                break

            #
            # Parse HTML
            #

            #print(soup.title.string)
            fnametitle = soup.article.h1.a.get_text().replace(":", "-").replace("#", "").replace(" ", "-")
            title = soup.article.h1.a.get_text().replace(":", " -").replace("#", "")

            episode_num = int(re.findall(r'\d+', fnametitle)[0])
            fnametitle = re.sub(r"\d+", "", fnametitle)
            outfname = p.get_pinyin(re.sub(r"\p{P}+", "", fnametitle)) + ".md"
            # hack to fix one name
            outfname = outfname.replace("MadeinChina", "made-in-china")
            outfname = outfname.replace("TFboys", "tfboys")
            outfname = "{:03d}-".format(episode_num) + outfname
            outfname = outfname.lower()

            author = soup.article.find("span", "meta_author").get_text()
            date = soup.article.find("span", "meta_date").get_text().replace("/", "-")

            raw_tags = soup.article.find("span", "meta_tag")
            tags = [tag.get_text() for tag in raw_tags.find_all("a")]

            raw_cat = soup.article.find("span", "meta_category")
            categories = [tag.get_text() for tag in raw_cat.find_all("a")]

            transcript = []
            if len(soup.article.find_all("div", id="-0")) == 0:
                start_text = soup.article.find_all("p", "powerpress_embed_box")[-1].next_sibling
                while(start_text.name == "p" or start_text == "\n"):
                    if isinstance(start_text, bs4.Tag):
                        transcript.append(start_text.get_text())
                    elif isinstance(start_text, bs4.NavigableString):
                        transcript.append("\n")

                    start_text = start_text.next_sibling
            else:
                transcript.append(soup.article.find_all("div", id="-0")[0].get_text())

            #
            # Write Markdown post
            #

            outlines = []
            outlines.append("---\n")
            outlines.append("layout: post\n")
            outlines.append("title: "+title+"\n")
            outlines.append("author: "+author+"\n")
            outlines.append("date: " + date + "\n")
            outlines.append("tags: [")
            for tag in tags:
                outlines.append(tag + ", ")
            outlines.append("]\n")

            outlines.append("categories: [")
            for tag in categories:
                outlines.append("\"" + tag + "\", ")
            outlines.append("]\n")

            localaudiofname = os.path.join(audiodir, "Slow_Chinese_{:03d}.mp3".format(episode_num))
            if os.path.exists(localaudiofname):

                audiosize = os.path.getsize(localaudiofname)
                audiolength = datetime.timedelta(seconds=eyed3.load(localaudiofname).info.time_secs)
                outlines.append(
                    "file: //archive.org/download/slowchinese_201909/Slow_Chinese_{:03d}.mp3\n".format(
                        episode_num))
                outlines.append("summary: \"{}\"\n".format("".join(transcript)))
                outlines.append("duration: \"{}\"\n".format(audiolength))
                outlines.append("length: \"{}\"\n".format(audiosize))

            # # image: cutting.jpg
            outlines.append("---\n\n")
            #

            #
            # Audio Embed
            #
            if os.path.exists(localaudiofname):
                embed = "<iframe src=\"https://archive.org/embed/slowchinese_201909/Slow_Chinese_{:03d}.mp3\" width=\"500\" height=\"30\" frameborder=\"0\" webkitallowfullscreen=\"true\" mozallowfullscreen=\"true\" allowfullscreen></iframe>\n"
                embed = embed.format(episode_num)
                outlines.append(embed)


        with open(os.path.join(targetdir, date + "--" + outfname), "w") as f_out:
            f_out.writelines(outlines)
            f_out.writelines(transcript)
