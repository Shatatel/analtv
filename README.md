# analtv
Primitive set of tools for video content analysis

**Requirements**
*software side of things* You'll need ffmpeg, this code and some instance empovered with Ubuntu 16.04-18.04 (tested)
*sources* We start with teletext capable streams that should be used as input as [STREAM URL], voice recognition is planned to add later.

**Usage**
**content preparing**
Let's start from raw data preparing
Navigate to the desired location in your server (cd /smth/) and execute in the command line the following:

ffmpeg -loglevel quiet -txt_format text -txt_page 888 -i [STREAM URL] -f srt -

**GOP structure check**
Sometimes you may need to analyze how group of pictures look like in particular file or stream.
That python script will assist you here.
