"""
Description: 常用方法 
Created_time: 2023-08-02
"""
import zlib
from datetime import datetime


def bytes_to_str(bytes_):
    """将二进制编码zlib解压后处理为字符串"""
    msg = zlib.decompress(bytes_)
    return str(msg, encoding="utf-8")


def __to_datetime(datetime_):
    if isinstance(datetime_, int):
        dt = datetime.fromtimestamp(datetime_)
    elif isinstance(datetime_, int):
        dt = datetime.fromisoformat(datetime_)
    elif isinstance(datetime_, datetime):
        dt = datetime_
    else:
        raise TypeError(f"type {type(datetime_)} is not expected.")
    return dt
    ...


def datetime_to_timestamp(datetime_):
    dt = __to_datetime(datetime_)
    return dt.timestamp()


def timestamp_to_datetime(datetime_):
    dt = __to_datetime(datetime_)
    return dt.isoformat(sep=" ", timespec="seconds")
