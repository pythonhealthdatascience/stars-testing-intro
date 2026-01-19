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
    SRC_DIR / "tests" / "testthat" / "test_intro_simple.R",
    SRC_DIR / "tests" / "testthat" / "test_intro_parametrised.R",
    SRC_DIR / "tests" / "testthat" / "test_functional.R",
    SRC_DIR / "tests" / "testthat" / "test_unit.R",
    SRC_DIR / "tests" / "testthat" / "test_back.R"
]

TEST_THAT_PATTERN = r'^\s*(test_that|(?:\w+::)?with_parameters_test_that)\s*\('


def is_test_file(src_path):
    return src_path.name.startswith("test_") or src_path.name.startswith("test-")


def slugify_desc(desc: str, max_words: int = 5, max_len: int = 40) -> str:
    # Keep only first `max_words`
    words = desc.split()
    trimmed = " ".join(words[:max_words])
    # Replace non-alnum with underscores
    slug = re.sub(r"[^0-9A-Za-z]+", "_", trimmed).strip("_")
    # Enforce max length
    return slug[:max_len] or "test"


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


def extract_testthat_blocks(src_path):
    """
    Yield (test_name, source_string) for each top-level test_that() block.

    test_that("description", {
      ...
    })

    test_name is a shortened, slugified version of the description.
    """
    source = src_path.read_text(encoding="utf-8")
    lines = source.splitlines(keepends=True)

    i = 0
    test_idx = 1
    while i < len(lines):
        line = lines[i]
        if re.match(TEST_THAT_PATTERN, line):
            # Try to capture the description inside test_that("...")
            desc_match = re.search(r'test_that\s*\(\s*["\']([^"\']+)["\']', line)
            if desc_match:
                raw_name = desc_match.group(1)
            else:
                raw_name = f"test_{test_idx}"

            slug = slugify_desc(raw_name, max_words=3)
            test_idx += 1

            # Find end of the block: track braces from first '{' onwards
            brace_count = line.count("{") - line.count("}")
            start = i
            i += 1
            while i < len(lines) and brace_count > 0:
                brace_count += lines[i].count("{") - lines[i].count("}")
                i += 1

            end = i  # one past the last line of the block
            test_src = "".join(lines[start:end])
            yield slug, test_src
        else:
            i += 1


def main():
    """
    Extract all imports, functions (R/) and tests (tests/testthat/) from FILES.

    Writes each import block to: <stem>__imports.R
    Writes each function to:     <stem>__<function_name>.R
    Writes each test to:         <stem>__<short_test_name>.R
    """
    for src in FILES:
        stem = src.stem

        # Extract and write imports-only snippets
        imports_src = extract_r_imports(src)
        if imports_src.strip():
            imports_file = OUT_DIR / f"{stem}__imports.R"
            imports_file.write_text(imports_src, encoding="utf-8")
            print(f"Wrote {imports_file}")

        if is_test_file(src):
            # Extract individual test_that() blocks with short names
            for test_name, test_src in extract_testthat_blocks(src):
                out_name = f"{stem}__{test_name}.R"
                out_file = OUT_DIR / out_name
                cleaned = textwrap.dedent(test_src)
                out_file.write_text(cleaned, encoding="utf-8")
                print(f"Wrote {out_file}")
        else:
            # Extract top-level functions with Roxygen docstrings
            for name, func_src in extract_r_functions(src):
                out_name = f"{stem}__{name}.R"
                out_file = OUT_DIR / out_name
                cleaned = textwrap.dedent(func_src)
                out_file.write_text(cleaned, encoding="utf-8")
                print(f"Wrote {out_file}")


if __name__ == "__main__":
    main()
