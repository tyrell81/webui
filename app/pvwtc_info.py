#!env/bin/python
# coding=utf-8
import os
import subprocess
from flask import Flask, url_for, redirect, render_template, request, Response
from datetime import datetime
import sys
reload(sys)
sys.setdefaultencoding('utf8')


def pvwtc_info_date():
    return datetime.now().strftime("%A %d.%m.%Y %H:%M")

def pvwtc_info_df():
    cmd = "df -h"
    df_str = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.read()
    print "out:"
    print df_str
    print "//"
    return df_str