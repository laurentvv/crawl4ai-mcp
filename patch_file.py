import re

with open('tests/test_results.py', 'r') as f:
    content = f.read()

content = content.replace('\nfrom unittest.mock import patch\n', '')
content = 'from unittest.mock import patch\n' + content

with open('tests/test_results.py', 'w') as f:
    f.write(content)
