import os
import subprocess

def get_changes(git_stdout):
    """Receives the changed files from git in the following format:

    M       foo
    A       bar
    A       quux

    Information on the meaning of the letters are in the help of git diff - diff-filter argument.
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

def git(args, **kwargs):
    environ = os.environ.copy()
    if 'repo' in kwargs:
        environ['GIT_DIR'] = kwargs['repo']
    if 'work' in kwargs:
        environ['GIT_WORK_TREE'] = kwargs['work']
    proc = subprocess.Popen(args, stdout=subprocess.PIPE, env=environ)
    return proc.communicate()

def get_changed_files(base, commit, **kw):
    (results, code) = git(('git', 'diff', '--name-status'), **kw)
    return get_changes(results)