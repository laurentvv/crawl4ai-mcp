import os

TEST_DIR = 'tests'

MAPPING = {
    'clean_ui_artifacts': 'crawl4ai_mcp.utils',
    'remove_links_from_markdown': 'crawl4ai_mcp.utils',
    'sanitize_text': 'crawl4ai_mcp.utils',
    'generate_filename_from_url': 'crawl4ai_mcp.utils',
    'is_safe_path': 'crawl4ai_mcp.utils',
    'get_results_directory': 'crawl4ai_mcp.utils',
    
    '_extract_unique_links': 'crawl4ai_mcp.crawler',
    '_format_markdown_page': 'crawl4ai_mcp.crawler',
    'crawl_and_output_to_markdown': 'crawl4ai_mcp.crawler',
    'results_to_markdown': 'crawl4ai_mcp.crawler',
    '_extract_page_content_and_errors': 'crawl4ai_mcp.crawler',
    
    'list_tools': 'crawl4ai_mcp.server',
    'app': 'crawl4ai_mcp.server',
    'crawl_tool': 'crawl4ai_mcp.server',
    
    'run_sse_server': 'crawl4ai_mcp.cli',
    'run_stdio_server': 'crawl4ai_mcp.cli',
    'main': 'crawl4ai_mcp.cli',
}

def patch_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all "from crawl4ai_mcp import X, Y" or "from crawl4ai_mcp.__init__ import X"
    def replacer(match):
        imports = match.group(2).split(',')
        imports = [i.strip() for i in imports]
        
        new_imports = {}
        for imp in imports:
            # Handle aliases like "remove_links_from_markdown as remove_links_optimized"
            base_imp = imp.split(' as ')[0].strip()
            target_mod = MAPPING.get(base_imp, 'crawl4ai_mcp.utils') # fallback
            
            if target_mod not in new_imports:
                new_imports[target_mod] = []
            new_imports[target_mod].append(imp)
            
        res = []
        for mod, imps in new_imports.items():
            res.append(f"from {mod} import {', '.join(imps)}")
        return "\n".join(res)

    # regex for "from crawl4ai_mcp import A, B"
    # or "from crawl4ai_mcp.__init__ import A"
    # Actually, let's just do a simpler search/replace because imports might be multi-line
    # Let's do a naive parse
    lines = content.split('\n')
    out_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith('from crawl4ai_mcp') and 'import' in line:
            # Gather full import statement
            full_stmt = line
            while '(' in full_stmt and ')' not in full_stmt and i + 1 < len(lines):
                i += 1
                full_stmt += " " + lines[i].strip()
            
            # parse out the imported names
            import_part = full_stmt.split('import', 1)[1]
            import_part = import_part.replace('(', '').replace(')', '').strip()
            names = [n.strip() for n in import_part.split(',')]
            
            new_imports = {}
            for name in names:
                if not name:
                    continue
                base_name = name.split(' as ')[0].strip()
                mod = MAPPING.get(base_name, 'crawl4ai_mcp.utils')
                if mod not in new_imports:
                    new_imports[mod] = []
                new_imports[mod].append(name)
            
            for mod, imps in new_imports.items():
                out_lines.append(f"from {mod} import {', '.join(imps)}")
        else:
            out_lines.append(line)
        i += 1
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(out_lines))


for f in os.listdir(TEST_DIR):
    if f.endswith('.py'):
        patch_file(os.path.join(TEST_DIR, f))
