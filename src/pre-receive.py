#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import tempfile
import shutil
import argparse
import os
import logging

from zooker.gitutil import GitRepo, retrieve_changed_files
from zooker.checkers import create_checkers
from zooker.config import Config

LOG_CONSOLE_FORMAT = '%(asctime)-15s %(levelname)s %(name)s: %(message)s'


def check(checkers):
    errors = {}
    for checker in checkers:
        for change in changes:
            try:
                curr_errors = checker.check(change)
                if curr_errors:
                    if checker not in errors:
                        errors[checker] = []
                    errors[checker].extend(curr_errors)
            except Exception, e:
                if checker not in errors:
                    errors[checker] = []
                errors[checker].append('checker [%s] had an unexpected error: %s' % (checker, e))
    return errors


def get_config():
    global parser, args, config
    parser = argparse.ArgumentParser(description='Pre receive hook for git repositories.')
    parser.add_argument('--dry-run', action='store_true', default=False, help='only log problems')
    parser.add_argument('--logfile', default=os.path.join(tempfile.gettempdir(), 'zooker.log'),
                        help='full path of the logfile')
    parser.add_argument('-c', '--config', help='path to config file')
    parser.add_argument('-v', '--verbose', action='count', help='verbose logging (-vv to be more verbose)', default=0)
    parser.add_argument('base', help='base commit hash')
    parser.add_argument('commit', help='new commit hash')
    parser.add_argument('ref', help='commit ref')
    args = parser.parse_args()
    level = [logging.ERROR, logging.INFO, logging.DEBUG]
    if args.logfile == '-':
        logging.basicConfig(format=LOG_CONSOLE_FORMAT, level=level[args.verbose])
    else:
        logging.basicConfig(filename=args.logfile, level=level[args.verbose])
    config = Config(checkers={'WhiteSpaceChecker': '', 'CodeValidatorChecker': ''}).add_from_default_locations()
    config.add_from_args(args)
    if args.config:
        config.add_from_json(args.config)
    return config


tempdir = None
try:
    config = get_config()
    checkers = create_checkers(config)
    logging.debug('Using %s', ', '.join([c.get_name() for c in checkers]))

    errors = None
    if checkers:
        tempdir = tempfile.mkdtemp()
        changes = retrieve_changed_files(tempdir, GitRepo(), config.base, config.commit)
        logging.debug('%d changes: %s', len(changes), [str(c) for c in changes])
        errors = check(checkers)

    if errors:
        error_msg = '\n'
        for checker, checker_errors in errors.iteritems():
            error_msg += '%s %s\n' % (checker.get_name(), checker.get_documentation_url())
            for error in checker_errors:
                error_msg += '    %s\n' % error
        logging.error(error_msg)
        if args.dry_run:
            error_msg = 'dry run enabled, only logging\n'
        else:
            sys.exit(1)
except Exception, e:

    logging.exception('Unknown error in pre-receive hook')
    sys.exit(1)
finally:
    if tempdir:
        shutil.rmtree(tempdir)
