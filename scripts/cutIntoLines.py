import os

def split_file(filename):
    with open(filename, 'r', encoding='utf-8', errors='replace') as f:
        lines = f.readlines()
        num_files = len(lines) // 15 + 1
        for i in range(num_files):
            start = i * 15
            end = (i + 1) * 15
            file_lines = lines[start:end]
            if file_lines:
                new_filename = f'{i+1}.txt'
                with open(new_filename, 'w', encoding='utf-8', errors='replace') as new_file:
                    new_file.writelines(file_lines)

if __name__ == '__main__':
    filename = 'phpCut.txt'  # 替换为你要分割的文件名
    split_file(filename)