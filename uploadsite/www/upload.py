#!/usr/bin/env python

import os
import re
import cgi
import sys
import json
import time
import wave
import shutil
import cgitb; cgitb.enable(format='text')

MAX_FILE_SIZE_BYTES = 1024*300

def getClipsDir():
    clipsDir = "clips"
    if not os.path.isdir(clipsDir):
        os.mkdir(clipsDir)
    return clipsDir

def parseTime(timeStr):
    # Format of a time:
    #  M:SS.DD(D)
    actualTime = error = None
    timeRe = r"^(?:([1-9]):([0-5])|([1-5]))?(\d)\.(\d\d\d?)$"
    matches = re.match(timeRe, timeStr)
    if not matches:
        error = "Invalid time specified: %s" % timeStr
    else:
        minutes, tensSeconds, otherTensSeconds, onesSeconds, decimalPart = matches.groups()
        tensSeconds = tensSeconds or otherTensSeconds
        minutes = minutes or "0"
        tensSeconds = tensSeconds or "0"

        minutes = int(minutes)
        tensSeconds = int(tensSeconds)
        onesSeconds = int(onesSeconds)
        actualTime = 60*minutes + 10*tensSeconds + onesSeconds
        if len(decimalPart) == 2:
            actualTime += int(decimalPart) / 100.0
        else:
            actualTime += int(decimalPart) / 1000.0

    return actualTime, error

def main():
    form = cgi.FieldStorage()
    timeStr = form.getfirst("time", None)
    audioFile = form["file"] if "file" in form else None
    def sendError(error):
        print json.dumps({ "error": error })
    if timeStr is None:
        return sendError("Missing parameter: time")
    elif audioFile is None:
        return sendError("Missing parameter: file")
    elif not audioFile.file:
        return sendError("Parameter not a file: file")
    if timeStr is not None:
        actualSignal, error = parseTime(timeStr)
        if error:
            return sendError(error)

    clipsDir = getClipsDir()

    audioFile.file.seek(0, 2) # seek to end of file
    filesize = audioFile.file.tell()
    audioFile.file.seek(0) # seek back to the start
    if filesize > MAX_FILE_SIZE_BYTES:
        return sendError("Uploaded file size is %s bytes. It may not be larger than %s bytes" % ( filesize, MAX_FILE_SIZE_BYTES ))
    waveFile = wave.open(audioFile.file, "r")
    timeSeconds = (1.0 * waveFile.getnframes()) / waveFile.getframerate()
    del waveFile
    audioFile.file.seek(0) # seek back to the start

    # Note that timeStr has been sanitized, and timestamp is definitely
    # path safe. There should be no injection vulnerabilities here.
    timestamp = int(time.time())
    fileName = "%s-%s.wav" % ( timeStr, timestamp )
    destFilename = os.path.join(clipsDir, fileName)
    destFile = open(os.path.join(clipsDir, fileName), "w")
    shutil.copyfileobj(audioFile.file, destFile)
    print json.dumps({ "signalSeconds": actualSignal, "clipLength": timeSeconds })

if __name__ == "__main__":
    print "Content Type: application/json"
    print

    try:
        main()
    except:
        bt = cgitb.text(sys.exc_info())
        print json.dumps({ "error": bt })
