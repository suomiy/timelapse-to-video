# Timelapse to Video

## Installation
- Install [ffmpeg](http://ffmpeg.org/) with [libx265 support](https://trac.ffmpeg.org/wiki/Encode/H.265#Gettingffmpegwithlibx265support) (for `--x265` option)
- `pip install astral` (pip3)
- Install [python 3](https://www.python.org/downloads/)
- `git clone https://github.com/suomiy/timelapse-to-video`
- Make symbolic link `timelapse-to-video.py -> timelapse-to-video`

## Usage

Basic usage which skips uneventful images and renders video with 60 images per second

```bash
timelapse-to-video --skip_over_exposed_images \
  --skip_dark_images \
  -framerate 60 \
  sunflower_dir/ sunflower.mkv
```

Set geographical location and skip images without any natural light which depends on sun's position

```bash
timelapse-to-video --skip_images_without_natural_light \
  --latitude "51.5074" \
  --longitude "0.1278" \
  --elevation 35 \
  --timezone "Europe/London" \
  sunflower_dir/ sunflower
```

Use x265 encoder with a [preset](https://x265.readthedocs.io/en/default/presets.html) for higher quality/compression
```bash
timelapse-to-video --x265 5 sunflower_dir/ sunflower
```

### Help
```
usage: timelapse-to-video.py [OPTIONS] INPUT_DIR OUTPUT

 - creates timelapse from series of images from INPUT_DIR
 - images have to be numbered in "abc123.jpg" format
 - skip unfitting images with "-w" "-b" "-n" options

positional arguments:
  INPUT_DIR             input directory with images
  OUTPUT                output file which will be saved in mkv format

optional arguments:
  -h, --help            show this help message and exit
  -w, --skip_over_exposed_images
                        slows down the processing
  -b, --skip_dark_images
                        slows down the processing.
  -n, --skip_images_without_natural_light
                        skip images before dawn and after dusk.
  -o [DAWN_DUSK_OFFSET], --skip_images_without_natural_light_offset [DAWN_DUSK_OFFSET]
                        e.g 5 skips images 5 minutes after dusk and 5 minutes
                        before dawn (default 15).
  -f [FRAMERATE], --framerate [FRAMERATE]
                        how many images per second should be rendered (default
                        30).
  -a [AUDIO_FILE], --audio [AUDIO_FILE]
                        audio file for the video
  -s [AUDIO_START], --audio_start [AUDIO_START]
                        where should the audio start (default 0.0)
  -e [IMAGE_EXTENSION], --extension [IMAGE_EXTENSION]
                        input images extension (default jpg).
  -x [ENCODING_QUALITY], --x265 [ENCODING_QUALITY]
                        use x265 encoder with preset 0-8
                        (ultrafast:low_quality-veryslow:high_quality) (default
                        x264 encoder with preset 5 ).
  -z [LAST_FRAME_FREEZE], --last-frame-freeze [LAST_FRAME_FREEZE]
                        freeze last frame of video (default 0.0 sec)
  -l [LATITUDE], --latitude [LATITUDE]
                        needed for "-n" option; used for calculating sun's
                        position (default 49.1951).
  -g [LONGITUDE], --longitude [LONGITUDE]
                        needed for "-n" option; used for calculating sun's
                        position (default 16.6068).
  -v [ELEVATION], --elevation [ELEVATION]
                        needed for "-n" option; used for calculating sun's
                        position (default 237); in meters.
  -t [TIMEZONE], --timezone [TIMEZONE]
                        needed for "-n" option; used for calculating sun's
                        position (default Europe/Prague).
  -j [THREADS], --jobs [THREADS]
                        default 8.
```

note: you can also write your options to `DefaultSettings` in `util/settings.py` :)


There is also a short script `add-audio-to-video.py` just for changing the audio track.

```
usage: add-audio-to-video.py [OPTIONS] VIDEO_INPUT AUDIO_INPUT OUTPUT

 - adds audio from AUDIO_INPUT to VIDEO_INPUT

positional arguments:
  VIDEO_INPUT           video file
  AUDIO_INPUT           audio file
  OUTPUT                output file which will be saved in mkv format

optional arguments:
  -h, --help            show this help message and exit
  -s [AUDIO_START], --audio_start [AUDIO_START]
                        where should the audio start (default 0.0)
  -j [THREADS], --jobs [THREADS]
                        default 8.
```
