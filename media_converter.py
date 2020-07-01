#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys


class OutputPrinter(object):
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def print_with_color(self, color, text):
        print('%s%s%s' % (color, text, self.ENDC))

    def info(self, text):
        self.print_with_color(self.OKBLUE, text)

    def ok(self, text):
        self.print_with_color(self.OKGREEN, text)

    def warning(self, text):
        self.print_with_color(self.WARNING, text)

    def fail(self, text):
        self.print_with_color(self.FAIL, text)


class Manager(object):
    """Manages converters
    """
    converter_data = [
        {
            'name': '30_to_24',
            'file_types': ['.mov', '.mp4', '.webm', '.mkv'],
            'output_file_extension': '.mp4',
            'command': 'ffmpeg -i "{input_file_full_path}" '
                       '-crf 14 -r 24 '
                       '{extra_options} '
                       '"{output_file_full_path}"',
        },
        {
            'name': 'extract_audio',
            'file_types': ['.mov', '.mp4', '.webm', '.mkv'],
            'output_file_extension': '.wav',
            'command': 'ffmpeg -i "{input_file_full_path}" '
                       '{extra_options} '
                       '"{output_file_full_path}"',
        },
        {
            'name': 'fix_screen_capture',
            'file_types': ['.mov', '.mp4', '.webm', '.mkv'],
            'output_file_extension': '.mp4',
            'command': 'ffmpeg -i "{input_file_full_path}" '
                       '-crf 28 -flags:v "+cgop" -g 300 -acodec copy '
                       '{extra_options} '
                       '"{output_file_full_path}"',
        },
        {
            'name': 'fix_screen_capture2',
            'file_types': ['.mov', '.mp4', '.mkv'],
            'output_file_extension': '.mp4',
            'command': 'ffmpeg -i "{input_file_full_path}" '
                       '-crf 15 -acodec copy '
                       '{extra_options} '
                       '"{output_file_full_path}"',
        },
        {
            'name': 'mp4_to_mov',
            'file_types': ['.mp4'],
            'output_file_extension': '.mov',
            'command': 'ffmpeg -i "{input_file_full_path}" '
                       '-crf 15 -acodec copy '
                       '{extra_options} '
                       '"{output_file_full_path}"',
        },
        {
            'name': 'image_seq_to_mp4',
            'file_types': ['.jpg', '.jpeg', '.png', '.tga', '.tiff', '.tif', '.bmp'],
            'output_file_extension': '.mp4',
            'command': 'ffmpeg -i "{input_file_full_path}" '
                       '-vcodec libx264 -pix_fmt yuv420p -g 1 -b:v 20480k -an '
                       '{extra_options} '
                       '"{output_file_full_path}"',
        },
        {
            'name': 'mov_to_mp4',
            'file_types': ['.mov'],
            'output_file_extension': '.mp4',
            'command': 'ffmpeg -i "{input_file_full_path}" '
                       '-crf 15 -acodec copy '
                       '{extra_options} '
                       '"{output_file_full_path}"',
        },
        {
            'name': 'audio_to_aac',
            'file_types': ['.wav', '.mp3', '.m4a'],
            'output_file_extension': '.m4a',
            'command': 'ffmpeg -i "{input_file_full_path}" '
                       '-c:a aac -b:a 192k '
                       '{extra_options} '
                       '"{output_file_full_path}"'
        },
        {
            'name': 'audio_to_wav',
            'file_types': ['.wav', '.mp3', '.m4a'],
            'output_file_extension': '.wav',
            'command': 'ffmpeg -i "{input_file_full_path}" '
                       # '-c:a aac -b:a 192k '
                       '{extra_options} '
                       '"{output_file_full_path}"'
        },
        {
            'name': 'prores_to_h264_simple',
            'file_types': ['.mov', '.mp4', '.webm', '.mkv'],
            'output_file_extension': '.mp4',
            'command': 'ffmpeg -i "{input_file_full_path}" '
                       '-c:v libx264 -b:v 30000k -c:a aac -b:a 192k '
                       '{extra_options} '
                       '"{output_file_full_path}"',
        },
        {
            'name': 'youtube',
            'file_types': ['.mov', '.mp4', '.webm', '.mkv'],
            'output_file_extension': '.mp4',
            'command': 'ffmpeg -i "{input_file_full_path}" '
                       '-c:v libx264 -crf 21 -bf 2 -flags:v "+cgop" -g 12 '
                       '-profile:v high -coder ac '
                       '-pix_fmt yuv420p -c:a aac -strict 2 -b:a 192k '
                       '-r:a 48000 -movflags faststart '
                       '{extra_options} '
                       '"{output_file_full_path}"'
        },
        {
            'name': 'youtube4K',
            'file_types': ['.mov', '.mp4', '.webm', '.mkv'],
            'output_file_extension': '.mp4',
            'command': 'ffmpeg -i "{input_file_full_path}" '
                       '-c:v libx264 -crf 18 -bf 2 -flags:v "+cgop" -g 12 '
                       '-profile:v high -coder ac '
                       '-pix_fmt yuv420p -c:a aac -strict 2 -b:a 192k '
                       '-r:a 48000 -movflags faststart '
                       '-s 3840x2160 '
                       '{extra_options} '
                       '"{output_file_full_path}"'
        },
        {
            'name': 'youtube2',
            'file_types': ['.mov', '.mp4', '.webm', '.mkv'],
            'output_file_extension': '.mp4',
            'command': 'ffmpeg -i "{input_file_full_path}" '
                       '-c:v libx264 -crf 18 -bf 2 -flags:v "+cgop" -g 12 '
                       '-preset slow '
                       '-profile:v high -coder 1 '
                       '-pix_fmt yuv420p -c:a aac -bf 2 -b:a 192k '
                       '-profile:a aac_low '
                       '-r:a 48000 -movflags faststart '
                       '{extra_options} '
                       '"{output_file_full_path}"'
        },
        {
            'name': 'prores_to_h264_422_100',
            'file_types': ['.mov', '.mp4', '.webm', '.mkv'],
            'output_file_extension': '.mp4',
            'command': 'ffmpeg -i "{input_file_full_path}" '
                       '-pix_fmt "yuv422p" '
                       '-c:v libx264 '
                       '-preset medium '
                       '-b:v 100M '
                       '-c:a aac '
                       '-b:a 192K '
                       '{extra_options} '
                       '"{output_file_full_path}"'
        },
        {
            'name': 'prores_to_h264_420_100',
            'file_types': ['.mov', '.mp4', '.webm', '.mkv'],
            'output_file_extension': '.mp4',
            'command': 'ffmpeg -i "{input_file_full_path}" '
                       '-pix_fmt "yuv420p" '
                       '-c:v libx264 '
                       '-preset medium '
                       '-b:v 100M '
                       '-c:a aac '
                       '-b:a 192K '
                       '{extra_options} '
                       '"{output_file_full_path}"'
        },
        {
            'name': 'prores422lt_proxy',
            'file_types': ['.mov', '.mp4', '.webm', '.mkv'],
            'output_file_extension': '.mov',
            'command': 'ffmpeg -i "{input_file_full_path}" '
                       '-probesize 5000000 '
                       '-s 1920x1080 '
                       '-c:v prores_ks '
                       '-profile:v 1 '
                       '-q:v 20 '
                       '-vendor ap10 '
                       '-pix_fmt yuv422p9le '
                       '-preset veryslow '
                       '{extra_options} '
                       '"{output_file_full_path}"'
        },
        {
            'name': 'prores422lt',
            'file_types': ['.mov', '.mp4', '.webm', '.mkv'],
            'output_file_extension': '.mov',
            'command': 'ffmpeg -i "{input_file_full_path}" '
                       '-probesize 5000000 '
                       '-c:v prores_ks '
                       '-profile:v 1 '
                       '-q:v 11 '
                       '-vendor ap10 '
                       '-pix_fmt yuv422p9le '
                       # '-preset veryslow '
                       '-threads 16 '
                       '{extra_options} '
                       '"{output_file_full_path}"'
        },
        {
            'name': 'prores422sq',
            'file_types': ['.mov', '.mp4', '.webm', '.mkv'],
            'output_file_extension': '.mov',
            'command': 'ffmpeg -i "{input_file_full_path}" '
                       '-probesize 5000000 '
                       '-c:v prores_ks '
                       '-profile:v 2 '
                       '-q:v 5 '
                       '-vendor ap10 '
                       '-pix_fmt yuv422p9le '
                       '-preset veryslow '
                       '{extra_options} '
                       '"{output_file_full_path}"'
        },
        {
            'name': 'prores422hq',
            'file_types': ['.mov', '.mp4', '.webm', '.mkv'],
            'output_file_extension': '.mov',
            'command': 'ffmpeg -i "{input_file_full_path}" '
                       '-probesize 5000000 '
                       '-c:v prores_ks '
                       '-profile:v 3 '
                       '-q:v 5 '
                       '-vendor ap10 '
                       '-pix_fmt yuv422p9le '
                       '-preset veryslow '
                       '{extra_options} '
                       '"{output_file_full_path}"'
        },
        {
            'name': 'vr',
            'file_types': ['.mov', '.mp4', '.webm', '.mkv'],
            'output_file_extension': '.mp4',
            'command': 'ffmpeg -i "{input_file_full_path}" '
                       '-s 1920x1080 '
                       '-b:v 4000k '
                       '{extra_options} '
                       '"{output_file_full_path}"'
        },
        {
            'name': 'vr1080',
            'file_types': ['.mov', '.mp4', '.webm', '.mkv'],
            'output_file_extension': '.mp4',
            'command': 'ffmpeg -i "{input_file_full_path}" '
                       '-s 1920x1080 '
                       '-b:v 4000k '
                       '{extra_options} '
                       '"{output_file_full_path}"'
        },
        {
            'name': 'vr1440',
            'file_types': ['.mov', '.mp4', '.webm', '.mkv'],
            'output_file_extension': '.mp4',
            'command': 'ffmpeg -i "{input_file_full_path}" '
                       '-s 2560x1440 '
                       '-b:v 6000k '
                       '{extra_options} '
                       '"{output_file_full_path}"'
        },
        {
            'name': 'whatsapp',
            'file_types': ['.mov', '.mp4', '.webm', '.mkv'],
            'output_file_extension': '.mp4',
            'command': 'ffmpeg -i "{input_file_full_path}" '
                       '-c:v libx264 -crf 25 -bf 2 -flags:v "+cgop" -g 12 '
                       # '-s 1280x720 '
                       '-vf "scale=1280:-2" '
                       '-profile:v high -coder ac '
                       '-pix_fmt yuv420p -c:a aac -strict 2 -b:a 192k '
                       '-r:a 48000 -movflags faststart '
                       '{extra_options} '
                       '"{output_file_full_path}"'
        },

        #
        # denoise with hqdn3d
        # -filter:v hqdn3d=4:3:6:2
        #                  | | | |
        #                  | | | +-> ct : Chroma Temporal Strength.
        #                  | |            Defaults to: lt * cs / ls
        #                  | | +---> lt : Luma Temporal Strength.
        #                  | |            Defaults to: 6.0 * ls / 4.0
        #                  | +-----> cs : Chroma Spatial Strength.
        #                                 Defaults to: 3.0 * ls / 4.0
        #                  +-------> ls : Luma Spatial Strength.
        #                                 Defaults to: 4.0
        #
        # For extreme chroma noise reduction I've used:
        # -filter:v hqdn3d=4:40:6:60
        #
        # This has resulted trails in chroma channel. So I've reduced to
        # -filter:v hqdn3d=4:40:6:6
        #
        # https://ffmpeg.org/ffmpeg-filters.html#toc-hqdn3d-1
    ]

    def __init__(self):
        self.converters = []
        self.__initialize_converters()

    def __initialize_converters(self):
        """Creates converters
        """
        for kwargs in self.converter_data:
            converter = MediaConverter(**kwargs)

            self.converters.append(converter)

    def get_converter(self, name):
        """returns a converter by its name
        """
        for converter in self.converters:
            if converter.name == name:
                return converter

        return None

    def list_converter_names(self):
        return [c.name for c in self.converters]


