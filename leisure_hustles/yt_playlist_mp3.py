# importing packages 
from pytube import YouTube 
import os 

'''
This script allows web scraping with a specific python module, named pytube.

It takes a playlist link and downloads all the videos in the playlist as mp3
format. The format is customizable and should be altered according to the 
individual's need. 
'''

# url input from user 
yt = YouTube(str('youtube/video/link')) 

# extract only audio 
video = yt.streams.filter(only_audio=True).first() 

# check for destination to save file 
destination = 'path/to/the/destination'

# download the file 
out_file = video.download(output_path=destination) 

# save the file 
base, ext = os.path.splitext(out_file) 
new_file = base + '.mp3'
os.rename(out_file, new_file) 

# result of success 
print(yt.title + " has been successfully downloaded.")
