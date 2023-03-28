#!/usr/bin/env python
# coding=utf-8
"""
注 dt: 时间类型字符串  date: date or datetime 类型
"""

import time
import datetime
from datetime import timedelta

from dateutil.relativedelta import relativedelta


def get_today():
    """
    获取今天的年月日格式的日期 str
    :return:
    """
    date = datetime.date.today()
    return date.strftime("%Y-%m-%d")


def date_to_str(date, dft='%Y-%m-%d'):
    """
    将datetime.date 类型转为 str
    :param date:
    :param dft:
    :return:
    """
    return date.strftime(dft)


def datetime_to_str(date, dft='%Y-%m-%d %H:%M:%S'):
    """
    将datetime.将datetime 类型转为 str
    :param date:
    :param dft:
    :return:
    """
    return date.strftime(dft)


def str_date_to_datetime(dt: str, dft='%Y-%m-%d'):
    """
    date str 转 datetime str
    """
    return str_to_datetime(dt, dft)


def str_to_datetime(dt: str, dft="%Y-%m-%d %H:%M:%S"):
    """
    将str 类型 转为 datetime.datetime 类型
    :param dt:
    :param dft:
    :return: datetime.datetime
    """
    return datetime.datetime.strptime(dt, dft)


def str_to_date(dt: str, dft='%Y-%m-%d'):
    """
    日期字符串转 date类型
    :param dt:
    :param dft:
    :return:  datetime.date
    """
    _datetime = datetime.datetime.strptime(dt, dft)
    return datetime.date(_datetime.year, _datetime.month, _datetime.day)


def date_add(dt=None, days=1, dft='%Y-%m-%d', **kw):
    """
    将日期加几天
    :param dt:
    :param days:
    :param dft:
    :return:
    """
    # 先将日期转为 datetime.date 类型
    _date = str_to_date(dt=dt, dft=dft)
    return _date + relativedelta(days=days, **kw)


def datetime_add(dt=None, days=0, dft='%Y-%m-%d %H:%M:%S', **kw):
    """
    将日期加几天
    :param dt:
    :param days:
    :param dft:
    :param kw:
    :return:
    """
    # 先将日期转为 datetime.datetime 类型
    _datetime = str_to_datetime(dt=dt, dft=dft)
    return _datetime + relativedelta(days=days, **kw)


def date_sub(dt=None, days=1, dft='%Y-%m-%d', **kw):
    """
    将日期减几天  默认
    :param dt:
    :param days:
    :param dft:
    :param kw:
    :return:
    """
    # 先将日期转为 datetime.date 类型
    _date = str_to_date(dt=dt, dft=dft)
    return _date - relativedelta(days=days, **kw)


def datetime_sub(dt=None, days=0, dft='%Y-%m-%d %H:%M:%S', **kw):
    """
    将日期减几天
    :param dt:datetime str
    :param days:
    :param dft:
    :param kw:
    :return:
    """
    # 先将日期转为 datetime.datetime 类型
    _datetime = str_to_datetime(dt=dt, dft=dft)
    return _datetime - relativedelta(days=days, **kw)


def datetime_now(dft='%Y-%m-%d %H:%M:%S'):
    """
    获取当前时间的datetime时间
    :return:
    """
    return datetime_to_str(datetime.datetime.now(), dft)


def get_utc_time(stamp_time):
    """
    获取当前utc时间
    :param stamp_time: 时间戳
    :return: '%Y-%m-%d'
    """
    return datetime.datetime.utcfromtimestamp(float(stamp_time))


def dt_to_stamp(dt, dft="%Y-%m-%d %H:%M:%S"):
    """datetime str类型 转 时间戳"""
    return int(time.mktime(time.strptime(dt, dft)))


def dt_tf_loc(dt, dft="%Y-%m-%d %H:%M:%S", hours=0, minutes=0):
    """datetime str类型 转 当地时间"""
    utc_time = get_utc_time(dt_to_stamp(dt, dft))
    time_array = utc_time + timedelta(hours=hours, minutes=minutes)
    return time_array.strftime(dft)


def dt_tf_mx(dt, dft="%Y-%m-%d %H:%M:%S", hours=-6):
    """时间转换成墨西哥时间"""
    return dt_tf_loc(dt, dft=dft, hours=hours)


def dt_tf_id(dt, dft="%Y-%m-%d %H:%M:%S", hours=+7):
    """时间转换成印尼时间"""
    return dt_tf_loc(dt, dft=dft, hours=hours)


def dt_tf_pak(dt, dft="%Y-%m-%d %H:%M:%S", hours=+5):
    """时间转换成巴基斯坦时间"""
    return dt_tf_loc(dt, dft=dft, hours=hours)


def dt_tf_in(dt, dft="%Y-%m-%d %H:%M:%S", hours=+5, minutes=30):
    """时间转换成印度时间"""
    return dt_tf_loc(dt, dft=dft, hours=hours, minutes=minutes)


def dt_tf_phl(dt, dft="%Y-%m-%d %H:%M:%S", hours=+8):
    """时间转换成菲律宾时间"""
    return dt_tf_loc(dt, dft=dft, hours=hours)


def datetime_transform(dt=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), sub_days=0, country='mx'):
    """北京时间 转 当地时间"""
    dt = datetime_to_str(datetime_sub(dt=dt, days=sub_days))
    if country == 'mx':
        return dt_tf_mx(dt)
    elif country == 'id':
        return dt_tf_id(dt)
    elif country == 'pak':
        return dt_tf_pak(dt)
    elif country == 'phl':
        return dt_tf_phl(dt)
    return dt_tf_in(dt)
