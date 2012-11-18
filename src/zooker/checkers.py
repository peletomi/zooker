#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import os
import mimetypes
import re
import subprocess


def is_text(path):
    known_extensions = [
        'sql',
        'sql_diff',
        'properties',
        'tex',
        'md',
        'py',
    ]
    known_files = ['.gitignore', 'README']

    mimetype, encoding = mimetypes.guess_type(path, False)
    if mimetype:
        return 'text' in mimetype or 'xml' in mimetype

    filename = os.path.basename(path)
    extension = os.path.splitext(path)[1]
    if extension:
        extension = extension.replace('.', '')

    if filename in known_files or extension in known_extensions:
        return True

    return False


class Checker:

    def set_config(self, config):
        self.config = config

    def get_name(self):
        return self.__class__.__name__

    def get_documentation(self):
        return self.__doc__

    def get_documentation_url(self):
        return ''

    def matches(self, change):
        """
        Returns true if the checker is able to handle this type of change.
        """

        return False

    def do_check(self, change):
        """
        Returns a list of strings describing the errors, otherwise returns an empty list.
        """

        return []

    def check(self, change):
        if change and self.matches(change):
            logging.debug('%s checking %s', self.__class__.__name__, change.repo_path)
            result = self.do_check(change)
            if result:
                return result

        return []


class CodeValidatorChecker(Checker):

    def matches(self, change):
        return change.temp_path

    def do_check(self, change):
        args = 'codevalidator.py -v %s' % change.temp_path
        results = []
        proc = subprocess.Popen(args.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out, stderr = proc.communicate()
        if out:
            results.append(out.rstrip())
        return results


class WhiteSpaceChecker(Checker):

    """
    This checker verifies common whitespace problems:

    * tabs in text files instead of spaces
    * lines with only whitespace
    * trailing whitespace
    """

    def __init__(self):
        self.empty_line = re.compile('\s+$')

    def matches(self, change):
        return change.temp_path and is_text(change.temp_path)

    def do_check(self, change):
        result = []
        with open(change.temp_path, 'r') as f:
            i = 0
            for line in f:
                line = line.rstrip('\n')
                i += 1
                if self.empty_line.match(line):
                    result.append('[%s:%s] empty line with whitespace' % (change.filename, i))
                elif line.endswith(' ') or line.endswith('\t'):
                    result.append('[%s:%s] trailing whitespace' % (change.filename, i))
                if line.find('\t') > -1:
                    result.append('[%s:%s] tabs' % (change.filename, i))
        return result


__checkers = {'CodeValidatorChecker': CodeValidatorChecker, 'WhiteSpaceChecker': WhiteSpaceChecker}


def create_checkers(config):
    """
    Creates checkers from the config dictionary. The 'list' of checkers is taken from the 'checkers' dict key.
    The keys in this should be the names of the checkers, the values are the config options passed to the instantiated
    checker. If the config option is a list, then for each item in the list a checker of that type will be instantiated
    with the item passed as config value.
    """

    checkers = []
    if 'checkers' in config:
        for checker_name, checker_config in config['checkers'].iteritems():
            if checker_name in __checkers:
                configs = None
                if type(checker_config) == list:
                    configs = checker_config
                else:
                    configs = [checker_config]
                for config in configs:
                    ch = __checkers[checker_name]()
                    ch.set_config(config)
                    if ch:
                        checkers.append(ch)
    return checkers


def list_checkers():
    return __checkers.values()


