#!/usr/bin/env python

import os
import sys
import json
import urlparse
import cgitb; cgitb.enable(format='text')

import upload
import cgiutils

def main():
    clipsDir = upload.getClipsDir()
    files = os.listdir(clipsDir)
    jsonClips = []
    for f in files:
        time_timestamp, extension = os.path.splitext(f)
        if extension != ".wav":
            continue
        if "-" not in time_timestamp:
            # We're only interested in files of the form TIME-TIMESTAMP.wav
            continue
        time, timestamp = time_timestamp.split("-")
        timestamp = int(timestamp)
        fullerPath = os.path.join(clipsDir, f)

        scriptUri = cgiutils.getBaseURL()
        lastSlash = scriptUri.rfind("/")
        parentUri = scriptUri[:lastSlash + 1]
        url = parentUri + fullerPath
        jsonClip = {}
        jsonClip['url'] = url
        jsonClip['time'] = time
        jsonClip['timestamp'] = timestamp
        jsonClips.append(jsonClip)
    print json.dumps(jsonClips)

if __name__ == "__main__":
    print "Content Type: application/json"
    print

    try:
        main()
    except:
        bt = cgitb.text(sys.exc_info())
        print json.dumps({ "error": bt })
