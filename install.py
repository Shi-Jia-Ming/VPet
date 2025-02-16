# -*- coding: utf-8 -*-
import os
import shutil
import time
import fnmatch

# 文件屏蔽列表
exclude_list = ['*.bkp', '*.lps']

def find_recently_modified_file(directory):
    # 获取目录下所有文件的列表
    files = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    
    if not files:
        return None

    # 从 files 中排除 exclude_list 中的文件
    for exclude in exclude_list:
        files = [f for f in files if not fnmatch.fnmatch(f, exclude)]
    
    # 找到最近修改的文件
    recently_modified_file = max(files, key=os.path.getmtime)

    modified_time_end = os.path.getmtime(recently_modified_file)

    # 获取最后修改时间的两分钟内修改的文件
    modified_time_start = modified_time_end - 120

    recently_modified_file = [f for f in files if modified_time_start <= os.path.getmtime(f) <= modified_time_end]

    return recently_modified_file

def move_file(src, dst):
    # 移动文件
    shutil.copy(src, dst)
    print(f"Copied {src} to {dst}")

def main():
    # 设置源目录和目标目录
    source_directory = '.\\VPet-Simulator.Windows\\bin\\x64\\Release\\net8.0-windows'
    destination_directory = 'C:\\Users\\LengTouZai\\AppData\\Local\\VPet'
    
    # 找到最近修改的文件
    recently_modified_file = find_recently_modified_file(source_directory)
    
    if recently_modified_file:
        # 移动文件
        for file in recently_modified_file:
            move_file(file, destination_directory)
    else:
        print("No files found in the source directory.")

if __name__ == "__main__":
    main()