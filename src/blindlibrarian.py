from __future__ import print_function

import glob
import json
import os
import shutil
import urllib.parse

import requests
from docopt import docopt
from guessit import guessit

__doc__ = """blindlibrarian.

Usage:
  blindlibrarian [ --api-key=<key> ] [ --dry-run ] INPUTPATH OUTPUTPATH
  blindlibrarian -h | --help
  blindlibrarian -v | --version
  
Options:
  -h, --help            Show this screen.
  -v, --version         Show version.
  INPUTPATH             Path to movies directory to be organized.
  OUTPUTPATH            Path to directory where organized movies should be placed. Do not use same directory as in INPUTPATH.
  --dry-run             Do not modify anything, just print the information.
  --api-key=<key>       Open Movie DataBase API Key - greatly increases organization correctness and cleanliness.

"""

OMDB_URL = 'http://www.omdbapi.com/?'

EXT = (".3g2 .3gp .3gp2 .3gpp .60d .ajp .asf .asx .avchd .avi .bik .bix"
       ".box .cam .dat .divx .dmf .dv .dvr-ms .evo .flc .fli .flic .flv"
       ".flx .gvi .gvp .h264 .m1v .m2p .m2ts .m2v .m4e .m4v .mjp .mjpeg"
       ".mjpg .mkv .moov .mov .movhd .movie .movx .mp4 .mpe .mpeg .mpg"
       ".mpv .mpv2 .mxf .nsv .nut .ogg .ogm .omf .ps .qt .ram .rm .rmvb"
       ".swf .ts .vfw .vid .video .viv .vivo .vob .vro .wm .wmv .wmx"
       ".wrap .wvx .wx .x264 .xvid")

EXT = tuple(EXT.split())


def main():
    args = docopt(__doc__, version='blindlibrarian 0.1.0')
    print(args)
    inputpath = args['INPUTPATH']
    outputpath = args['OUTPUTPATH']
    dryrun = args['--dry-run'] or os.getenv('dry-run')
    apikey = args['--api-key'] or os.getenv('api-key')
    for_each_file(inputpath, lambda file, directory: organize(apikey, file, directory, outputpath, dryrun))


def organize(apikey, file, directory, output, dryrun=True):
    movie_info = guessit(file)
    ext = os.path.splitext(file)[1]
    input_file = os.path.join(directory, file)
    if ext in EXT and movie_info.get('title') is not None:

        movie_title = movie_info.get('title')

        output_path = output
        output_filename = ''

        if movie_info.get('type') == 'episode':
            omdb_info = get_omdb(apikey, movie_title, 'episode', movie_info.get('year'),
                                 season=movie_info.get('season'), episode=movie_info.get('episode'))
            movie_year = omdb_info.get('Year') or movie_info.get('year') or 'xxxx'
            output_path = os.path.join(output_path, f'{movie_title} ({movie_year})')
            movie_season = movie_info.get('season') or 'XX'
            movie_episode = movie_info.get('episode') or 'XX'
            output_path = os.path.join(output_path, f'{movie_title} ({movie_year}) Season {movie_season}')
            movie_episode_title = f'S{movie_season:02d}E{movie_episode:02d}'
            movie_episode_subtitle = omdb_info.get('Title')
            if movie_episode_subtitle:
                movie_episode_title = f'{movie_episode_title} - {movie_episode_subtitle}'
            output_filename = f'{movie_title} {movie_episode_title}{ext}'
        else:
            omdb_info = get_omdb(apikey, movie_title, 'movie', movie_info.get('year'))
            movie_title = omdb_info.get('Title') or movie_title
            movie_year = omdb_info.get('Year') or movie_info.get('year') or 'xxxx'
            movie_language = movie_info.get('language') or 'xx'
            output_path = os.path.join(output_path, f'{movie_title} ({movie_year}) [{movie_language}]')
            output_filename = f'{movie_title} ({movie_year}) [{movie_language}]{ext}'

        move_file(dryrun, input_file, output_path, output_filename)

        # also check for subtitles and other files with matching filenames and move them also
        moving_prefix = os.path.join(directory, os.path.splitext(file)[0])
        for matching_file in glob.glob(f'{moving_prefix}.*'):
            if matching_file != input_file:
                ext = os.path.splitext(matching_file)[1]
                output_filename = os.path.splitext(output_filename)[0] + ext
                move_file(dryrun, matching_file, output_path, output_filename)


def move_file(dryrun, input_file, output_path, output_filename):
    if dryrun:
        print(f'{input_file} -> {os.path.join(output_path, output_filename)}')
    else:
        os.makedirs(output_path, exist_ok=True)
        shutil.move(input_file, os.path.join(output_path, output_filename))


def for_each_file(directory, callback):
    for root, subdirs, files in os.walk(directory):
        for file in files:
            callback(file, root)


def get_omdb(apikey, title, tpe='movie', year=None, season=None, episode=None):
    if apikey:
        params = {
            'apikey': apikey,
            't': title.encode('ascii', 'ignore'),
            'type': tpe
        }
        if year:
            params['y'] = year
        if season:
            params['season'] = season
        if episode:
            params['episode'] = episode
        url = OMDB_URL + urllib.parse.urlencode(params)
        try:
            r = requests.get(url)
            if r.status_code == 200:
                if "application/json" in r.headers['content-type']:
                    return json.loads(r.text)
        except requests.exceptions.ConnectionError:
            print(f'Connection refused for {title}')
        print(f'Cannot fetch omdb info for {title}')
    return {}


main()
