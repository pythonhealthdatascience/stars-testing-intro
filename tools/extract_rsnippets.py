#!/usr/bin/env python
"""
Extract R library() imports and function definitions.
"""

from pathlib import Path
import re
import textwrap

ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT / "examples" / "r_package"
OUT_DIR = ROOT / "pages" / "code"
OUT_DIR.mkdir(parents=True, exist_ok=True)

FILES = [
    SRC_DIR / "R" / "patient_analysis.R",
]


def extract_r_imports(src_path):
    """
    Extract library() and require() calls from R file.
    
    Returns
    -------
    str
        String containing all library/require statements, one per line.
    """
    source = src_path.read_text(encoding="utf-8")

    # Pattern for: library(pkgname), require(pkgname), etc.
    # Allows quotes or no quotes around package name
    pattern = r'^\s*(library|require)\s*\(\s*["\']?([^\)"\'\n]+)["\']?\s*\)'

    import_lines = []
    for line in source.splitlines():
        if re.match(pattern, line):
            import_lines.append(line.rstrip() + "\n")

    return "".join(import_lines)


def extract_r_functions(src_path):
    """
    Yield (function_name, source_string) for each top-level function in R.

    Includes any Roxygen2 docstrings (#' comments) that precede the function.

    Pattern matched: function_name <- function(...) { ... }

    Yields
    ------
    tuple[str, str]
        (function_name, full_source_with_docstring)
    """
    source = src_path.read_text(encoding="utf-8")
    lines = source.splitlines(keepends=True)

    # Match function definitions at start of line (allowing indentation)
    # Captures: name <- function(args) {
    func_pattern = r'^\s*(\w+)\s*<-\s*function\s*\('

    i = 0
    while i < len(lines):
        # Check if this line is a function definition
        if re.match(func_pattern, lines[i]):
            func_name = re.match(func_pattern, lines[i]).group(1)

            # Walk backwards to find preceding Roxygen docstrings
            docstring_start = i
            j = i - 1
            while j >= 0:
                stripped = lines[j].strip()
                # Roxygen lines start with #'
                if stripped.startswith("#'"):
                    docstring_start = j
                    j -= 1
                # Allow blank lines between docstring and function
                elif stripped == "":
                    j -= 1
                else:
                    # Stop when we hit non-Roxygen, non-blank line
                    break

            # Now find the end of function (matching closing brace)
            brace_count = lines[i].count('{') - lines[i].count('}')
            end = i + 1

            while end < len(lines) and brace_count > 0:
                brace_count += lines[end].count('{') - lines[end].count('}')
                end += 1

            # Extract full source (docstring + function)
            func_src = "".join(lines[docstring_start:end])

            yield func_name, func_src

            # Move to next line after function
            i = end
        else:
            i += 1


def main():
    """
    Extract all top-level functions and imports from configured FILES.

    Writes each import block to: <stem>__imports.R
    Writes each function to: <stem>__<function_name>.R
    """
    for src in FILES:
        stem = src.stem

        # Extract and write imports-only snippets
        imports_src = extract_r_imports(src)
        if imports_src.strip():
            imports_file = OUT_DIR / f"{stem}__imports.R"
            imports_file.write_text(imports_src, encoding="utf-8")
            print(f"Wrote {imports_file}")

        # Extract and write one snippet per top-level function
        for name, func_src in extract_r_functions(src):
            out_name = f"{stem}__{name}.R"
            out_file = OUT_DIR / out_name
            # Remove common indentation for neat documentation display
            cleaned = textwrap.dedent(func_src)
            out_file.write_text(cleaned, encoding="utf-8")
            print(f"Wrote {out_file}")


if __name__ == "__main__":
    main()
