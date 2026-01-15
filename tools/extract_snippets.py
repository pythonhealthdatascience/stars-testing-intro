#!/usr/bin/env python
"""
Extract individual functions and write as separate files in `pages/code/`.
"""

from pathlib import Path

import ast
import textwrap


# Get path to project root
ROOT = Path(__file__).resolve().parents[1]

# Directory containing the example package
SRC_DIR = ROOT / "examples" / "python_package"

# Output directory for generated snippet files used in website
OUT_DIR = ROOT / "pages" / "code"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Source files to process. Each function in these files will be written
# to its own snippet file in OUT_DIR.
FILES = [
    SRC_DIR / "src" / "waitingtimes" / "patient_analysis.py",
    SRC_DIR / "tests" / "test_functional.py",
    SRC_DIR / "tests" / "test_unit.py",
    SRC_DIR / "tests" / "test_back.py",
    SRC_DIR / "tests" / "test_intro_simple.py",
    SRC_DIR / "tests" / "test_intro_parametrised.py"
]


def extract_functions(src_path):
    """
    Yield (function_name, source_string) for each top-level function.

    The returned `source_string` contains the full function definition
    (signature + body) exactly as it appears in the original file,
    sliced using the AST node line numbers. Imports and other module-level
    code are not included.

    Parameters
    ----------
    src_path : Path
        Path to a Python source file from which to extract top-level
        function definitions.

    Yields
    ------
    tuple[str, str]
        Pairs of (function_name, source_string), where `function_name` is
        the name of the top-level function and `source_string` is the exact
        function definition text as it appears in `src_path`.
    """
    source = src_path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    lines = source.splitlines(keepends=True)

    # Only look at top-level statements
    for node in tree.body:
        # Treat each top-level `def` as a separate snippet
        if isinstance(node, ast.FunctionDef):
            start = node.lineno - 1
            end = node.end_lineno
            func_src = "".join(lines[start:end])
            yield node.name, func_src


def extract_imports(src_path):
    """
    Return a string containing only the top-level import statements from
    src_path, excluding the module docstring and any functions/classes.
    """
    source = src_path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    lines = source.splitlines(keepends=True)

    import_lines = []

    for node in tree.body:
        # Skip module docstring (an Expr with Constant str at top)
        if (
            isinstance(node, ast.Expr)
            and isinstance(node.value, ast.Constant)
            and isinstance(node.value.value, str)
        ):
            continue

        if isinstance(node, (ast.Import, ast.ImportFrom)):
            start = node.lineno - 1
            end = node.end_lineno
            import_lines.append("".join(lines[start:end]))

        # Ignore FunctionDef, ClassDef, etc.

    return "".join(import_lines)


def main():
    """
    Extract all top-level functions from the configured FILES and write each
    to a separate snippet file under OUT_DIR.

    The output filename convention is:
        <source_stem>__<function_name>.py
    """
    for src in FILES:
        # File stem without extension, e.g. "patient_analysis"
        rel_stem = src.stem

        #  Write imports-only snippets
        imports_src = extract_imports(src)
        if imports_src.strip():
            imports_file = OUT_DIR / f"{rel_stem}__imports.py"
            imports_file.write_text(imports_src, encoding="utf-8")
            print(f"Wrote {imports_file}")

        # Write one snippet per top-level function
        for name, func_src in extract_functions(src):
            # Build the snippet filename
            out_name = f"{rel_stem}__{name}.py"
            out_file = OUT_DIR / out_name
            # Remove a level of common indentation to make the snippet neat
            # when shown in documentation, without altering the code itself
            cleaned = textwrap.dedent(func_src)
            # Write the snippet file.
            out_file.write_text(cleaned, encoding="utf-8")
            print(f"Wrote {out_file}")


if __name__ == "__main__":
    main()
