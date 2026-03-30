import os
import sys

def is_safe_path(path, base_dir):
    """
    Checks if the path is safe (i.e., it is within the base_dir).
    """
    abs_base = os.path.abspath(base_dir)
    abs_path = os.path.abspath(path)
    return abs_path.startswith(abs_base + os.sep) or abs_path == abs_base

def test_is_safe_path():
    cwd = os.getcwd()
    base_dir = os.path.join(cwd, "crawl_results")

    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    print(f"Base directory: {base_dir}")

    safe_paths = [
        os.path.join(base_dir, "test.md"),
        os.path.join(base_dir, "subdir", "test.md"),
        "crawl_results/relative_test.md",
    ]

    unsafe_paths = [
        "/etc/passwd",
        "../../etc/passwd",
        os.path.join(cwd, "secret.txt"),
        "../vulnerable.txt",
        "some_other_dir/test.md",
        cwd
    ]

    all_passed = True

    print("\n--- Testing Safe Paths ---")
    for path in safe_paths:
        safe = is_safe_path(path, base_dir)
        print(f"Path: {path:40} -> {'SAFE' if safe else 'UNSAFE'}")
        if not safe:
            print(f"FAILED: {path} should be safe")
            all_passed = False

    print("\n--- Testing Unsafe Paths ---")
    for path in unsafe_paths:
        safe = is_safe_path(path, base_dir)
        print(f"Path: {path:40} -> {'SAFE' if safe else 'UNSAFE'}")
        if safe:
            print(f"FAILED: {path} should be unsafe")
            all_passed = False

    if all_passed:
        print("\nAll path validation tests PASSED!")
    else:
        print("\nSome path validation tests FAILED!")
        sys.exit(1)

if __name__ == "__main__":
    test_is_safe_path()
