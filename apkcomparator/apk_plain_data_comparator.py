from apkcomparator.data import ApkPlainData
from utils.numbers import get_sign, human_readable_size


def compare_plain_data(prev: ApkPlainData, curr: ApkPlainData) -> str:
    diff_download_size = curr.download_size - prev.download_size
    diff_file_size = curr.file_size - prev.file_size
    diff_methods_count = curr.methods_count - prev.methods_count
    lines = [
        'Download size: {size} (diff: {sign}{diff})'.format(
            size=human_readable_size(curr.download_size),
            sign=get_sign(diff_download_size),
            diff=human_readable_size(diff_download_size)
        ),
        'File size: {size} (diff: {sign}{diff})'.format(
            size=human_readable_size(curr.file_size),
            sign=get_sign(diff_file_size),
            diff=human_readable_size(diff_file_size)
        ),
        'Methods count: {size} (diff: {sign}{diff})'.format(
            size=curr.methods_count,
            sign=get_sign(diff_methods_count),
            diff=abs(diff_methods_count)
        )]
    return '\n'.join(lines)
