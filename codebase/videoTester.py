#requires the installation of moviepy and imagemagick
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.editor import*
import subprocess

from giphypop import Giphy  # necessary for uploading to giphy.com
import webbrowser  # used to open giphy.com URL after upload
from datetime import datetime  # used to create filename of gif in this context


#globals that will need defined for gifEngine to work


#Giphy api_key, required for uploads
API_KEY = 'iTmKRrpWJUCpn6nWMSIp42gmkXA6hpfh'

#the four variables defined below are what gifEngine needs
def main():
    
    starttime = "00:04:49,934"
    endtime = "00:05:01,500"
    # set these to appropriate locations, eventually will be passed in from db
    videofileloc = r"G:\Users\Tempest3\Documents\USCU\Fall 2019\Software Engineering\QuoteGIFr\MEDIA\GS_S01E01.mp4"
    strfileloc = r"G:\Users\Tempest3\Documents\USCU\Fall 2019\Software Engineering\QuoteGIFr\MEDIA\GS_S01E01.srt"
    outfile = r"G:\Users\Tempest3\Documents\USCU\Fall 2019\Software Engineering\QuoteGIFr\outfile"
    
    outfileloc = (outfile+"\GIF_{}.gif").format(datetime.now().strftime("%H_%M_%S"))

    print(gifEngine(starttime, endtime, videofileloc, strfileloc,  outfileloc) + " rendered successfully")
    print("Uploading to giphy.com...")
    
    giphyobj = Giphy(API_KEY)
    response = giphyobj.upload("Get Smart, Cone of Silence", outfileloc, username="QuoteGIFr")

    webbrowser.open_new(str(response))  # shows us the GIF on giphy.com
    

#creates a gif from the videoFileLoc with subtitles from strFileLoc 
#returns the location of the GIF as a string
def gifEngine(starttime, endtime, videofileloc, srtfileloc, outfileloc):
    
    #creating the initial GIF
    generator = lambda txt: TextClip(txt, font='Impact', fontsize=28, color='white')
    video = VideoFileClip(videofileloc)
    sub = SubtitlesClip(srtfileloc, generator).set_position(("center", "bottom"), relative=True)	
    composite = CompositeVideoClip([video, sub])
    composite = composite.subclip(starttime, endtime)
    composite.write_gif(outfileloc, program='ffmpeg', opt='palettegen')
    
    return (outfileloc)	
    
if '__main__' == __name__:
    main()
