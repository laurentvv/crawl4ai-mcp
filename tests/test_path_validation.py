import os
import sys
from unittest.mock import MagicMock

# Mock out heavy dependencies that might not be available or fail to load
sys.modules["anyio"] = MagicMock()
sys.modules["click"] = MagicMock()
sys.modules["mcp"] = MagicMock()
sys.modules["mcp.types"] = MagicMock()
sys.modules["mcp.server"] = MagicMock()
sys.modules["mcp.server.lowlevel"] = MagicMock()
sys.modules["crawl4ai"] = MagicMock()
sys.modules["crawl4ai.content_scraping_strategy"] = MagicMock()
sys.modules["crawl4ai.deep_crawling"] = MagicMock()

# Now we can import from our module safely
sys.path.append(os.path.join(os.getcwd(), "src"))
from crawl4ai_mcp import is_safe_path

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

    # Test symlink attack (if possible in this env)
    evil_link = os.path.join(base_dir, "evil")
    if not os.path.exists(evil_link):
        try:
            os.symlink("/", evil_link)
            attack_path = os.path.join(evil_link, "etc/shadow")
            safe = is_safe_path(attack_path, base_dir)
            print(f"Symlink attack Path: {attack_path:40} -> {'SAFE' if safe else 'UNSAFE'}")
            if safe:
                print(f"FAILED: Symlink attack path {attack_path} should be unsafe")
                all_passed = False
        except (OSError, NotImplementedError):
            print("Skipping symlink test (not supported in this environment)")

    if all_passed:
        print("\nAll path validation tests PASSED!")
    else:
        print("\nSome path validation tests FAILED!")
        sys.exit(1)

if __name__ == "__main__":
    test_is_safe_path()
