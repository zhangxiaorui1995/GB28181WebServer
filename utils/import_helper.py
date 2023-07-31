import sys


class ImportHelper:
    @staticmethod
    def load_class(s: str):
        """
        :param s: xxx.xxx  example: datetime.datetime
        """
        path, klass = s.rsplit(".", 1)
        __import__(path)
        mod = sys.modules[path]
        return getattr(mod, klass)