class MediaConverter(object):
    """Converts between different media types
    """

    def __init__(self, **kwargs):

        name = kwargs.get('name')
        command = kwargs.get('command')
        source_path = kwargs.get('source_path')
        target_path = kwargs.get('target_path')
        output_file_extension = kwargs.get('output_file_extension')
        file_types = kwargs.get('file_types')
        extra_options = kwargs.get('extra_options')
        auto_rename = kwargs.get('auto_rename', False)

        self.name = name
        self.command = command
        self.source_path = source_path
        self.target_path = target_path
        self.output_file_extension = output_file_extension
        self._extra_options = None
        self.extra_options = extra_options
        self.auto_rename = auto_rename

        if file_types is None:
            file_types = []

        self.file_types = file_types

    @property
    def extra_options(self):
        """Add extra options.

        Setting any pre existing flags here will remove the original flag from
        the original command
        """
        return self._extra_options

    @extra_options.setter
    def extra_options(self, extra_options):
        """setter for the extra_options attribute

        :param str extra_options:
        :return:
        """
        if extra_options is not None:

            # clean the original command first
            command = self.command
            # print('original command: %s' % command)
            input_file_template = 'ffmpeg -i "{input_file_full_path}"'
            extra_options_template = ' {extra_options}'
            output_file_template = ' "{output_file_full_path}"'
            command = command.replace(input_file_template, '')
            command = command.replace(extra_options_template, '')
            command = command.replace(output_file_template, '')
            # print("kilciksiz command: %s" % command)

            # remove any occurrence of the options from the original command
            # part the original command to flag and value pairs
            flags_and_values = command.split(' -')[1:]
            # print("flags_and_values: %s" % flags_and_values)

            # now we should left with only the commands and value pairs
            # add the dash '-' sign back in to the flags_and_values
            flags_and_values = ["-%s" % x for x in flags_and_values]
            # print("flags_and_values (after adding dash): %s" % flags_and_values)
            # now for each command try to find the extra option and replace it
            if not extra_options.startswith(" "):
                extra_options = " %s" % extra_options
            extra_options_flags_and_values = extra_options.split(" -")[1:]
            # restore extra_options
            extra_options = extra_options.strip()

            # print("extra_options_flags_and_values: %s" % extra_options_flags_and_values)
            for extra_options_flag_and_value in extra_options_flags_and_values:
                # print("extra_options_flag_and_value: %s" % extra_options_flag_and_value)
                flag, value = extra_options_flag_and_value.split(" ")
                # print("flag: %s" % flag)
                # print("value: %s" % value)
                if not flag:
                    # this should be the first one skip it
                    # print("no flag! skipping")
                    continue

                # add the dash sign back
                flag = '-%s' % flag
                # now try to find the flag in flags_and_values

                new_flags_and_values = []
                for f in flags_and_values:
                    if flag in f:
                        # print("overriding %s in the original command" % f)
                        pass
                    else:
                        new_flags_and_values.append(f)
                flags_and_values = new_flags_and_values

            # now we should have filtered the original flags and values
            # recompile them to a proper command
            self.command = '%s %s%s%s' % (
                input_file_template,
                ' '.join(flags_and_values),
                extra_options_template,
                output_file_template
            )
            # print('self.command: %s' % self.command)

        self._extra_options = extra_options

    def run_per_file(self, f):
        """converts only one file
        """
        op = OutputPrinter()

        source_file_full_path = f
        op.info('source_file_full_path: %s' % source_file_full_path)

        # get file extension
        source_file_basename, source_file_extension = os.path.splitext(
            os.path.basename(f)
        )

        # remove any %03d or %04d from the source_file_basename
        import re
        source_file_basename = re.sub("\.%[0-9]+d", "", source_file_basename)
        source_file_extension = source_file_extension.lower()
        op.info("source_file_basename: %s" % source_file_basename)
        op.info("source_file_extension: %s" % source_file_extension)

        output_file_name = '%s%s' % (
            source_file_basename,
            self.output_file_extension
        )
        op.info("output_file_name: %s" % output_file_name)

        output_file_full_path = os.path.join(
            self.target_path,
            output_file_name
        )

        op.info('self.target_path: %s' % self.target_path)
        op.info('output_file_full_path: %s' % output_file_full_path)

        # do not run the command if:
        #    the file has no extension
        #    the extension is not in the right format
        #    or there is an file with the same name
        type_is_matching = True
        if self.file_types:
            if source_file_extension == '' \
               or source_file_extension not in self.file_types:
                type_is_matching = False

        if type_is_matching:
            generate_media = True
            if os.path.exists(output_file_full_path):
                if not self.auto_rename:
                    generate_media = False
                    op.warning("already exists!")
                    op.warning("skipping: %s" % source_file_full_path)
                else:
                    # generate a new name for the media
                    i = 1
                    while os.path.exists(output_file_full_path):
                        filename, ext = os.path.splitext(output_file_name)
                        new_output_filename = '%s_%i%s' % (filename, i, ext)
                        output_file_full_path = os.path.join(
                            self.target_path,
                            new_output_filename
                        )
                        i += 1

            if generate_media:
                # create the target path
                try:
                    os.makedirs(self.target_path)
                except OSError:
                    # path already exists
                    pass

                op.info("converting with: %s" % self.name)
                rendered_command = self.command.format(
                    input_file_full_path=source_file_full_path,
                    output_file_full_path=output_file_full_path,
                    extra_options=self.extra_options
                )

                op.info('rendered command: %s' % rendered_command)
                os.system(rendered_command)

        else:
            op.fail('file type is not matching: %s -> %s' %
                    (source_file_extension, self.file_types))

    def run(self):
        """runs the command
        """
        source_path = self.source_path
        if "%" in self.source_path:
            # this is an image sequence
            self.run_per_file(self.source_path)
        else:
            if os.path.isdir(source_path):
                for f in os.listdir(self.source_path):
                    self.run_per_file(os.path.join(self.source_path, f))
            elif os.path.isfile(source_path):
                self.run_per_file(self.source_path)


