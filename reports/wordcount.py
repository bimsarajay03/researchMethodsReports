import re
import sys

# Environments whose content should never count towards the word limit
# (figures/tables including their captions, and the reference list).
EXCLUDED_ENVIRONMENTS = ['figure', 'table', 'thebibliography']


def remove_environments(text, envs):
    for env in envs:
        pattern = re.compile(r'\\begin\{' + env + r'\*?\}.*?\\end\{' + env + r'\*?\}', re.DOTALL)
        text = pattern.sub('', text)
    return text


def strip_latex(text):
    # Remove comments
    text = re.sub(r'%.*', '', text)

    # Remove whole environments that are excluded from the word count
    # (figures, tables, and the bibliography/reference list).
    text = remove_environments(text, EXCLUDED_ENVIRONMENTS)

    # Remove any bibliography-related commands left outside the environment
    # (e.g. \bibliographystyle{...}, \bibliography{...}, \renewcommand{\bibname}{...}).
    text = re.sub(r'\\bibliographystyle\{[^}]*\}', '', text)
    text = re.sub(r'\\bibliography\{[^}]*\}', '', text)
    text = re.sub(r'\\(newcommand|renewcommand)\s*(\[[^\]]*\])?\{[^}]*\}(\{[^}]*\})?', '', text)

    # Remove \begin{...} and \end{...} markers for remaining environments
    # (their inner content, e.g. itemize/enumerate body text, still counts).
    text = re.sub(r'\\(begin|end)\{[^}]*\}', '', text)

    # Remove heading commands together with their title text; headings
    # (chapter/section/subsection/subsubsection titles) do not count as body prose.
    text = re.sub(r'\\(chapter|section|subsection|subsubsection)\*?\s*(\[[^\]]*\])?\{[^}]*\}', '', text)

    # Remove \addcontentsline{toc}{chapter}{Title} -- takes three brace groups,
    # the last of which duplicates a heading title and must not leak through.
    text = re.sub(r'\\addcontentsline\s*\{[^}]*\}\{[^}]*\}\{[^}]*\}', '', text)

    # Remove common non-text commands with arguments
    text = re.sub(r'\\(documentclass|usepackage|geometry|titleformat|vspace|hspace|setcounter|label|ref|cite|href|url|includegraphics|caption|captionof)\s*(\[[^\]]*\])?\{[^}]*\}', '', text)
    # Remove commands with optional and mandatory args that produce no text
    text = re.sub(r'\\(textbf|textit|emph|underline|texttt|large|Large|huge|Huge|small|footnotesize|normalfont|bfseries|normalsize)\s*', '', text)
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
    print(f"Words (excl. {excluded_labels}, figures, tables, references, headings) : {body_count}")
