# -*- coding: utf-8 -*-
# -- This file is part of the Apio project
# -- (C) 2016 FPGAwars
# -- Author Juan González, Jesús Arroyo
# -- Licence GPLv2

import sys
import json
import click

from os.path import isfile, join, dirname

# -- Project file name
PROJECT_FILENAME = 'apio.ini'


class Project(object):

    def __init__(self):
        self.board = None

    def create_sconstruct(self, project_dir=''):
        """Creates a default SConstruct file"""

        if project_dir is None:
            project_dir = ''
        sconstruct_name = 'SConstruct'
        sconstruct_path = join(project_dir, sconstruct_name)
        local_sconstruct_path = join(
            dirname(__file__), '..', 'resources', sconstruct_name)

        if isfile(sconstruct_path):
            click.secho('Warning: ' + sconstruct_name + ' file already exists',
                        fg='yellow')
            if click.confirm('Do you want to replace it?'):
                self._copy_file(sconstruct_name, sconstruct_path,
                                local_sconstruct_path)
        else:
            self._copy_file(sconstruct_name, sconstruct_path,
                            local_sconstruct_path)

    def _copy_file(self, sconstruct_name,
                   sconstruct_path, local_sconstruct_path):
        click.secho('Creating ' + sconstruct_name + ' file ...')
        with open(sconstruct_path, 'w') as sconstruct:
            with open(local_sconstruct_path, 'r') as local_sconstruct:
                sconstruct.write(local_sconstruct.read())
                click.secho(
                    'File \'' + sconstruct_name +
                    '\' has been successfully created!',
                    fg='green')

    def new_ini(self, board, project_dir=''):
        """Creates a new apio project file"""

        if project_dir is None:
            project_dir = ''

        # -- Creates the project dictionary
        project = {"board": board}

        # -- Dump the project into the apio.ini file
        project_str = json.dumps(project)

        project_path = join(project_dir, PROJECT_FILENAME)

        with open(project_path, 'w') as f:
            f.write(project_str)
        f.closed

        print("{} file created".format(PROJECT_FILENAME))

    def read(self):
        """Read the project config file"""

        # -- If no project finel found, just return
        if not isfile(PROJECT_FILENAME):
            print("Info: No apio.ini file")
            return

        # -- Open the project file
        with open(PROJECT_FILENAME, 'r') as f:
            project_str = f.read()

        # -- Decode the jsonj
        try:
            project = json.loads(project_str)
        except:
            print("Error: Invalid {} project file".format(PROJECT_FILENAME))
            sys.exit(1)

        # -- TODO: error checking

        # -- Update the board
        try:
            self.board = project['board']
        except:
            print("Error: Invalid {} project file".format(PROJECT_FILENAME))
            print("No 'board' field defined in project file")
            sys.exit(1)