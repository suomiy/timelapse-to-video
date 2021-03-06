import argparse
from settings.timelapse_settings import Settings, DefaultSettings
from arg_parses.utils import positive_float, positive_int, proccess_dir, proccess_file, proccess_filename, \
    resolve_encoding, x265_preset_int


class ArgParser:
    @staticmethod
    def require_args():
        parser = argparse.ArgumentParser(usage='timelapse-to-video.py [OPTIONS] INPUT_DIR OUTPUT\n'
                                               '\n'
                                               ' - creates timelapse from series of images from INPUT_DIR\n'
                                               ' - images have to be numbered in "abc123.jpg" format\n'
                                               ' - skip unfitting images with "-w" "-b" "-n" options')
        parser.add_argument('INPUT_DIR', help=f'input directory with images')
        parser.add_argument('OUTPUT', help=f'output file which will be saved in mkv format')

        parser.add_argument('-w', '--skip_over_exposed_images', action='store_true',
                            dest='skip_over_exposed_images',
                            help=f'slows down the processing')
        parser.add_argument('-b', '--skip_dark_images', action='store_true', dest='skip_dark_images',
                            help=f'slows down the processing.')
        parser.add_argument('-n', '--skip_images_without_natural_light', action='store_true',
                            dest='skip_images_without_natural_light',
                            help=f'skip images before dawn and after dusk.')
        parser.add_argument('-o', '--skip_images_without_natural_light_offset', type=int, nargs='?',
                            dest='dawn_dusk_offset',
                            required=False, const=True, default=DefaultSettings.dawn_dusk_offset,
                            help=f'e.g 5 skips images 5 minutes after dusk and 5 minutes before dawn (default {DefaultSettings.dawn_dusk_offset}).')

        parser.add_argument('-f', '--framerate', type=positive_int, nargs='?',
                            dest='framerate',
                            required=False, const=True, default=DefaultSettings.framerate,
                            help=f'how many images per second should be rendered (default {DefaultSettings.framerate}).')

        parser.add_argument('-a', '--audio', type=str, nargs='?',
                            dest='audio_file',
                            required=False, const=True, default=DefaultSettings.audio_file,
                            help=f'audio file for the video')
        parser.add_argument('-s', '--audio_start', type=positive_float, nargs='?',
                            dest='audio_start',
                            required=False, const=True, default=DefaultSettings.audio_start,
                            help=f'where should the audio start (default {DefaultSettings.audio_start})')

        parser.add_argument('-e', '--extension', type=str, nargs='?',
                            dest='image_extension',
                            required=False, const=True, default=DefaultSettings.image_extension,
                            help=f'input images extension (default {DefaultSettings.image_extension}).')

        parser.add_argument('-x', '--x265', type=x265_preset_int, nargs='?',
                            dest='encoding_quality',
                            required=False, const=True, default=None,
                            help=f'use x265 encoder with preset 0-8 (ultrafast:low_quality-veryslow:high_quality) (default {DefaultSettings.encoder} encoder with preset {DefaultSettings.encoding_quality} ).')

        parser.add_argument('-z', '--last-frame-freeze', type=positive_float, nargs='?',
                            dest='last_frame_freeze',
                            required=False, const=True, default=DefaultSettings.last_frame_freeze,
                            help=f'freeze last frame of video (default {DefaultSettings.last_frame_freeze} sec)')

        parser.add_argument('-l', '--latitude', type=float, nargs='?',
                            dest='latitude',
                            required=False, const=True, default=DefaultSettings.latitude,
                            help=f'needed for "-n" option; used for calculating sun\'s position (default {DefaultSettings.latitude}).')
        parser.add_argument('-g', '--longitude', type=float, nargs='?',
                            dest='longitude',
                            required=False, const=True, default=DefaultSettings.longitude,
                            help=f'needed for "-n" option; used for calculating sun\'s position (default {DefaultSettings.longitude}).')
        parser.add_argument('-v', '--elevation', type=float, nargs='?',
                            dest='elevation',
                            required=False, const=True, default=DefaultSettings.elevation,
                            help=f'needed for "-n" option; used for calculating sun\'s position (default {DefaultSettings.elevation}); in meters.')
        parser.add_argument('-t', '--timezone', nargs='?',
                            dest='timezone',
                            required=False, const=True, default=DefaultSettings.timezone,
                            help=f'needed for "-n" option; used for calculating sun\'s position (default {DefaultSettings.timezone}).')

        parser.add_argument('-j', '--jobs', type=positive_int, nargs='?',
                            dest='threads',
                            required=False, const=True, default=DefaultSettings.threads,
                            help=f'default {DefaultSettings.threads}.')

        args = parser.parse_args()

        return ArgParser._as_settings(args)

    @staticmethod
    def _as_settings(args):
        input_dir = proccess_dir(args.INPUT_DIR, args.image_extension)
        output_file = proccess_filename(args.OUTPUT, DefaultSettings)
        encoder, encoding_quality = resolve_encoding(args.encoding_quality, DefaultSettings)

        audio_file = proccess_file(args.audio_file)

        return Settings(
            skip_over_exposed_images=args.skip_over_exposed_images,
            skip_dark_images=args.skip_dark_images,
            skip_images_without_natural_light=args.skip_images_without_natural_light,
            input_dir=input_dir,
            output_filename=output_file,
            audio_file=audio_file,
            audio_start=args.audio_start,
            image_extension=args.image_extension,
            framerate=args.framerate,
            latitude=args.latitude,
            longitude=args.longitude,
            elevation=args.elevation,
            timezone=args.timezone,
            dawn_dusk_offset=args.dawn_dusk_offset,
            threads=args.threads,
            encoder=encoder,
            encoding_quality=encoding_quality,
            last_frame_freeze=args.last_frame_freeze,
        )
