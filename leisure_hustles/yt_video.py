from yt_dlp import YoutubeDL
'''
This code takes up the link to the youtube video and downloads the same to
the designated folder.
'''
video_url = "link/to/youtube/video"

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': 'path/to/the/destination/%(title)s.%(ext)s',
}

with YoutubeDL(ydl_opts) as ydl:
    ydl.download([video_url])
