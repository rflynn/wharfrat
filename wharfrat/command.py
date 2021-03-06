import os
import yaml
from argparse import ArgumentParser

from wharfrat.wharf_rat import WharfRat
from wharfrat.interface import issue


def create_parser():

    parser = ArgumentParser(description='Wharf-Rat is a simple tool to '
                            'convert .yml config files into docker '
                            'commands')
    parser.add_argument('-f', dest='filename')
    parser.add_argument('command')
    parser.add_argument('task')

    return parser


def get_command(args):

    commands = {
        'run': WharfRat.run
    }
    return commands[args.command]


def main(args=None):

    parser = create_parser()
    _args = parser.parse_args(args)
    translater = WharfRat.build(_args)
    command = get_command(_args)
    result = command(translater, _args.task)
    for item in result:
        issue(item)
