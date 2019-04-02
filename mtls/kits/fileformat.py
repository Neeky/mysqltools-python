"""
把以字节为单位的文件大小转换为对人类友好的方式
1024 B --> 1KiB
1024 * 1024 * 3 --> 3MiB
......
"""

def fileformat(size,base=1000):
    """把文件大小从字节转化成对人类友好的形式
    >>> print(fileformat(1024))
    1.0 KiB
    >>> print(fileformat(1024 * 1024))
    1.0 MiB
    >>> print(fileformat(0))
    0.0 B
    >>> print(fileformat(6))
    6.0 B
    """
    if base not in (1000,1024):
        # 为么以 1000 进位，要么以 1024 进位
        raise ValueError("the base argument must be 1000 or 1024 .")

    size = float(size)
    if base == 1024:
        suffix = ['KiB','MiB','GiB','TiB','PiB','EiB','ZiB','YiB']
    else:
        suffix = ['KB','MB','GB','TB','PB','EB','ZB','YB']
    
    if size < base:
        return f"{size} B"
    else:
        for i,suf in enumerate(suffix):
            unit = base ** (i + 2)
            if size < unit:
                return "{0:.1f} {1}".format(size * base /unit,suf)
        return "{0:.1f} {1}".format(size * base /unit,suf)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
