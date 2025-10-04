# -*- coding: utf-8 -*-
"""
convert_to_utf8.py
一键把整个项目的 .py 文件从 UTF-16 / GBK / ANSI 转成 UTF-8。
"""

import os

def convert_to_utf8(root_path):
    converted = 0
    skipped = 0

    for dirpath, _, files in os.walk(root_path):
        for filename in files:
            if filename.endswith(".py"):
                file_path = os.path.join(dirpath, filename)
                try:
                    # 尝试读取
                    with open(file_path, "r", encoding="utf-8") as f:
                        f.read()
                    print(f"✅ 已是 UTF-8：{file_path}")
                    skipped += 1
                except UnicodeDecodeError:
                    # 不是 UTF-8，尝试用 UTF-16/GBK/latin1 打开
                    for enc in ["utf-16", "utf-16-le", "utf-16-be", "gbk", "latin1"]:
                        try:
                            with open(file_path, "r", encoding=enc) as f:
                                content = f.read()
                            with open(file_path, "w", encoding="utf-8") as f:
                                f.write(content)
                            print(f"🌈 已转换为 UTF-8: {file_path} （原编码 {enc}）")
                            converted += 1
                            break
                        except UnicodeDecodeError:
                            continue
    print("\n=== 转换完成 ===")
    print(f"成功转换: {converted} 个文件")
    print(f"原本就是UTF-8: {skipped} 个文件")


if __name__ == "__main__":
    project_root = os.path.dirname(os.path.abspath(__file__))
    convert_to_utf8(project_root)
