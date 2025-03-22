#!/usr/bin/env python3
import os
import sys

def rename_items(directory):
    """모든 파일 및 폴더 이름에서 점(.)을 언더스코어(_)로 변경합니다."""
    
    # 디렉토리 내의 모든 항목을 가져옵니다
    items = os.listdir(directory)
    
    # 항목을 깊이 우선으로 처리하기 위해 먼저 파일을 처리합니다
    for item in sorted(items, key=lambda x: (os.path.isdir(os.path.join(directory, x)), x)):
        old_path = os.path.join(directory, item)
        
        # 숨김 파일이나 특수 디렉토리는 건너뜁니다
        if item.startswith('.') or item == "__pycache__":
            continue
        
        # 이름에 점이 있는지 확인합니다
        if '.' in item:
            if os.path.isdir(old_path):
                # 디렉토리인 경우 모든 점을 언더스코어로 변경
                new_name = item.replace('.', '_')
                new_path = os.path.join(directory, new_name)
                print(f"Renaming directory: {old_path} -> {new_path}")
                os.rename(old_path, new_path)
                old_path = new_path
                item = new_name
            elif os.path.isfile(old_path):
                # 파일인 경우 확장자 부분을 제외하고 점을 언더스코어로 변경
                name_parts = item.rsplit('.', 1)  # 마지막 점을 기준으로 파일명과 확장자 분리
                if len(name_parts) > 1:
                    name, extension = name_parts
                    if '.' in name:  # 파일명 부분에 점이 있는 경우만 처리
                        new_name = name.replace('.', '_') + '.' + extension
                        new_path = os.path.join(directory, new_name)
                        print(f"Renaming file: {old_path} -> {new_path}")
                        os.rename(old_path, new_path)
                        old_path = new_path
                        item = new_name
        
        # 디렉토리인 경우 재귀적으로 처리합니다
        if os.path.isdir(old_path):
            rename_items(old_path)

if __name__ == "__main__":
    # 현재 디렉토리나 명령줄 인수로 지정된 디렉토리를 사용합니다
    directory = sys.argv[1] if len(sys.argv) > 1 else "."
    
    print(f"Starting to rename files and directories in {directory}")
    rename_items(directory)
    print("Renaming complete")