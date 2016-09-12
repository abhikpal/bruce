#!/usr/bin/env python3

import argparse
import csv
from datetime import datetime
import os
import re

__version__ = 0.2
__codename__ = 'toddler'


def get_timestamp(tm=datetime.now()):
    """Formats the time in a nice time string.
    """
    assert isinstance(tm, datetime), \
        "get_timestamp expects a datetime object."
    return tm.strftime("%Y-%m-%d_%H%M")


def generate_file_list(directory, filename=None):
    """Generates a filelist for the current directory.
    """
    if not filename:
        filename = 'filelist_{}.csv'.format(get_timestamp())
    directory_contents = os.listdir(directory)
    filelist = open(filename, 'x')
    filelist.write("filename\n")
    for item in sorted(directory_contents):
        if os.path.isfile(item):
            filelist.write("{}\n".format(item))
    filelist.close()


def batch_rename(source, data, mask):
    """Batch renames files in the `source` directory based on the
    `mask` using data from `data`
    """
    # Get the placeholder names in a tuple
    tuple_regex = re.compile(r'[@]([\w]+)')
    placeholders = tuple(tuple_regex.findall(mask))
    # Get the bare mask from the mask+placeholder string.
    # We also swap the placeholders for braces to be used with str.format().
    string_regex = re.compile(r'[@][\w]+')
    mask_string = '{}'.join(string_regex.split(mask))

    # Get the headers from the csv file
    data_reader = csv.reader(open(data))
    data_header = next(data_reader)

    assert set(data_header).issuperset(set(placeholders)), \
        "Placeholder names not recognized"
    assert 'filename' in data_header, \
        "Required column \'filename\' not found"

    # We don't know the column order in the csv file, so convert it to a list
    # of dictionaries.
    data_dictionaries = []
    for row in data_reader:
        data_dictionaries.append(dict(zip(data_header, row)))

    filename='changelog.csv'
    changelog = open(filename, 'w')
    changelog.write("filename,oldname\n")
    
    for file_data in data_dictionaries:
        filename = file_data['filename']

        source_filename = os.path.join(source, filename.replace("%44",","))
        file_info_tuple = tuple(file_data[p] for p in placeholders)
        target_filename = mask_string.format(*file_info_tuple)

        filename_nacomas=filename.replace(",","%44")
        target_filename_nacomas=target_filename.replace(",","%44")
        changelog.write('{},{}\n'.format(target_filename_nacomas,filename_nacomas))
        target_filename = os.path.join(source, target_filename.replace("%44",","))

        os.rename(source_filename, target_filename)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog="bruce",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="bruce helps you batch rename files",
        epilog="Mind if we call you 'Bruce' to keep it clear?")
    parser.add_argument(
        '-v', '--version',
        action='store_true',
        help="""
            Print version and exit.
        """)
    parser.add_argument(
        '-s', '--source',
        default='./',
        metavar="DIR",
        help="""
            Source directory for the rename operation. Defaults to the current
            directory.
        """)
    parser.add_argument(
        '-g', '--generate',
        action='store_true',
        help="""
            Generates an empty csv file (`filelist_YYYY-mm-dd_HHMM.csv`) with
            a list of all the files in the --source directory. All other
            arguments are ignored.
        """)
    parser.add_argument(
        '-r', '--revert',
        action='store_true',
        help="""
            Reverts the previous batch rename from the history in changelog.csv.
        """) 
    parser.add_argument(
                       '-m', '--mask',
                       type=str,
                       default="{filename}",
                       metavar="MASK",
                       help="""
                           Defines the formatting mask to be used while renaming files. This
                      should be a string with column headers in --data-source as
              placeholders. A placeholder is just the '@' symbol followed by
            the placeholder name.
            Example: "@author - @title (@year).pdf" is a valid renaming
            mask.
        """)
    parser.add_argument(
        '-d', '--data-source',
        default=None,
        metavar="FILENAME",
        help="""
            The comma separated value file to be used to fill in information
            in the renaming mask.
        """)
    args = parser.parse_args()

    if args.version:
        print("this is {} bruce {}".format(__codename__, __version__))
        exit()
    if args.generate:
        generate_file_list(args.source)
        exit()
    if args.revert:
        logfile_name='changelog.csv'
        if(os.path.isfile(logfile_name)):
             batch_rename(
                  source=args.source,
                  data='changelog.csv',
                  mask='@oldname')
        else:
             print('Error: Bruce cannot revert the filename changes you made. Possible causes: 1) You have made no changes. 2) The log file (changelog.csv) is gone. Good luck.')
        exit()
    if not args.data_source:
        print("No --data-source specified. Quitting.")
    else:
        batch_rename(
            source=args.source,
            data=args.data_source,
            mask=args.mask)
