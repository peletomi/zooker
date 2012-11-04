
import os
import mimetypes
import re

def is_text(path):
    known_extensions = ['sql', 'sql_diff', 'properties', 'tex', 'md']
    known_files = ['.gitignore', 'README']

    (mimetype, encoding) = mimetypes.guess_type(path, False)
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
        class_str = str(self.__class__)
        return class_str[class_str.rfind('.') + 1:]

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
            result = self.do_check(change)
            if result:
                return result

        return []

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
                i += 1
                if self.empty_line.match(line):
                    result.append("[%s:%s] empty line with whitespace" % (change.filename, i))
                if  line.find('\t') > -1:
                    result.append("[%s:%s] tabs" % (change.filename, i))
                if line.endswith(' ') or line.endswith('\t'):
                    result.append("[%s:%s] trailing whitespace" % (change.filename, i))
        return result

__checkers = {
    'WhiteSpaceChecker': WhiteSpaceChecker
}
def create_checkers(config):
    checkers = []
    if 'checkers' in config:
        for checker_name, checker_config in config['checkers'].iteritems():
            if checker_name in __checkers:
                ch = __checkers[checker_name]()
                ch.set_config(checker_config)
                if ch:
                    checkers.append(ch)
    return checkers
