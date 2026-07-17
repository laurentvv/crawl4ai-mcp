import unittest
import sys
import os

if __name__ == '__main__':
    # Ensure src is in path
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

    # Discover and run tests
    loader = unittest.TestLoader()
    suite = loader.discover("tests", pattern="test_*.py")

    runner = unittest.TextTestRunner()
    result = runner.run(suite)

    sys.exit(0 if result.wasSuccessful() else 1)
