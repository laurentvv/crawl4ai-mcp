import time
import re

# Mock clean_ui_artifacts for benchmark
def clean_ui_artifacts(text):
    return text

def remove_links_original(markdown_text):
    code_blocks = []

    def save_code_block(match):
        code = match.group(0)
        code_blocks.append(code)
        return f"__CODE_BLOCK_{len(code_blocks)-1}__"

    markdown_with_placeholders = re.sub(r'```[\s\S]*?```', save_code_block, markdown_text)
    text_without_images = re.sub(r'!\[[^\]]*\]\([^)]+\)', '', markdown_with_placeholders)
    text_without_links = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text_without_images)
    text_cleaned = clean_ui_artifacts(text_without_links)
    text_without_empty_lines = re.sub(r'\n\s*\n', '\n\n', text_cleaned)
    text_without_extra_spaces = re.sub(r' {2,}', ' ', text_without_empty_lines)

    result = text_without_extra_spaces
    for i, code_block in enumerate(code_blocks):
        result = result.replace(f"__CODE_BLOCK_{i}__", code_block)

    return result

def remove_links_optimized_split(markdown_text):
    parts = re.split(r'(```[\s\S]*?```)', markdown_text)
    for i in range(0, len(parts), 2):
        if not parts[i]: continue
        part = re.sub(r'!\[[^\]]*\]\([^)]+\)', '', parts[i])
        part = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', part)
        part = clean_ui_artifacts(part)
        part = re.sub(r'\n\s*\n', '\n\n', part)
        parts[i] = re.sub(r' {2,}', ' ', part)
    return "".join(parts)

def remove_links_optimized_sub(markdown_text):
    code_blocks = []

    def save_code_block(match):
        code = match.group(0)
        code_blocks.append(code)
        return f"__CODE_BLOCK_{len(code_blocks)-1}__"

    markdown_with_placeholders = re.sub(r'```[\s\S]*?```', save_code_block, markdown_text)
    text_without_images = re.sub(r'!\[[^\]]*\]\([^)]+\)', '', markdown_with_placeholders)
    text_without_links = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text_without_images)
    text_cleaned = clean_ui_artifacts(text_without_links)
    text_without_empty_lines = re.sub(r'\n\s*\n', '\n\n', text_cleaned)
    text_without_extra_spaces = re.sub(r' {2,}', ' ', text_without_empty_lines)

    def restore_code_block(match):
        index = int(match.group(1))
        return code_blocks[index]

    return re.sub(r'__CODE_BLOCK_(\d+)__', restore_code_block, text_without_extra_spaces)

# Generate test data
text = ""
for i in range(2000):
    text += f"Some ![image](img{i}.jpg) and [link text {i}](http://example.com/{i}) here.  \n\n"
    text += f"```python\nprint('Hello world {i}')\nfor j in range(10):\n    pass\n```\n"

# Warmup
remove_links_original(text)
remove_links_optimized_split(text)
remove_links_optimized_sub(text)

# Benchmark
import timeit

n_runs = 10
orig_time = timeit.timeit(lambda: remove_links_original(text), number=n_runs)
split_time = timeit.timeit(lambda: remove_links_optimized_split(text), number=n_runs)
sub_time = timeit.timeit(lambda: remove_links_optimized_sub(text), number=n_runs)

print(f"Original: {orig_time:.4f}s")
print(f"Optimized (split): {split_time:.4f}s")
print(f"Optimized (sub): {sub_time:.4f}s")
