with open("src/crawl4ai_mcp/__init__.py", "r") as f:
    content = f.read()

# I apparently overwrote my previous fix for `_extract_page_content_and_errors` during the last rewrite
# Let's fix the NoneType title error again.

old_line = 'title = result.metadata.get("title", "Untitled page") if hasattr(result, "metadata") else "Untitled page"'
new_line = 'title = result.metadata.get("title", "Untitled page") if hasattr(result, "metadata") and result.metadata and result.metadata.get("title") is not None else "Untitled page"'
content = content.replace(old_line, new_line)

old_line2 = 'if any(indicator in title for indicator in error_indicators):'
new_line2 = 'if title and any(indicator in str(title) for indicator in error_indicators):'
content = content.replace(old_line2, new_line2)

old_line3 = 'error_type = "404" if "404" in title or "Not Found" in title else "403"'
new_line3 = 'error_type = "404" if "404" in str(title) or "Not Found" in str(title) else "403"'
content = content.replace(old_line3, new_line3)

with open("src/crawl4ai_mcp/__init__.py", "w") as f:
    f.write(content)
