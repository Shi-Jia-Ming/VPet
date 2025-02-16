# -*- coding: utf-8 -*-
import os
import shutil
import time
import fnmatch

# �ļ������б�
exclude_list = ['*.bkp', '*.lps']

def find_recently_modified_file(directory):
    # ��ȡĿ¼�������ļ����б�
    files = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    
    if not files:
        return None

    # �� files ���ų� exclude_list �е��ļ�
    for exclude in exclude_list:
        files = [f for f in files if not fnmatch.fnmatch(f, exclude)]
    
    # �ҵ�����޸ĵ��ļ�
    recently_modified_file = max(files, key=os.path.getmtime)

    modified_time_end = os.path.getmtime(recently_modified_file)

    # ��ȡ����޸�ʱ������������޸ĵ��ļ�
    modified_time_start = modified_time_end - 120

    recently_modified_file = [f for f in files if modified_time_start <= os.path.getmtime(f) <= modified_time_end]

    return recently_modified_file

def move_file(src, dst):
    # �ƶ��ļ�
    shutil.copy(src, dst)
    print(f"Copied {src} to {dst}")

def main():
    # ����ԴĿ¼��Ŀ��Ŀ¼
    source_directory = '.\\VPet-Simulator.Windows\\bin\\x64\\Release\\net8.0-windows'
    destination_directory = 'C:\\Users\\LengTouZai\\AppData\\Local\\VPet'
    
    # �ҵ�����޸ĵ��ļ�
    recently_modified_file = find_recently_modified_file(source_directory)
    
    if recently_modified_file:
        # �ƶ��ļ�
        for file in recently_modified_file:
            move_file(file, destination_directory)
    else:
        print("No files found in the source directory.")

if __name__ == "__main__":
    main()