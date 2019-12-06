# a simple script for shifting the timestamps in an SRT by timeDiff seconds
from quotegipher import SrtTime

def main():
    inFile = open(r"G:\Users\Tempest3\Documents\USCU\Fall 2019\Software Engineering\QuoteGIFr\MEDIA\The-Last-Time-I-Saw-Paris.srt", 'r', newline="\r\n")
    outFile = open(r"G:\Users\Tempest3\Documents\USCU\Fall 2019\Software Engineering\QuoteGIFr\MEDIA\The-Last-Time-I-Saw-Paris-Copy.srt", 'w+', newline='')

    # Because the srt's were somehow not lining up evenly,
    # I added the following offset. Simply input how far off the
    # subtitles are in the beginning and the end, plus what the 
    # final line header is (integer near the end of the SRT) and
    # the program will stretch the subtitles to fit.

    # ====Set values between these lines====
    totalLines = 1499  # number of line headers in srt # <---- ENTER THIS

    # Negative values are allowed in following positions
    startTimeDiffMilli = 600  # <---- ENTER THIS
    startTimeDiffSec = -16  # <---- ENTER THIS

    endTimeDiffMilli = 590  # <---- ENTER THIS
    endTimeDiffSec = -18  # <---- ENTER THIS
    # ======================================
    timeDiffSec = 0  # these values are going to be set later,
    timeDiffMilli = 0  # don't put custom values here

    elapsedLines = 1
    percentLines = elapsedLines / totalLines  # initial percentage of endTime offset

    intLine = 1  # used to track line headers
    inList = inFile.readlines()
    inFile.close()  # closing because we don't need it anymore
    outString = ""
    for line in inList:
        if intLine == 2:
            t1 = SrtTime(line[0:12])  # grab first timestamp
            t2 = SrtTime(line[17:29])  # grab second timestamp

            timeDiffSec = (startTimeDiffSec * (1 - percentLines)) + (endTimeDiffSec * percentLines)
            timeDiffMilli = (startTimeDiffMilli * (1 - percentLines)) + (endTimeDiffMilli * percentLines)
            # shift time in srtTime objects
            t1.adjustTime(timeDiffSec, timeDiffMilli)
            t2.adjustTime(timeDiffSec, timeDiffMilli)
            outString = t1.toString() + " --> " + t2.toString() + "\r\n"
        elif line == '\r\n':
            intLine = 0
            outString = line
            elapsedLines = elapsedLines + 1
            percentLines = elapsedLines / totalLines
        else:
            outString = line
        outFile.write(outString)
        intLine = intLine + 1

    outFile.close()

if '__main__' == __name__:
    main()
