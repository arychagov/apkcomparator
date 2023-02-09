import collections

from utils.stringify import stringify


@stringify
class Apk(object):
    def __init__(self, apk_path: str):
        self.apk_path = apk_path


class ApkCompareReport(object):
    def __init__(self, report: str):
        self.report = report


ApkPlainData = collections.namedtuple(
    'ApkPlainData', ('download_size', 'file_size', 'methods_count'))
