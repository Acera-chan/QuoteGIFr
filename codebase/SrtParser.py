from quotegipher import SrtFile  # Custom class for parsing and manipulating SRTs

def main():
    # demonstrate usage of SrtFile class
    fileloc = ""
    while fileloc != "0":
        fileloc = input("Enter the full path to SRT you would like to parse: ")
        outfileloc = r'G:\Users\Tempest3\Documents\USCU\Fall 2019\Software Engineering\QuoteGIFr\MEDIA\The Last Time I Saw Paris 1954.srt'
        if fileloc == "0":
            break
        try:
            srttest = SrtFile(fileloc)
            srttest.writeSRT(outfileloc)
            linenum = int(input("What line would you like to see: "))
            print("Line " + str(linenum) + "\n"
                  + srttest.getLineStartTime(linenum) + "-->"
                  + srttest.getLineEndTime(linenum) + "\n"
                  + srttest.getLineCaption(linenum))
        except FileNotFoundError as fnf_error:
            print(fnf_error)

if '__main__' == __name__:
    main()
