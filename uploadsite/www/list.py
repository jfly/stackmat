#!/usr/bin/env python

import os
import json
import cgitb; cgitb.enable(format='text')

import upload

def main():
    clipsDir = upload.getClipsDir()
    clips = os.listdir(clipsDir)
    clips = filter(lambda f: f.endswith(".wav"), clips)
    clips = map(lambda f: os.path.join(clipsDir, f), clips)
    print json.dumps(clips)

if __name__ == "__main__":
    print "Content Type: application/json"
    print

    try:
        main()
    except:
        bt = cgitb.text(sys.exc_info())
        print json.dumps({ "error": bt })
