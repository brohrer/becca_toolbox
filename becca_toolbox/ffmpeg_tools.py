"""
Tools for working with still images and videos based on the ffmpeg library.

To make use of these, you'll need to install ffmpeg and make sure that
the ffmpeg executable is in your PATH.
https://ffmpeg.org/

Usage
-----
From an interactive python interpreter window:
>>> import becca_toolbox.ffmpeg_tools as ft
>>> ft.produce("<world package name>", "<world module name>")

From the command line:
> python -m ffmpeg_tools -p <world package name> -m <world module name> -o <ouput_file_name  # noqa: E501
"""
from __future__ import print_function

import argparse
import importlib
import os
import subprocess as sp
import sys


def make_movie(stills_directory, input_file_format='*.png',
               movie_filename='', frames_per_second=30):
    """
    Make a movie out of a sequence of still frames.

    Parameters
    ----------
    frames_per_second : int
        The number of stills that get packed into one second of video.
    input_file_format : str
        The format of the still images that are read in.
    movie_filename : str
        The filename to apply to the video file.
        Default is empty string, in which case a filename is autogenerated..
    stills_directory : str
        The relative path to the directory that contains the still images.
    """
    # Generate a movie filename if one was not provided.
    if not movie_filename:
        movie_filename = ''.join([stills_directory, os.pathsep, 'movie.mp4'])

    # Prepare the arguments for the call to ffmpeg.
    input_file_pattern = ''.join(
        ['\'', os.path.join(stills_directory, input_file_format), '\''])
    codec = 'libx264'
    command = ' '.join(['ffmpeg -framerate', str(frames_per_second),
                        '-pattern_type glob -i', input_file_pattern,
                        '-y -c:v', codec, movie_filename])
    print(command)
    # shell=True is considered a bit of a security risk, but without it
    # this cammand won't parse properly
    sp.call(command, shell=True)


def break_movie(movie_filename, stills_directory, output_file_format='.jpg'):
    """
    Create a set of numbered still images from a movie.
    Run from the directory containing the movie file.

    Parameters
    ----------
    movie_directory : str
        The relative path to the directory that contains the video file.
    movie_filename : str
        The name of the video file.
    output_file_format : str
        The format of the output still images, indicated by the suffix.
    stills_directory
        The relative path to the directory that contains the still images.
    """
    # Prepare the arguments for the call to ffmpeg
    output_files = ''.join(['%05d', output_file_format])
    output_file_pattern = os.path.join(stills_directory, output_files)

    command = ' '.join(['ffmpeg -i', movie_filename, output_file_pattern])
    print(command)
    # shell=True is considered a bit of a security risk, but without it
    # this cammand won't parse properly
    sp.call(command, shell=True)


def produce(pkg_name, mod_name, movie_name=None):
    """
    Put together a movie for world, based on frames it has already gathered.
    """
    if pkg_name is None or mod_name is None:
        print('You need to pick a Becca world module',
              'with its own installed package and \'frames\' directory.',
              'Use the --package and --module options.')
        return
    else:
        if mod_name[-3:] == '.py':
            mod_name = mod_name[:-3]
        submod_name = '.'.join([pkg_name, mod_name])
        mod = importlib.import_module(submod_name)
        World = getattr(mod, 'World')
        world = World()

    if movie_name is None:
        movie_filename = ''.join([world.log_directory, os.pathsep,
                                  world.name, '_',
                                  int(world.timestep), '.mp4'])
    else:
        movie_filename = ''.join([world.log_directory, os.pathsep,
                                  movie_name, '.mp4'])

    make_movie(world.frames_directory, movie_filename=movie_filename)


def parse(args):
    """
    Parse out command line arguments.
    """
    parser = argparse.ArgumentParser(
        description='Make and break movies for Becca.')
    parser.add_argument(
        '-p', '--package',
        help="The name of the world package to make a movie for.",
    )
    parser.add_argument(
        '-m', '--module',
        help="The name of the world module",
    )
    parser.add_argument(
        '-o', '--name',
        help="The name of the finished movie file.",
    )
    args = parser.parse_args()

    produce(args.package, args.module, args.name)


if __name__ == "__main__":
    parse(sys.argv)
