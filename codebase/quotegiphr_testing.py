import unittest
from datetime import datetime
from quotegipher import gifEngine, getImage, SrtFile
import os.path


class TestQGiphrMethods(unittest.TestCase):
    def test_gifEngine(self):
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
                self.assertTrue(retcode != 0)
                self.assertFalse(os.path.isfile(gif_outfileloc))
                self.assertTrue(os.path.isfile(jpg_outfileloc))
            elif movie == "Dressed to Kill 1946":
                self.assertEqual(retcode, 0)
                self.assertTrue(os.path.isfile(gif_outfileloc))
                self.assertTrue(os.path.isfile(jpg_outfileloc))
            elif movie == "The Last Time I Saw Paris 1954":
                self.assertTrue(retcode != 0)
                self.assertFalse(os.path.isfile(gif_outfileloc))
                self.assertFalse(os.path.isfile(jpg_outfileloc))

    def test_srt_file(self):
        movieNames = ["An Ideal Husband 1947", "Dressed to Kill 1946", "The Last Time I Saw Paris 1954"]
        directory = "media/"
        for movie in movieNames:
            srtfileloc = directory + movie + ".srt"

            # An Ideal Husband is renamed and should fail to be found
            if movie == "An Ideal Husband 1947":
                with self.assertRaises(FileNotFoundError):
                    srttest = SrtFile(srtfileloc)
            elif movie == "Dressed to Kill 1946":
                srttest = SrtFile(srtfileloc)
                self.assertEqual(srttest.getNumLines(), 1358)
                self.assertEqual(srttest.getLineCaption(989), "the fifth key 'E',\r\n")
                self.assertTrue(srttest.getLineStartTime(214) == "00:11:08,120"
                                and srttest.getLineEndTime(214) == "00:11:09,700")
            elif movie == "The Last Time I Saw Paris 1954":
                srttest = SrtFile(srtfileloc)
                self.assertEqual(srttest.getNumLines(), 2016)
                self.assertEqual(srttest.getLineCaption(930), "I am Wills from the\r\n Europa News Service.\r\n")


if __name__ == '__main__':
    unittest.main()
