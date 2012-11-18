#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import os
import subprocess


class GitRepo:

    """
    This class is used to abstract away the git repository. Making it possible to mock it in the unit tests.
    """

    def __init__(self, **kwargs):
        environ = os.environ.copy()
        if not environ.get('GIT_DIR'):
            if 'repo' in kwargs:
                repo = kwargs['repo']
            else:
                repo = '.git'
            environ['GIT_DIR'] = os.path.abspath(repo)

        if 'work' in kwargs:
            environ['GIT_WORK_TREE'] = kwargs['work']

        self.__environ = environ

    def parse_changes(self, git_stdout):
        """Receives the changed files from git in the following format:

        M       foo
        A       bar
        A       quux

        Information on the meaning of the letters is:
          * A - Added
          * C - Copied
          * D - Deleted
          * M - Modified
          * R - Renamed
          * T - have their type (i.e. regular file, symlink, submodule, ...) changed
          * U - are Unmerged
          * X - are Unknown
          * B - have had their pairing Broken

        More info in the help of git diff - diff-filter argument.
        The result is parsed and returned as a map(letter -> file path).
        """

        result = {}
        if not git_stdout:
            return result

        lines = git_stdout.split('\n')[:-1]
        for line in lines:
            if line:
                [k, v] = line.strip().split()
                if k not in result:
                    result[k] = []
                result[k].append(v)
        return result

    def __git(self, args):
        logging.debug(args)
        try:
            results = subprocess.check_output(args.split(), stderr=subprocess.STDOUT, env=self.__environ)
        except subprocess.CalledProcessError, e:
            logging.exception('Output was: %s', e.output)
            raise
        return results

    def get_changed_files(self, base, commit, **kw):
        results = self.__git('git diff --name-status %s..%s' % (base, commit))
        return self.parse_changes(results)

    def get_file_contents(self, commit, filename):
        results = self.__git('git show %s:%s' % (commit, filename))
        return results


class Change:

    def __init__(self, repo_path, change_type, temp_path=None):
        self.filename = os.path.basename(repo_path)
        self.repo_path = repo_path
        self.change_type = change_type
        self.temp_path = temp_path
        self.extension = os.path.splitext(self.filename)

    def __str__(self):
        return '%s %s' % (self.change_type, self.repo_path)


def copy_file_to(basedir, repo, commit, filename):
    contents = repo.get_file_contents(commit, filename)
    dirname = os.path.join(basedir, os.path.dirname(filename))
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    name = os.path.join(dirname, os.path.basename(filename))
    with open(name, 'w') as f:
        f.write(contents)
    return name


def copy_files_to(basedir, repo, commit, filenames):
    """
    This function copies all the files from the given commit to a specified base directory.
    It will create the folder hierarchy of the files as well.
    """

    return map(lambda f: copy_file_to(basedir, repo, commit, f), filenames)


def retrieve_changed_files(basedir, repo, base, commit):
    """
    This function retrieves all the changes files in a repository, and copies them to a give
    base directory (where it makes sense). It returns a list Change objects.
    """

    result = []
    changes = repo.get_changed_files(base, commit)

    if not changes:
        return result

    with_temp_path = [
        'A',
        'C',
        'M',
        'R',
        'T',
    ]
    without_temp_path = [
        'D',
        'T',
        'U',
        'X',
        'B',
    ]

    for change_type in with_temp_path:
        if change_type in changes:
            for repo_path in changes[change_type]:
                temp_path = copy_file_to(basedir, repo, commit, repo_path)
                result.append(Change(repo_path, change_type, temp_path))

    for change_type in without_temp_path:
        if change_type in changes:
            for repo_path in changes[change_type]:
                result.append(Change(repo_path, change_type))

    return result


