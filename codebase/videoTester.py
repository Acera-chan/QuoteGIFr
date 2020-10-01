from giphypop import Giphy  # necessary for uploading to giphy.com
import webbrowser  # used to open giphy.com URL after upload
from datetime import datetime  # used to create filename of gif in this context
from quotegipher import gifEngine, getImage
import prolog

# Giphy api_key, required for uploads
API_KEY = 'iTmKRrpWJUCpn6nWMSIp42gmkXA6hpfh'


def main():
    # the five variables defined below are what gifEngine needs
    starttime = "00:57:46,129"
    endtime = "00:57:49,086"
    # set these to appropriate locations, eventually will be passed in from db
    movieNames = ["An Ideal Husband 1947"]
    directory = "media/"
    outfile = "static/outfile/"
    for movie in movieNames:
        print(movie)
        videofileloc = directory + movie + ".mp4"
        srtfileloc = directory + movie + ".srt"
        gif_outfileloc = (outfile+"GIF_{}.gif").format(datetime.now().strftime("%H_%M_%S"))
        jpg_outfileloc = (outfile+"JPG_{}.jpg").format(datetime.now().strftime("%H_%M_%S"))

        getImage(starttime, videofileloc, jpg_outfileloc)
        retcode = gifEngine(starttime, endtime, videofileloc, srtfileloc,  gif_outfileloc, width=480)

        print(retcode)
    # print("Uploading to giphy.com...")

    # giphyobj = Giphy(API_KEY)
    # response (below) is the URL for our giphy upload
    # response = giphyobj.upload(["An Ideal Husband, Never marry a man with a future"], gif_outfileloc, username="QuoteGIFr")

    # webbrowser.open_new(str(response))  # shows us the GIF on giphy.com


if __name__ == '__main__':
    main()
