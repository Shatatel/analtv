#!/usr/bin/env python
#
# This script shows GOP structure of video file. It requires ffprobe from ffmpeg set of tools. 
# It's useful for checking suitability for HLS and DASH packaging.
# Example:
# chmpd +x gop-check.py
# ./gop-check.py yourvideo.mp4
# GOP: IPPPPPPPPPPPPP 14 CLOSED
# GOP: IPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP 39 CLOSED
# GOP: IPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP 31 CLOSED
# GOP: IPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP 52 CLOSED
# GOP: IPPPPPPPPPPPPPPPPP 18 CLOSED
# GOP: IPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP 39 CLOSED
# GOP: IPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP 31 CLOSED
# GOP: IPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP 39 CLOSED
# GOP: IPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP 31 CLOSED
# GOP: IPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP 56 CLOSED
#
# Legend:
#     I: IDR Frame
#     i: i frame
#     P: p frame
#     B: b frame
# 
# I'd love to provide credits to an author, but didn't find him yet.

from __future__ import print_function
import json
import subprocess
import argparse

class BFrame(object):
    def __repr__(self, *args, **kwargs):
        return "B"
    
    def __str__(self, *args, **kwargs):
        return repr(self)

class PFrame(object):
    def __repr__(self, *args, **kwargs):
        return "P"

    def __str__(self, *args, **kwargs):
        return repr(self)

class IFrame(object):
    
    def __init__(self):
        self.key_frame = False

    def __repr__(self, *args, **kwargs):
        if self.key_frame:
            return "I"
        else:
            return "i"
        
    def __str__(self, *args, **kwargs):
        return repr(self)

class GOP(object):
    
    def __init__(self):
        self.closed = False
        self.frames = []
        
    def add_frame(self, frame):
        self.frames.append(frame)
        
        if isinstance(frame, IFrame) and frame.key_frame:
            self.closed = True
            
    def __repr__(self, *args, **kwargs):
        frames_repr = ''
        
        for frame in self.frames:
            frames_repr += str(frame)
        
        gtype = 'CLOSED' if self.closed else 'OPEN'
        
        return 'GOP: {frames} {count} {gtype}'.format(frames=frames_repr, 
                                                      count=len(self.frames), 
                                                      gtype=gtype)

parser = argparse.ArgumentParser(description='Dump GOP structure of video file')
parser.add_argument('filename', help='video file to parse')
parser.add_argument('-e', '--ffprobe-exec', dest='ffprobe_exec', 
                    help='ffprobe executable. (default: %(default)s)',
                    default='ffprobe')

args = parser.parse_args()

command = '"{ffexec}" -show_frames -print_format json "{filename}"'\
                .format(ffexec=args.ffprobe_exec, filename=args.filename)
                
response_json = subprocess.check_output(command, shell=True, stderr=None)

frames = json.loads(response_json)["frames"]


gop_count = 0
gops = []
gop = GOP()
gops.append(gop)

for jframe in frames:
    if jframe["media_type"] == "video":
        
        frame = None
        
        if jframe["pict_type"] == 'I':
            if len(gop.frames):
                # GOP open and new iframe. Time to close GOP
                gop = GOP()
                gops.append(gop)
            frame = IFrame()
            if jframe["key_frame"] == 1:
                frame.key_frame = True
        elif jframe["pict_type"] == 'P':
            frame = PFrame()
        elif jframe["pict_type"] == 'B':
            frame = BFrame()
        
        frame.json = jframe
        gop.add_frame(frame)

for gop in gops:
    print(gop)

# counter = 0
# 
# last_frame_number = None
# 
# 
# for gop in gops:
#     for frame in gop.frames:
#         current_frame_number = int(frame.json[u'coded_picture_number'])
#         print (current_frame_number)
#         
#         
#         if last_frame_number is not None:
#             difference = current_frame_number - last_frame_number
#             if difference > 1:
#                 print("Difference is: %s" % difference)
#     
#         counter += 1
#         if counter > 1000:
#             break
#         
#         last_frame_number = int(frame.json[u'coded_picture_number'])
