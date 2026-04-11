import timeit
import re

# Mock required functions
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

from crawl4ai_mcp import remove_links_from_markdown as remove_links_optimized

def test_performance_improvement():
    # Generate test data
    text = ""
    for i in range(1000):
        text += f"Some ![image](img{i}.jpg) and [link text {i}](http://example.com/{i}) here.  \n\n"
        text += f"```python\nprint('Hello world {i}')\nfor j in range(10):\n    pass\n```\n"

    # Warmup and correctness check
    orig_result = remove_links_original(text)
    opt_result = remove_links_optimized(text)

    assert orig_result == opt_result, "Optimized version does not match original behavior"

    n_runs = 5
    orig_time = timeit.timeit(lambda: remove_links_original(text), number=n_runs)
    opt_time = timeit.timeit(lambda: remove_links_optimized(text), number=n_runs)

    print(f"\nBaseline execution time: {orig_time:.4f}s")
    print(f"Optimized execution time: {opt_time:.4f}s")

    improvement = (orig_time - opt_time) / orig_time * 100
    print(f"Improvement: {improvement:.2f}%")

    # Assert improvement is meaningful (e.g. at least 30%)
    assert opt_time < orig_time * 0.7, "Optimization did not improve performance significantly"
