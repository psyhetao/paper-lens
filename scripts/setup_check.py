import sys
import importlib

def check_python_version():
    required = (3, 8)
    current = sys.version_info[:2]
    if current >= required:
        print(f"OK: Python {sys.version[0:5]}")
        return True
    else:
        print(f"ERROR: Python {sys.version[0:5]} < 3.8")
        return False

def check_lib(lib_name, import_name=None):
    import_name = import_name or lib_name
    try:
        lib = importlib.import_module(import_name)
        version = getattr(lib, "__version__", getattr(lib, "version", "unknown"))
        print(f"OK: {lib_name} {version}")
        return True
    except ImportError:
        print(f"ERROR: {lib_name} missing")
        return False

def main():
    print("--- paper-lens Environment Check ---")
    results = [
        check_python_version(),
        check_lib("pymupdf", "fitz"),
        check_lib("pdfplumber")
    ]
    if all(results):
        print("\nAll dependencies satisfied.")
        sys.exit(0)
    else:
        print("\nMissing dependencies. Run: pip install -r REQUIREMENTS.txt")
        sys.exit(1)

if __name__ == "__main__":
    main()
