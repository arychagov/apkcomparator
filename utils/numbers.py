def human_readable_size(_bytes: int) -> str:
    _bytes = float(abs(_bytes))
    kilobytes = float(1024)
    megabytes = float(kilobytes ** 2)
    gigabytes = float(kilobytes ** 3)

    if _bytes < kilobytes:
        return '{0} B'.format(_bytes)
    elif kilobytes <= _bytes < megabytes:
        return '{0:.2f} KB'.format(_bytes / kilobytes)
    elif megabytes <= _bytes < gigabytes:
        return '{0:.2f} MB'.format(_bytes / megabytes)
    elif gigabytes <= _bytes:
        return '{0:.2f} GB'.format(_bytes / gigabytes)


def get_sign(value: int) -> str:
    return '' if value == 0 else ('-' if value < 0 else '+')
