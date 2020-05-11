#!/usr/bin/env python
# -*- coding: utf-8 -*-


def test_extra_options_are_not_overriding_template_options():
    """testing if extra_options are overriding normal options
    """
    from media_converter import Manager, MediaConverter
    manager = Manager()
    converter = manager.get_converter('fix_screen_capture')

    assert isinstance(converter, MediaConverter)

    assert converter.command == 'ffmpeg -i "{input_file_full_path}" -crf 15 ' \
        '-an {extra_options} ' \
        '"{output_file_full_path}"'
    assert converter.extra_options is None

    # now setting the extra options with let's say -crf 20 should remove the
    # original flag from the self.command attribute
    converter.extra_options = '-crf 20'

    assert converter.command == 'ffmpeg -i "{input_file_full_path}" ' \
        '-an {extra_options} ' \
        '"{output_file_full_path}"'
    assert converter.extra_options == '-crf 20'


def test_extra_options_are_overriding_template_options():
    """testing if extra_options are overriding normal options
    """
    from media_converter import Manager, MediaConverter
    manager = Manager()
    converter = manager.get_converter('image_seq_to_mp4')

    assert isinstance(converter, MediaConverter)

    assert converter.command == 'ffmpeg -i "{input_file_full_path}" ' \
        '-vcodec libx264 -pix_fmt yuv420p -g 1 -b:v 20480k ' \
        '-an {extra_options} ' \
        '"{output_file_full_path}"'
    assert converter.extra_options is None

    # now setting the extra options with let's say -crf 20 should remove the
    # original flag from the self.command attribute
    converter.extra_options = '-pix_fmt yuv422p'

    assert converter.command == 'ffmpeg -i "{input_file_full_path}" ' \
        '-vcodec libx264 -g 1 -b:v 20480k ' \
        '-an {extra_options} ' \
        '"{output_file_full_path}"'
    assert converter.extra_options == '-pix_fmt yuv422p'


def test_extra_options_are_overriding_multiple_template_options():
    """testing if extra_options are overriding normal options
    """
    from media_converter import Manager, MediaConverter
    manager = Manager()
    converter = manager.get_converter('image_seq_to_mp4')

    assert isinstance(converter, MediaConverter)

    assert converter.command == 'ffmpeg -i "{input_file_full_path}" ' \
        '-vcodec libx264 -pix_fmt yuv420p -g 1 -b:v 20480k ' \
        '-an {extra_options} ' \
        '"{output_file_full_path}"'
    assert converter.extra_options is None

    # now setting the extra options with let's say -crf 20 should remove the
    # original flag from the self.command attribute
    converter.extra_options = '-pix_fmt yuv422p -b:v 120480k'

    assert converter.command == 'ffmpeg -i "{input_file_full_path}" ' \
        '-vcodec libx264 -g 1 ' \
        '-an {extra_options} ' \
        '"{output_file_full_path}"'
    assert converter.extra_options == '-pix_fmt yuv422p -b:v 120480k'
