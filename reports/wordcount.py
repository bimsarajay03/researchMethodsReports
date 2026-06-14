import re
import sys

def strip_latex(text):
    # Remove comments
    text = re.sub(r'%.*', '', text)
    # Remove \begin{...} and \end{...} blocks (environments)
    text = re.sub(r'\\(begin|end)\{[^}]*\}', '', text)
    # Remove common non-text commands with arguments
    text = re.sub(r'\\(documentclass|usepackage|geometry|titleformat|vspace|hspace|newcommand|renewcommand|setcounter|addcontentsline|label|ref|cite|href|url|includegraphics|captionof)\s*(\[[^\]]*\])?\{[^}]*\}', '', text)
    # Remove commands with optional and mandatory args that produce no text
    text = re.sub(r'\\(chapter\*?|section\*?|subsection\*?|subsubsection\*?|textbf|textit|emph|underline|texttt|large|Large|huge|Huge|small|footnotesize|normalfont|bfseries|normalsize)\s*', '', text)
    # Remove display math
    text = re.sub(r'\$\$.*?\$\$', '', text, flags=re.DOTALL)
    # Remove inline math
    text = re.sub(r'\$.*?\$', '', text)
    # Remove remaining LaTeX commands (with or without arguments)
    text = re.sub(r'\\[a-zA-Z]+\*?(\[[^\]]*\])?(\{[^}]*\})?', '', text)
    # Remove leftover braces and brackets
    text = re.sub(r'[{}\[\]]', '', text)
    # Remove standalone backslashes
    text = re.sub(r'\\', '', text)
    # Collapse whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def count_words(text):
    words = text.split()
    return len(words)

EXCLUDED_CHAPTERS = ['acknowledgement', 'abstract']

def remove_excluded_chapters(text):
    """Remove chapter blocks whose title matches the exclusion list."""
    # Split on \chapter occurrences, keeping the delimiter
    parts = re.split(r'(\\chapter\*?\s*\{[^}]*\})', text)
    filtered = []
    skip = False
    for part in parts:
        if re.match(r'\\chapter\*?\s*\{[^}]*\}', part):
            title = re.search(r'\{([^}]*)\}', part).group(1).strip().lower()
            skip = any(excl in title for excl in EXCLUDED_CHAPTERS)
            if not skip:
                filtered.append(part)
        else:
            if not skip:
                filtered.append(part)
    return ''.join(filtered)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python wordcount.py <file.tex>")
        sys.exit(1)

    filepath = sys.argv[1]

    with open(filepath, 'r', encoding='utf-8') as f:
        raw = f.read()

    cleaned_full = strip_latex(raw)
    total = count_words(cleaned_full)

    body_only = remove_excluded_chapters(raw)
    cleaned_body = strip_latex(body_only)
    body_count = count_words(cleaned_body)

    excluded_labels = ', '.join(c.capitalize() for c in EXCLUDED_CHAPTERS)

    print(f"File                                    : {filepath}")
    print(f"Total words                             : {total}")
    print(f"Words (excl. {excluded_labels}) : {body_count}")
