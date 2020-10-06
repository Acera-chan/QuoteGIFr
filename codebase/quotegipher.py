# requires the installation of moviepy and imagemagick
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.editor import TextClip, VideoFileClip, CompositeVideoClip
from os import listdir, path, remove
import io
import logging
import prolog


#  Creates a gif from the videoFileLoc with subtitles from strFileLoc
#  Raises IOError or OSError from moviepy/gif_writers
def gifEngine(starttime, endtime, videofileloc, srtfileloc, outfileloc, logger='gifEngine.log', width=None):
    # initializing logger
    logging.basicConfig(filename=logger, level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    prolog.basic_config()
    # creating the initial GIF
    # try/except because of file IO
    try:
        # generator is specifying format of subtitles for sub
        generator = lambda txt: TextClip(txt, font='Impact', fontsize=28, color='white')
        video = VideoFileClip(videofileloc)
        if width is not None:
            video = video.resize(width=width)
        sub = SubtitlesClip(srtfileloc, generator).set_position(("center", "bottom"), relative=True)
        # composite overlays sub onto video
        composite = CompositeVideoClip([video, sub])
        # trim clip to desired length
        composite = composite.subclip(starttime, endtime)
        # using new palettegen opt
        composite.write_gif(outfileloc, program='ffmpeg', opt='palettegen', logger=logger, verbose=True)
        return 0
    except (IOError, OSError) as err:
        return err


#  writes a single frame of a video file (at timecode) to outfileloc
def getImage(timecode, videofileloc, outfileloc):
    retcode = 0
    try:
        video = VideoFileClip(videofileloc)
        video.save_frame(outfileloc, timecode)
        video.close()
    except Exception as errCode:
        retcode = errCode

    return(retcode)


# Prunes file count in specified folder to <= desired size
def pruneGIFs(folder, desired_size):
    file_list = listdir(folder)

    while len(file_list) > desired_size:
        del_file = min(file_list, key=path.getctime)
        remove(path.abspath(del_file))


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
                    if("<i>" in line):
                        line = line.replace("<i>", "")
                    if("</i>" in line):
                        line = line.replace("</i>", "")
                    if("{{i}}" in line):
                        line = line.replace("{{i}}", "")
                    if("{{\\i}}" in line):
                        line = line.replace("{{\\i}}", "")
                    # do some parsing to avoid long lines
                    for subline in line.split(sep='\n'):
                        if len(subline) > 28:
                            linebreak = subline.find(' ', int((len(subline))/2), len(subline)-1)
                            subline = subline[:linebreak]+'\n'+subline[linebreak+1:]  # linebreak+1 removes space between words
                        if subline != '':
                            subline = subline + "\n"
                        if subline != '':
                            captionstrings.append(subline)
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
        if self.minutes < 0:
            self.minutes = self.minutes + 60
            self.hours = self.hours - 1

    #  Adds newSeconds and newMilliseconds to current time
    #  and normalizes resulting time
    def adjustTime(self, newSeconds, newMilliseconds):
        self.milliseconds = self.milliseconds + int(newMilliseconds)
        self.normalize()
        self.seconds = self.seconds + int(newSeconds)
        self.normalize()

    #  Generates a string in SRT format of HH:MM:SS,mmm
    def toString(self):
        output = "{:0>2d}:{:0>2d}:{:0>2d},{:0>3d}".format(int(self.hours), int(self.minutes), int(self.seconds), int(self.milliseconds))
        return output
