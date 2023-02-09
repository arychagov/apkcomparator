import os.path
import subprocess
from typing import Optional

from apkcomparator.android_manifest_comparator import compare_manifests
from apkcomparator.apk_compare_result_processor import (
    process_apk_compare_result)
from apkcomparator.apk_plain_data_comparator import compare_plain_data
from apkcomparator.data import Apk, ApkCompareReport, ApkPlainData
from utils.environment import android_tools_bin_dir
from utils.logger import log


def call_with_output(command: list[str]):
    output = None
    error = None
    try:
        rc = subprocess.run(command, capture_output=True)
        if rc.returncode == 0:
            output = rc.stdout.decode()
        else:
            error = rc.stderr.decode()
    except subprocess.CalledProcessError as e:
        error = e.output.decode()
    except Exception as e:
        # check_call can raise other exceptions, such as FileNotFoundError
        error = str(e)
    return output, error


def execute_apkanalyzer(subject: str, verb: str, *args):
    log().info('Executing command: apkanalyzer {subject} {verb} {args}'.format(
        subject=subject, verb=verb, args=' '.join(args)
    ))
    apkanalyzer = os.path.join(android_tools_bin_dir(), 'apkanalyzer')
    command = [apkanalyzer, subject, verb]
    command.extend(args)
    return call_with_output(command)


def get_download_size(apk: Apk) -> int:
    output, error = execute_apkanalyzer('apk', 'download-size', apk.apk_path)
    if error:
        log().error('Failed to get download size, error: {}'.format(output))
        return -1
    return int(output)


def get_file_size(apk: Apk) -> int:
    output, error = execute_apkanalyzer('apk', 'file-size', apk.apk_path)
    if error:
        log().error('Failed to get file size, error: {}'.format(output))
        return -1
    return int(output)


def get_methods_count(apk: Apk) -> int:
    output, error = execute_apkanalyzer('dex', 'references', apk.apk_path)
    if error:
        log().error('Failed to get methods count, error: {}'.format(error))
        return -1
    return sum([int(line.split('\t')[1]) for line in output.splitlines()])


def get_manifest(apk: Apk) -> Optional[str]:
    output, error = execute_apkanalyzer('manifest', 'print', apk.apk_path)
    if error:
        log().error('Failed to get manifest, error: {}'.format(error))
        return None
    return output


def get_compare_result(prev: Apk, curr: Apk) -> Optional[str]:
    output, error = execute_apkanalyzer(
        'apk', 'compare', '--different-only', '--files-only', prev.apk_path,
        curr.apk_path)
    if error:
        log().error('Failed to compare result, error: {}'.format(error))
        return None
    return output


def get_version_name(apk: Apk) -> Optional[str]:
    output, error = execute_apkanalyzer('apk', 'summary', apk.apk_path)
    if error:
        log().error('Failed to get app summary, error: {}'.format(error))
        return None
    return output.split('\t')[2]


def assemble_report(plain_data_report: str, compare_report: str, manifest_report: str):
    return '\n'.join([plain_data_report, compare_report, manifest_report])


def generate_report(prev_apk: Apk, curr_apk: Apk) -> ApkCompareReport:
    prev_apk_plain_data = ApkPlainData(
        download_size=get_download_size(prev_apk),
        file_size=get_file_size(prev_apk),
        methods_count=get_methods_count(prev_apk)
    )
    curr_apk_plain_data = ApkPlainData(
        download_size=get_download_size(curr_apk),
        file_size=get_file_size(curr_apk),
        methods_count=get_methods_count(curr_apk)
    )
    plain_data_report = compare_plain_data(prev_apk_plain_data, curr_apk_plain_data)
    apk_compare_result = get_compare_result(prev_apk, curr_apk)
    compare_report = process_apk_compare_result(apk_compare_result)
    prev_apk_manifest, curr_apk_manifest = get_manifest(prev_apk), get_manifest(curr_apk)
    manifest_compare_report = compare_manifests(prev_apk_manifest, curr_apk_manifest)
    report = assemble_report(plain_data_report, compare_report, manifest_compare_report)
    return ApkCompareReport(report)
