#requires the installation of moviepy
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.editor import*
import subprocess
import requests
from giphypop import Giphy


#globals that will need defined for gifEngine to work
outfile = r"G:\Users\Tempest3\Documents\USCU\Fall 2019\Software Engineering\QuoteGIFr\outfile"
gifNum = 5


API_KEY = 'iTmKRrpWJUCpn6nWMSIp42gmkXA6hpfh'

#the four variables defined below are what gifEngine needs
def main():
	
	startTime = "00:04:49,934"
	endTime = "00:05:01,500"
	videoFileLoc = r"G:\Users\Tempest3\Documents\USCU\Fall 2019\Software Engineering\QuoteGIFr\MEDIA\GS_S01E01.mp4"
	strFileLoc = r"G:\Users\Tempest3\Documents\USCU\Fall 2019\Software Engineering\QuoteGIFr\MEDIA\GS_S01E01.srt"
	
	print(gifEngine(startTime, endTime, videoFileLoc, strFileLoc) + " rendered successfully")
	
	global gifNum
	uploadLoc = outfile + "\GIF_%d.gif"%gifNum
	giphyobj = Giphy(API_Key)
	response = giphyobj.upload("Get Smart, Cone of Silence", uploadLoc, username="konradwiley")

	print(response)  # gives us the url of GIF on giphy.com
	
	gifNum = gifNum + 1

#creates a gif from the videoFileLoc with subtitles from strFileLoc 
#returns the location of the GIF as a string
def gifEngine(startTime, endTime, videoFileLoc, srtFileLoc):
	
	#creating the initial GIF
	generator = lambda txt: TextClip(txt, font='Impact', fontsize=36, color='white')
	video = VideoFileClip(videoFileLoc)
	sub = SubtitlesClip(srtFileLoc, generator).set_position(("center", "bottom"), relative=True)	
	composite = CompositeVideoClip([video, sub])
	composite = composite.subclip(startTime, endTime)
	composite.write_gif(outfile + "\GIF_%d.gif"%gifNum, program='ffmpeg')
	
	return (outfile + "\GIF_%d.gif"%gifNum)	
	
if '__main__' == __name__:
    main()
