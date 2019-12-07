from giphypop import Giphy  # necessary for uploading to giphy.com
import webbrowser  # used to open giphy.com URL after upload
from datetime import datetime  # used to create filename of gif in this context
from quotegipher import gifEngine, getImage
import prolog

# Giphy api_key, required for uploads
API_KEY = 'iTmKRrpWJUCpn6nWMSIp42gmkXA6hpfh'


def main():
    # the five variables defined below are what gifEngine needs
    starttime = "00:03:50,975"
    endtime = "00:03:57,054"
    # set these to appropriate locations, eventually will be passed in from db
    movieNames = ["An Ideal Husband 1947", "Dressed to Kill 1946", "The Last Time I Saw Paris 1954"]
    directory = "media/"
    outfile = "static/outfile/"
    for movie in movieNames:
        videofileloc = directory + movie + ".mp4"
        srtfileloc = directory + movie + ".srt"
        gif_outfileloc = (outfile+"GIF_{}.gif").format(datetime.now().strftime("%H_%M_%S"))
        jpg_outfileloc = (outfile+"JPG_{}.jpg").format(datetime.now().strftime("%H_%M_%S"))

        getImage(starttime, videofileloc, jpg_outfileloc)
        retcode = gifEngine(starttime, endtime, videofileloc, srtfileloc,  gif_outfileloc)

        # The Last Time I Saw Paris.mp4 is renamed and should fail to be found.
        # An Ideal Husband.srt is renamed and should fail to be found.
        if movie == "An Ideal Husband 1947":
            assert retcode != 0
        elif movie == "Dressed to Kill 1946":
            assert retcode == 0
        elif movie == "The Last Time I Saw Paris 1954":
            assert retcode != 0

    # print("Uploading to giphy.com...")

    # giphyobj = Giphy(API_KEY)
    # response (below) is the URL for our giphy upload
    # response = giphyobj.upload(["An Ideal Husband, Never marry a man with a future"], gif_outfileloc, username="QuoteGIFr")

    # webbrowser.open_new(str(response))  # shows us the GIF on giphy.com


if __name__ == '__main__':
    main()
