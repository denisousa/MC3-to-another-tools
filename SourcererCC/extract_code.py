import re
import pandas as pd
import regex

pattern = r"""
\b[\w<>\[\]]+\s+generateSetParameter\s*
\([^)]*\)                 # parâmetros
\s*
(?<block>\{               # nomeia grupo recursivo
    (?:                   # conteúdo do bloco
        [^{}]+            # qualquer coisa exceto {}
        |
        (?&block)         # recursivamente outro bloco
    )*
\})
"""


java_keywords = [
    "abstract", "assert", "boolean", "break", "byte",
    "case", "catch", "char", "class", "const",  # 'const' is reserved but not used
    "continue", "default", "do", "double", "else",
    "enum", "extends", "final", "finally", "float",
    "for", "goto",  # 'goto' is reserved but not used
    "if", "implements", "import", "instanceof", "int",
    "interface", "long", "native", "new", "null",
    "package", "private", "protected", "public", "return",
    "short", "static", "strictfp", "super", "switch",
    "synchronized", "this", "throw", "throws", "transient",
    "try", "void", "volatile", "while", "true", "false", "var", "yield", "record", "sealed", "permits", "non-sealed"
]

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.readlines()

def find_file_for_method_id(method_id, stats_lines):
    file_line = None
    for line in stats_lines:
        if line.startswith('f'):
            file_line = line
        
        if method_id in line:
            file_path = '/'.join(file_line.split(',')[2].replace('"','').split('/')[1:])
            return '/'.join(file_path.split('/')[1:])

def get_method_name(method_id, tokens_lines):
    for line in tokens_lines:
        if method_id in line:
            i = 5 
            while(True):
                method_name = line.split(',')[i].split('@@')[0]
                if method_name not in java_keywords:
                    return line.split(',')[i].split('@@')[0]
                i += 1

def extract_clones(results_path, stats_path, tokens_path):
    results = read_file(results_path)
    stats_lines = read_file(stats_path)
    tokens_lines = read_file(tokens_path)

    clone_groups = []
    for line in results:
        if not line.strip() or line.startswith("#"):
            continue
        ids = line.strip().split(',')
        ids = [item for i, item in enumerate(ids) if i % 2 != 0]

        group = []
        for method_id in ids:
            filename = find_file_for_method_id(method_id, stats_lines)
            method_name = get_method_name(method_id, tokens_lines)
            if filename and method_name:
                group.append({'id': method_id, 'file': f'projects_unzip/{filename}', 'method': method_name})
        if group:
            clone_groups.append(group)
    return clone_groups

def extract_method_code(filepath, method_name):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        match = regex.search(pattern, content, regex.DOTALL | regex.VERBOSE)
        # match = re.search(pattern, content, re.DOTALL)
        
        if match:
            code = match.group()
            start_index = match.start()
            end_index = match.end()

            start_line = content.count('\n', 0, start_index) + 1
            end_line = content.count('\n', 0, end_index) + 1

            return code, start_line, end_line

    except FileNotFoundError:
        return None, None, None
    
    return None, None, None

def execute_extraction():
    results_path = "results.pairs"
    stats_path = "tokenizers/block-level/file_block_stats/files-stats-0.stats"
    tokens_path = "tokenizers/block-level/blocks_tokens/files-tokens-0.tokens"

    clones = extract_clones(results_path, stats_path, tokens_path)
    df = []
    results_txt = ""

    with open(f"clone_group.txt", 'w', encoding='utf-8') as f:
        f.write('')
    
    f.close()

    for i, group in enumerate(clones):
        for j, clone in enumerate(group):
            results_txt += f"File: {clone['file']} | Method: {clone['method']}\n"
            code, start_line, end_line = extract_method_code(clone['file'], clone['method'])
            if code:
                results_txt += "Code Snippet:\n" + code + "\n"
                results_txt += f"Start Line: {start_line}, End Line: {end_line}\n"
            else:
                results_txt += "Method code not found.\n"

        results_txt += "="*60 + "\n"

        with open(f"clone_group.txt", 'a', encoding='utf-8') as f:
            f.write(results_txt)
            results_txt = ""
        
        f.close()
        
        df.append({
            'path1': group[0]['file'],
            'method1': group[0]['method'],
            'start_line1': extract_method_code(group[0]['file'], group[0]['method'])[1],
            'end_line1': extract_method_code(group[0]['file'], group[0]['method'])[2],
            'path2': group[1]['file'],
            'method2': group[1]['method'],
            'start_line2': extract_method_code(group[1]['file'], group[1]['method'])[1],
            'end_line2': extract_method_code(group[1]['file'], group[1]['method'])[2],
        })


    df = pd.DataFrame(df)
    df.to_csv('result-pairs.csv', index=False)
