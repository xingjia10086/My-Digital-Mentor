import zipfile
import os

def check_epub(file_path):
    print(f"--- 正在检查文件: {file_path} ---")
    
    if not os.path.exists(file_path):
        print(f"错误: 文件不存在。")
        return

    # 1. 检查基础元数据
    file_size = os.path.getsize(file_path)
    print(f"文件大小: {file_size / (1024*1024):.2f} MB")

    try:
        with zipfile.ZipFile(file_path, 'r') as z:
            # 2. 检查 ZIP 完整性
            bad_file = z.testzip()
            if bad_file:
                print(f"警告: ZIP 结构损坏，首个错误文件: {bad_file}")
            else:
                print("ZIP 结构完整性: 正常")

            # 3. 列出关键文件
            file_list = z.namelist()
            print(f"总文件数: {len(file_list)}")

            # 4. 检查标准 EPUB 标记
            has_mimetype = "mimetype" in file_list
            has_container = "META-INF/container.xml" in file_list
            
            print(f"标准 mimetype 存在: {has_mimetype}")
            print(f"标准 container.xml 存在: {has_container}")

            # 5. 检查加密/DRM 标记
            # Adobe DRM 通常在 META-INF/encryption.xml 或 META-INF/rights.xml
            drm_markers = [f for f in file_list if "encryption.xml" in f or "rights.xml" in f]
            if drm_markers:
                print(f"检测到潜在 DRM/加密标记: {drm_markers}")
                print("结论: 该文件可能受版权保护(DRM)加密，VS Code 插件可能无法直接读取。")
            else:
                print("未检测到常见 DRM 加密标记。")

            # 6. 检查 mimetype 内容（第一个文件应该是 mimetype 且不压缩）
            try:
                with z.open("mimetype") as m:
                    content = m.read().decode('utf-8').strip()
                    print(f"Mimetype 内容: {content}")
                    if content != "application/epub+zip":
                        print("警告: Mimetype 内容不符合 EPUB 标准。")
            except Exception:
                pass

    except zipfile.BadZipFile:
        print("错误: 该文件不是一个有效的 ZIP 压缩包（EPUB 本质上是 ZIP）。")
        print("可能原因: 下载不完整，或者是加密后的专有格式（如部分财新专有阅读器格式）。")
    except Exception as e:
        print(f"检查过程中发生异常: {e}")

if __name__ == "__main__":
    target = r"c:\Users\xingj\Downloads\财新周刊-第17期2025.epub"
    check_epub(target)