def main():
    """The main function
    """
    try:
        from colorama import init
        init()
    except ImportError:
        pass

    # create a manager
    manager = Manager()
    converter_names = manager.list_converter_names()

    import argparse
    parser = argparse.ArgumentParser(
        description='Batch convert media by using templates'
    )
    parser.add_argument(
        '-t', '--template', required=True,
        help='The template to use. One of: ' '%s' % ", ".join(converter_names)
    )
    parser.add_argument(
        '-i', '--input', required=False, help='The input folder or file'
    )
    parser.add_argument(
        '-o', '--output', help='The output folder, if skipped it will be same'
                               'with the input folder'
    )
    parser.add_argument(
        '-x', '--extra-options', help='Extra options', default=''
    )
    parser.add_argument(
        '-a', '--auto-rename',
        help='Auto Rename output filename if it already exists',
        action='store_true'
    )

    parser.add_argument(
        '-c', '--command-info',
        help='Print command info.',
        action='store_true'
    )

    args = parser.parse_args()

    converter_name = args.template
    source_path = args.input
    target_path = args.output
    auto_rename = args.auto_rename
    command_info = args.command_info

    if converter_name == 'get_converters':
        print(" ".join(converter_names))
        sys.exit(0)

    if target_path is None:
        if source_path:
            if "%" in source_path or os.path.isfile(source_path):
                target_path = os.path.dirname(source_path)
        else:
            target_path = source_path

    # find the converter
    converter = manager.get_converter(converter_name)
    assert isinstance(converter, MediaConverter)

    if converter:
        if command_info:
            print(converter.name)
            print(converter.command)
            return
        # do conversion
        converter.source_path = source_path
        converter.target_path = target_path
        converter.extra_options = args.extra_options.replace('\\-', '-')
        converter.auto_rename = auto_rename
        converter.run()
    else:
        print("no converter found")
        sys.exit(-1)


if __name__ == '__main__':
    main()
