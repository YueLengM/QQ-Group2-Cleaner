#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os
from datetime import datetime
from tkinter import Tk, filedialog

bucket_size = {}
bucket_date = {}


def add_file(path, name):
    file_date = datetime.fromtimestamp(os.path.getctime(path)).date()
    file_size = round(os.path.getsize(path) / 1024, 2)

    if file_date.year not in bucket_size:
        bucket_size[file_date.year] = {}

    if file_date.month not in bucket_size[file_date.year]:
        bucket_size[file_date.year][file_date.month] = 0

    bucket_size[file_date.year][file_date.month] += file_size

    if file_date.year not in bucket_date:
        bucket_date[file_date.year] = {}

    if file_date.month not in bucket_date[file_date.year]:
        bucket_date[file_date.year][file_date.month] = []

    bucket_date[file_date.year][file_date.month].append(name)


def scan():
    for root, _, files in os.walk(ROOT_PATH):
        for name in files:
            path = os.path.join(root, name)
            print(path, end=' ' * 4 + '\r')
            add_file(path, name)


def output():
    years = sorted(bucket_size.keys())
    for year in years:
        print(year)
        months = sorted(bucket_size[year].keys())
        for month in months:
            size = bucket_size[year][month] / 1024
            if size < 1024:
                print('    {}\t{}MB'.format(month, round(size, 2)))
            else:
                print('    {}\t{}GB'.format(month, round(size / 1024, 2)))


def del_target(year, month):
    prefix = '删除 {} {}'.format(year, month)
    print(prefix, end='\r')
    for file in bucket_date[year][month]:
        try:
            path = os.path.join(ROOT_PATH, file[0:2], file[2:4], file)
            print(prefix + ': ' + file, end='\r')
            os.remove(path)
        except:
            continue
    del bucket_size[year][month]
    del bucket_date[year][month]
    print(prefix + '    完成' + ' ' * 30)


def del_before(tar_year, tar_month):
    years = sorted(bucket_date.keys())
    for year in years:
        if year > tar_year:
            break
        else:
            months = sorted(bucket_size[year].keys())
            if year < tar_year:
                for month in months:
                    del_target(year, month)
            else:
                for month in months:
                    if month > tar_month:
                        break
                    else:
                        del_target(year, month)


def del_ipt():
    ipt = input('删除 XXXX 年 XX 月及更旧的文件：').split()
    if not ipt:
        return
    try:
        year = int(ipt[0])
        month = int(ipt[1])
        del_before(year, month)
    finally:
        pass


Tk().withdraw()
ROOT_PATH = filedialog.askdirectory(title="请选择要清理的 Group2 文件夹")
if ROOT_PATH:
    os.system('mode con: cols={} lines=20'.format(len(ROOT_PATH) + 50))
    scan()
    print()
    while True:
        output()
        del_ipt()
