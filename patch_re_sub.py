import re

with open("src/crawl4ai_mcp/__init__.py", "r") as f:
    content = f.read()

# Replace the loop with re.sub
old_loop = """    # Put the code blocks back in place
    result = text_without_extra_spaces
    for i, code_block in enumerate(code_blocks):
        result = result.replace(f"__CODE_BLOCK_{i}__", code_block)"""

new_loop = """    # Put the code blocks back in place
    def restore_code_block(match):
        index = int(match.group(1))
        return code_blocks[index]

    result = re.sub(r'__CODE_BLOCK_(\d+)__', restore_code_block, text_without_extra_spaces)"""

new_content = content.replace(old_loop, new_loop)

with open("src/crawl4ai_mcp/__init__.py", "w") as f:
    f.write(new_content)
