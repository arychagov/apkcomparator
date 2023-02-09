import collections
from typing import Optional

from utils.numbers import human_readable_size, get_sign

ReportLine = collections.namedtuple(
    'ReportLine', ('lhs_size', 'rhs_size', 'diff', 'path'))


def format_line(line: ReportLine, indent_tabs: int = 1):
    return (
        '{indent}{path}\n'
        '{indent_inner}Was: {lhs_size}\n'
        '{indent_inner}Now: {rhs_size}\n'
        '{indent_inner}Diff: {sign}{diff}'
    ).format(
        path=line.path,
        lhs_size=human_readable_size(line.lhs_size),
        rhs_size=human_readable_size(line.rhs_size),
        sign=get_sign(line.diff),
        diff=human_readable_size(line.diff),
        indent="\t" * indent_tabs,
        indent_inner="\t" * (indent_tabs + 1)
    )


def get_report_line(line: str) -> ReportLine:
    terms = line.split('\t')
    return ReportLine(lhs_size=int(terms[0]), rhs_size=int(terms[1]),
                      diff=int(terms[2]), path=terms[3][1:])


def get_report_lines(report: Optional[str]) -> list[ReportLine]:
    if not report:
        return []
    return [get_report_line(line) for line in report.splitlines()]


def add_report(report_header: str, lines: list[str], report_lines: list[ReportLine]):
    accumulated_diff = 0
    for report_line in report_lines:
        accumulated_diff += report_line.diff
    lines.append('{}:'.format(report_header))
    lines.append('\tTotal diff: {sign}{diff}'.format(
        sign=get_sign(accumulated_diff),
        diff=human_readable_size(accumulated_diff)
    ))
    for line in report_lines:
        lines.append(format_line(line))


def process_apk_compare_result(report: Optional[str]) -> str:
    lines = ['Diff less that 1KB omitted from report!']
    report_lines = get_report_lines(report)
    report_lines = filter(lambda line: abs(line.diff) > 1024, report_lines)
    report_lines = sorted(report_lines, key=lambda line: line.diff, reverse=True)
    resource_lines = [line for line in report_lines if line.path.startswith('res/')]
    dex_lines = [line for line in report_lines if line.path.endswith('.dex')]
    asset_lines = [line for line in report_lines if line.path.startswith('assets/')]
    lib_lines = [line for line in report_lines if line.path.startswith('lib/')]
    other_lines = [line for line in report_lines if
                   line not in resource_lines and
                   line not in dex_lines and
                   line not in asset_lines and
                   line not in lib_lines]
    add_report('Dex files', lines, dex_lines)
    add_report('Libraries', lines, lib_lines)
    add_report('Assets', lines, asset_lines)
    add_report('Resources', lines, resource_lines)
    add_report('Other', lines, other_lines)
    return '\n'.join(lines)
