#!/usr/bin/env python3
"""
paper-lens 环境检查工具
验证所有必需依赖是否正确安装
"""

import sys
import importlib

REQUIRED_LIBS = [
    ("pymupdf", "fitz", "PDF parsing, highlighting, and annotations"),
]

def check_python_version():
    """检查 Python 版本"""
    required = (3, 8)
    current = sys.version_info[:2]
    if current >= required:
        print(f"[OK] Python {sys.version.split()[0]}")
        return True
    else:
        print(f"[ERROR] Python {sys.version.split()[0]} < 3.8 required")
        return False

def check_lib(lib_name, import_name, description):
    """检查单个库是否安装"""
    try:
        lib = importlib.import_module(import_name)
        version = getattr(lib, "__version__", getattr(lib, "version", "installed"))
        if callable(version):
            version = "installed"
        print(f"[OK] {lib_name} ({version}) - {description}")
        return True
    except ImportError:
        print(f"[MISSING] {lib_name} - {description}")
        return False

def check_optional_libs():
    """检查可选库"""
    optional = [
        ("camelot-py", "camelot", "Table extraction (optional)"),
    ]
    print("\n--- Optional Dependencies ---")
    for lib_name, import_name, description in optional:
        try:
            importlib.import_module(import_name)
            print(f"[OK] {lib_name} - {description}")
        except ImportError:
            print(f"[SKIP] {lib_name} - {description}")

def main():
    print("=" * 50)
    print("paper-lens Environment Check")
    print("=" * 50)
    print("\n--- Required Dependencies ---")
    
    results = [check_python_version()]
    for lib_name, import_name, description in REQUIRED_LIBS:
        results.append(check_lib(lib_name, import_name, description))
    
    check_optional_libs()
    
    print("\n" + "=" * 50)
    if all(results):
        print("All required dependencies are satisfied.")
        print("\nTo get started:")
        print("  python scripts/extract_content.py <pdf_path> --purpose deep_dive")
        sys.exit(0)
    else:
        print("Missing dependencies detected!")
        print("\nInstall with:")
        print("  pip install pymupdf")
        sys.exit(1)

if __name__ == "__main__":
    main()
