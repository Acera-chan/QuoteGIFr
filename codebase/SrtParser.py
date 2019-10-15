def main():
    # demonstrate usage of SrtFile class
    fileLoc = ""
    while fileLoc != "0":
        fileLoc = input("Enter the full path to SRT you would like to parse: ")
        if fileLoc == "0":
            break
        try:
            srtTest = SrtFile(fileLoc)
            lineNum = int(input("What line would you like to see: "))
            print("Line " + str(lineNum) + "\n"
                  + srtTest.getLineStartTime(lineNum) + "-->"
                  + srtTest.getLineEndTime(lineNum) + "\n"
                  + srtTest.getLineCaption(lineNum))
        except FileNotFoundError as fnf_error:
            print(fnf_error)


class SrtFile:
    def __init__(self, srtFileDescriptor):
        inList = []
        try:
            inFile = open(srtFileDescriptor, 'r', newline="\r\n")
            inList = inFile.readlines()
            inFile.close()
            self.lines = {}
            lineNum = 0
            timeString = ""
            captionStrings = []

            intLineTracker = 1
            for line in inList:
                if intLineTracker == 1:
                    lineNum = int(line.encode('utf-8').decode('ascii', 'ignore'))  # removes formatting characters from line number
                elif intLineTracker == 2:
                    timeString = line
                elif line == '\r\n':
                    # push into SrtLine object
                    if captionStrings:  # check if anything to push
                        srtObject = SrtLine(timeString, captionStrings)
                        self.lines[lineNum] = srtObject

                        # reset collector
                        captionStrings = []
                        intLineTracker = 0
                else:  # add caption to list
                    captionStrings.append(line)
                intLineTracker = intLineTracker + 1
        except FileNotFoundError as fnf_error:
            raise fnf_error

    def getLineCaption(self, lineNum):
        return self.lines[lineNum].getCaptions()

    def getLineStartTime(self, lineNum):
        return self.lines[lineNum].getStartTime()

    def getLineEndTime(self, lineNum):
        return self.lines[lineNum].getEndTime()


class SrtLine:
    def __init__(self, timeString, captionStrings):
        self.startTime = SrtTime(timeString[0:12])  # extract first time stamp
        self.endTime = SrtTime(timeString[17:29])  # extract second time stamp
        self.captions = []
        for line in captionStrings:
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
        output = "%02d" % self.hours + ":" + "%02d" % self.minutes + ":" + "%02d" % self.seconds + "," + "%003d" % self.milliseconds
        return output


if '__main__' == __name__:
    main()
