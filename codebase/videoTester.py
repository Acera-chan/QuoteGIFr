from giphypop import Giphy  # necessary for uploading to giphy.com
import webbrowser  # used to open giphy.com URL after upload
from datetime import datetime  # used to create filename of gif in this context
from quotegipher import gifEngine
#Giphy api_key, required for uploads
API_KEY = 'iTmKRrpWJUCpn6nWMSIp42gmkXA6hpfh'


def main():
    #the five variables defined below are what gifEngine needs
    starttime =  "00:07:21,754"
    endtime = "00:07:31,029"
    # set these to appropriate locations, eventually will be passed in from db
    videofileloc = r"G:\Users\Tempest3\Documents\USCU\Fall 2019\Software Engineering\QuoteGIFr\MEDIA\An Ideal Husband 1947.mp4"
    strfileloc = r"G:\Users\Tempest3\Documents\USCU\Fall 2019\Software Engineering\QuoteGIFr\MEDIA\An Ideal Husband 1947.srt"
    outfile = r"G:\Users\Tempest3\Documents\USCU\Fall 2019\Software Engineering\QuoteGIFr\outfile"
    
    outfileloc = (outfile+"\GIF_{}.gif").format(datetime.now().strftime("%H_%M_%S"))

    print(gifEngine(starttime, endtime, videofileloc, strfileloc,  outfileloc) + " rendered successfully")
    print("Uploading to giphy.com...")
    
    giphyobj = Giphy(API_KEY)
    response = giphyobj.upload("Get Smart, Cone of Silence", outfileloc, username="QuoteGIFr")

    webbrowser.open_new(str(response))  # shows us the GIF on giphy.com
    
if '__main__' == __name__:
    main()
