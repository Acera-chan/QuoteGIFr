from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.editor import*
import subprocess

#requires the installation of ImageMagick and moviepy

#globals that will need defined for gifEngine to work
outfile = r"G:\Users\Tempest3\Documents\USCU\Fall 2019\Software Engineering\QuoteGIFr\outfile"
gifNum = 5
IMAGEMAGICK_BINARY = r"C:\Program Files\ImageMagick-7.0.8-Q16\magick.exe"

#the four variables defined below are what gifEngine needs
def main():
	
	startTime = "00:04:49,934"
	endTime = "00:05:01,500"
	videoFileLoc = r"G:\Users\Tempest3\Documents\USCU\Fall 2019\Software Engineering\QuoteGIFr\MEDIA\GS_S01E01.mp4"
	strFileLoc = r"G:\Users\Tempest3\Documents\USCU\Fall 2019\Software Engineering\QuoteGIFr\MEDIA\GS_S01E01.srt"
	
	print(gifEngine(startTime, endTime, videoFileLoc, strFileLoc) + " rendered successfully")
	
	global gifNum
	gifNum = gifNum + 1

#creates a gif from the videoFileLoc with subtitles from strFileLoc 
#returns the location of the GIF as a string
def gifEngine(startTime, endTime, videoFileLoc, srtFileLoc):
	#arguments for ImageMagick systemcall
	args = []
	args.append(IMAGEMAGICK_BINARY)
	args.append(outfile + "\GIF_%d.gif"%gifNum)
	args.extend(("-fuzz","5%","-layers","optimizeplus","-colors","24"))
	args.append(outfile + "\GIF_%d.gif"%gifNum)
	
	#creating the initial GIF
	generator = lambda txt: TextClip(txt, font='Impact', fontsize=36, color='white')
	video = VideoFileClip(videoFileLoc)
	sub = SubtitlesClip(srtFileLoc, generator).set_position(("center", "bottom"), relative=True)	
	composite = CompositeVideoClip([video, sub])
	composite = composite.subclip(startTime, endTime)
	#composite.write_videofile("outfile.webm", audio='False')
	composite.write_gif(outfile + "\GIF_%d.gif"%gifNum, program='ImageMagick', fuzz=40)
	
	#composite.write_gif(outfile + "\GIF_%d.gif"%gifNum)

	#proc = subprocess.Popen(args)
	#print("Compressing GIF, please wait...")
	#proc.wait()
	return (outfile + "\GIF_%d.gif"%gifNum)	
	
if '__main__' == __name__:
    main()
