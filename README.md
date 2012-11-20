Zooker
======

Python library for use in git hooks.

Usage
-----

To try locally (with console output):

  ./src/pre-receive.py 53d47 f8c2f 12 -vv --logfile=-

Symlink pre-receive.py as .git/hooks/pre-receive in your Git repo.

TODO
----

* commit message validation
* Jira integration (parse commit message and use Jira API)
* notification emails (configurable)
