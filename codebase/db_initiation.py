from app import db, Movie, Timestamp
import io

""" class Movie(db.Model):
    def __init__(self, uid, title):
        self.uid = uid
        self.title = title
    __tablename__ = 'movie'
    uid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    timestamps = db.relationship("Timestamp", back_populates='movie')


class Timestamp(db.Model):
    def __init__(self, uid, subtitle, timestamp, movieid):
        self.uid = uid
        self.subtitle = subtitle
        self.timestamp = timestamp
        self.movieid = movieid
    __tablename__ = 'timestamp'
    uid = db.Column(db.Integer, primary_key=True)
    subtitle = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.String(100), nullable=False)
    movieid = db.Column(db.Integer, db.ForeignKey('movie.uid'))
    movie = db.relationship("Movie", back_populates='movie') """


#  Class for parsing and manipulating text stored in an SRT format
class SrtFile:

    #  Constructor reads in an SRT and builds
    #  class structures from SRT fields
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
                    if len(line) > 44:
                        linebreak = line.find(' ', int(len(line)/2), len(line)-1)
                        line = line[:linebreak] + '\n' + line[linebreak+1:]  # linebreak+1 removes space between words
                    captionstrings.append(line)
                intlinetracker = intlinetracker + 1
        except FileNotFoundError as fnf_error:
            raise fnf_error

    #  returns a caption (String) associated with a line number
    #  in the original SRT
    def getLineCaption(self, linenum):
        return self.lines[linenum].getCaptions()

    def getLineStartTime(self, linenum):
        return self.lines[linenum].getStartTime()

    def getLineEndTime(self, linenum):
        return self.lines[linenum].getEndTime()

    def getNumLines(self):
        return len(self.lines)

    def writeSRT(self, fileloc):
        with io.open(fileloc, 'w', newline='', encoding='utf-8') as f:
            f.write('\ufeff')  # add utf-8 BOM to beginning of file
            for linenum in self.lines:
                outstring = '{}\r\n{} --> {}\r\n{}\r\n'.format(linenum,
                    self.getLineStartTime(linenum),
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

    #  Resolves time overflows, so all values
    #  fit in their contexts (eg., minutes < 60)
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

    #  Adds newSeconds and newMilliseconds to current time
    #  and normalizes resulting time
    def adjustTime(self, newSeconds, newMilliseconds):
        self.milliseconds = self.milliseconds + newMilliseconds
        self.normalize()
        self.seconds = self.seconds + newSeconds
        self.normalize()

    #  Generates a string in SRT format of HH:MM:SS,mmm
    def toString(self):
        output = "{:0>2d}:{:0>2d}:{:0>2d},{:0>3d}".format(self.hours, self.minutes, self.seconds, self.milliseconds)
        return output


#srt_file = SrtFile("media/The Last Time I Saw Paris 1954.srt")

"""for key in srt_file.lines:
    subtitle = srt_file.getLineCaption(key)
    start_time = srt_file.getLineStartTime(key)
    end_time = srt_file.getLineEndTime(key)
    timestamp = Timestamp(startime = start_time, endtime = end_time, subtitle = subtitle, movieid = 3)
    db.session.add(timestamp)
    db.session.commit()"""
