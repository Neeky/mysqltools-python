"""
实现若干通用的核心函数
"""
import os
import sys
import time
import mysql
import random
import string
import logging
import argparse

def check_python_version() -> None:
    """
    检测当前的 python 版本是否被支持，只支持 python-3.0.x 以上的环境
    """
    if sys.version_info.major <= 2:
        print("only support python-3.x",file=sys.stderr)
        sys.exit(1)




