import io

def main():
    # demonstrate usage of SrtFile class
    fileloc = ""
    while fileloc != "0":
        fileloc = input("Enter the full path to SRT you would like to parse: ")
        outfileloc = r'G:\Users\Tempest3\Documents\USCU\Fall 2019\Software Engineering\QuoteGIFr\MEDIA\test.srt'
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


class SrtFile:
    def __init__(self, srtfiledescriptor):
        inlist = []
        try:
            infile = io.open(srtfiledescriptor, 'r', newline="\r\n", encoding='utf-8')
            inlist = infile.readlines()
            infile.close()
            self.lines = {}
            linenum = 0
            timestring = ""
            captionstrings = []

            intlinetracker = 1
            for line in inlist:
                if intlinetracker == 1:
                    linenum = int(line.encode('utf-8').decode('ascii', 'ignore'))  # removes formatting characters from line number
                elif intlinetracker == 2:
                    timestring = line
                elif line == '\r\n':
                    # push into SrtLine object
                    if captionstrings:  # check if anything to push
                        srtobject = SrtLine(timestring, captionstrings)
                        self.lines[linenum] = srtobject

                        # reset collector
                        captionstrings = []
                        intlinetracker = 0
                else:  # add caption to list
                    #do some parsing to avoid long lines
                    if len(line) > 42:
                        linebreak = line.rfind(' ', 0, 42)
                        line = line[:linebreak] + '\n' + line[linebreak+1:]  # linebreak+1 removes space between words
                    captionstrings.append(line)
                intlinetracker = intlinetracker + 1
        except FileNotFoundError as fnf_error:
            raise fnf_error

    def getLineCaption(self, linenum):
        return self.lines[linenum].getCaptions()

    def getLineStartTime(self, linenum):
        return self.lines[linenum].getStartTime()

    def getLineEndTime(self, linenum):
        return self.lines[linenum].getEndTime()
        
    def writeSRT(self, fileloc):
        with io.open(fileloc, 'w', newline='', encoding='utf-8') as f:
            f.write('\ufeff')  # add utf-8 BOM to beginning of file
            for linenum in self.lines:
                outstring = '{}\r\n{} --> {}\r\n{}\r\n'.format(linenum, self.getLineStartTime(linenum),
                self.getLineEndTime(linenum),
                self.getLineCaption(linenum))
                f.write(outstring)

class SrtLine:
    def __init__(self, timestring, captionstrings):
        self.startTime = SrtTime(timestring[0:12])  # extract first time stamp
        self.endTime = SrtTime(timestring[17:29])  # extract second time stamp
        self.captions = []
        for line in captionstrings:
            self.captions.append(line)  # add each caption line to object

    def getCaptions(self):
        # unsure if we want to make one string with newlines,
        # or return list of caption strings(current)
        seperator = ""  # this goes between each item in the outString
        outString = seperator.join(self.captions)  # joins items in list as a single string
        return outString

    def getStartTime(self):
        return self.startTime.toString()

    def getEndTime(self):
        return self.endTime.toString()


class SrtTime:
    def __init__(self, stringTime):
        self.hours = int(stringTime[0:2])
        self.minutes = int(stringTime[3:5])
        self.seconds = int(stringTime[6:8])
        self.milliseconds = int(stringTime[9:12])

    def normalize(self):
        if self.milliseconds > 999:
            self.milliseconds = self.milliseconds - 1000
            self.seconds = self.seconds + 1
        if self.seconds > 59:
            self.seconds = self.seconds - 60
            self.minutes = self.minutes + 1
        if self.minutes > 59:
            self.minutes = self.minutes - 60
            self.hours = self.hours + 1
        if self.milliseconds < 0:
            self.milliseconds = self.milliseconds + 1000
            self.seconds = self.seconds - 1
        if self.seconds < 0:
            self.seconds = self.seconds + 60
            self.minutes = self.minutes - 1

    def adjustTime(self, newSeconds, newMilliseconds):
        self.milliseconds = self.milliseconds + newMilliseconds
        self.normalize()
        self.seconds = self.seconds + newSeconds
        self.normalize()

    def toString(self):
        output = "{:0>2d}:{:0>2d}:{:0>2d},{:0>3d}".format(self.hours, self.minutes, self.seconds, self.milliseconds)
        return output


if '__main__' == __name__:
    main()
