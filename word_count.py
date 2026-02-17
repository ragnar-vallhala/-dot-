#!/usr/bin/env python3
import os
import re

def count_words_in_latex(file_path):
    """
    Counts words in a .tex file, ignoring LaTeX commands and comments.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return 0

    # 1. Remove comments
    # Matches % and everything until the end of the line
    content = re.sub(r'%.*$', '', content, flags=re.MULTILINE)

    # 2. Handle common text-containing commands
    # Replace \chapter{Title}, \textit{Text}, \textbf{Text}, etc. with their contents
    # This is a bit simplistic but works for most common prose LaTeX
    content = re.sub(r'\\(?:chapter|section|subsection|textit|textbf|emph)\{(.*?)\}', r'\1', content)
    
    # Handle \lettrine{T}{he} -> T he
    content = re.sub(r'\\lettrine\{(.*?)\}\{(.*?)\}', r'\1\2', content)

    # 3. Remove other LaTeX commands (\command or \command[opt]{arg})
    # Remove \command{...}
    content = re.sub(r'\\[a-zA-Z]+\{.*?\}', '', content)
    # Remove \command
    content = re.sub(r'\\[a-zA-Z]+', '', content)

    # 4. Remove LaTeX environments (\begin{...} and \end{...})
    content = re.sub(r'\\begin\{.*?\}.*?\\end\{.*?\}', '', content, flags=re.DOTALL)

    # 5. Clean up extra whitespace and count words
    words = re.findall(r'\b\w+\b', content)
    return len(words)

def main():
    base_dir = "."
    tex_files = []
    
    for root, dirs, files in os.walk(base_dir):
        # Skip hidden directories like .git
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for file in files:
            if file.endswith('.tex'):
                tex_files.append(os.path.join(root, file))

    if not tex_files:
        print("No .tex files found.")
        return

    print(f"{'File Path':<50} | {'Word Count':>10}")
    print("-" * 63)
    
    total_words = 0
    for file_path in sorted(tex_files):
        count = count_words_in_latex(file_path)
        print(f"{file_path:<50} | {count:>10}")
        total_words += count

    print("-" * 63)
    print(f"{'Total':<50} | {total_words:>10}")

if __name__ == "__main__":
    main()
