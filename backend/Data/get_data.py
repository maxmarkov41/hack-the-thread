import yt_dlp

# import json
import re


def process_url(dynamic_url):
    ydl_opts = {
        # 'format': 'best',
        # 'outtmpl': '%(fulltitle)s-%(creator)s.%(ext)s',
        # 'outtmpl_na_placeholder': 'Null',
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "geo_bypass": True,
        # 'geo_bypass_ip_block': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # try:
        # with open('test.json','r', encoding='utf-8') as f:
        #     video_info = json.load(f)
        video_info = ydl.extract_info(dynamic_url)  # , download=False)
        title = video_info["title"]
        full_title = video_info["fulltitle"]
        description = video_info["description"]
        direct_url = dynamic_url
        link = video_info["original_url"]
        thumbnail = video_info["thumbnail"]
        hashes = re.findall(r"(#[a-zA-Z0-9]*)", description)
        # print(title)
        # print(full_title)
        # print(description)
        # print(direct_url)
        # print(link)
        # print(thumbnail)
        # print(hashes)
        # with open('test1.json','w') as f:
        #     json.dump(video_info, f, indent=4)

        return {
            # 'video_info':video_info,
            "title": title,
            "full_title": full_title,
            "description": description,
            "direct_url": direct_url,
            "link": link,
            "thumbnail": thumbnail,
            "hashes": hashes,
        }
    # except Exception as e:
    #     print(f"yt-dlp failed to process the URL: {e}")
    #     return f"yt-dlp failed to process the URL: {e}"


# x = process_url("https://www.youtube.com/shorts/veSRXLDgcSs")
# print(x)
