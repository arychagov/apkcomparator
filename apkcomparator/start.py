import argparse
import os.path

from apkcomparator.apk_comparator import generate_report
from apkcomparator.data import Apk
from utils.environment import check_environment_variable_set
from utils.logger import log


def get_report_file(args):
    if args.out:
        return args.out
    directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'result')
    if not os.path.exists(directory):
        os.makedirs(directory)
    return os.path.join(directory, 'report.txt')


def verify_environment():
    check_environment_variable_set('ANDROID_HOME')
    check_environment_variable_set('JAVA_HOME')


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--prev-apk-path', type=str, required=True,
                        dest='prevapkpath', default=None,
                        help='Previous apk file path to compare with')
    parser.add_argument('--apk-path', type=str, required=True,
                        dest='currapkpath', default=None,
                        help='Current apk file path to compare with')
    parser.add_argument('--output', type=str, required=False,
                        dest='out', default=None,
                        help='Optional output file. By default reports are stored in result directory.')
    return parser.parse_args()


def save_report_to_file(report: str, file: str):
    log().info('Saving report to {}'.format(file))
    with open(file, 'w') as file:
        file.write(report)


def fetch_apks(args):
    return Apk(args.prevapkpath), Apk(args.currapkpath)


def main():
    args = parse_args()
    verify_environment()
    prev_apk, curr_apk = fetch_apks(args)
    if not prev_apk or not curr_apk:
        raise RuntimeError('Cannot get apk(s), check error logs.')
    report = generate_report(prev_apk, curr_apk)
    save_report_to_file(report.report, get_report_file(args))


if __name__ == '__main__':
    main()
