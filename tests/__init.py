#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

# 本文件的目的，在于pyest测试时导入，可以定位到工程文件代码，直接 import
# 后面的注释部分，请严格按照真实的项目名、路径进行替换

TESTS_FOLDER_DIR = os.path.dirname(os.path.abspath(__file__))
FATHER_DIR = os.path.dirname(TESTS_FOLDER_DIR)

PROJECT_DIR = os.path.join(FATHER_DIR, "/src")

# 将项目工程加入到import 检索路径中
sys.path.insert(0, PROJECT_DIR)

print(f"tests folder dir is {TESTS_FOLDER_DIR}")
print(f"father folder dir is {FATHER_DIR}")
print(f"prject folder dir is {PROJECT_DIR}")