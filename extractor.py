import re
import json
import os

def clean_latex(text):
    # Remove \chapter{...}
    text = re.sub(r'\\chapter\{.*?\}', '', text)
    # Handle \lettrine{T}{he} -> <span class="lettrine">T</span>he
    text = re.sub(r'\\lettrine\{(.*?)\}\{(.*?)\}', r'<span class="dropcap">\1</span>\2', text)
    # Handle \textit{...} -> <i>...</i>
    text = re.sub(r'\\textit\{(.*?)\}', r'<i>\1</i>', text)
    # Handle \textbf{...} -> <b>...</b>
    text = re.sub(r'\\textbf\{(.*?)\}', r'<b>\1</b>', text)
    # Handle `` and '' quotes
    text = text.replace('``', '“').replace("''", '”').replace('`', '‘').replace("'", '’')
    # Handle em-dash
    text = text.replace('---', '—').replace('--', '–')
    # Remove remaining backslashes and commands (crude fallback)
    # text = re.sub(r'\\[a-zA-Z]+', '', text)
    
    # Split into paragraphs by double newlines or single newlines that look like paragraph breaks
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    if not paragraphs: # fallback for single line chapters or different spacing
        paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
        
    return paragraphs

def extract_book_data(base_path):
    main_tex_path = os.path.join(base_path, '[dot].tex')
    with open(main_tex_path, 'r', encoding='utf-8') as f:
        main_content = f.read()

    # Extract Title and Author
    title = "." # Hardcoded from what I saw in titlepage
    subtitle = "second row, second seat"
    author = "Ashutosh Vishwakarma"

    # Find included chapters
    chapter_includes = re.findall(r'\\include\{chapters/(.*?)\}', main_content)
    
    book_data = {
        "title": title,
        "subtitle": subtitle,
        "author": author,
        "chapters": []
    }

    for ch_file in chapter_includes:
        ch_path = os.path.join(base_path, 'chapters', f'{ch_file}.tex')
        if os.path.exists(ch_path):
            with open(ch_path, 'r', encoding='utf-8') as f:
                ch_content = f.read()
            
            # Get chapter title
            ch_title_match = re.search(r'\\chapter\{(.*?)\}', ch_content)
            ch_title = ch_title_match.group(1) if ch_title_match else ch_file
            
            # Clean content
            paragraphs = clean_latex(ch_content)
            
            book_data["chapters"].append({
                "id": ch_file,
                "title": ch_title,
                "paragraphs": paragraphs
            })

    return book_data

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(base_dir, "book_data.json")
    
    data = extract_book_data(base_dir)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"Extraction complete. Data saved to {output_file}")
