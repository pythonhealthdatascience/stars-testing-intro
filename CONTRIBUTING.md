# Contributing

This file is for contributors. It describes how the `stars-testing-intro` site is set-up and quality controlled.

## Example code

The example code is contained in `examples`.

We want to be able to show individual functions without imports in the quarto website, so we have a script `tools/extract_snippets.py` which extracts each function without imports into individual `.py` files within `pages/code/`. This is run each time the site is built via Quarto's `pre-render` hook.

Example commands for the python package:

* `pip install -e examples/python_package`
* `pytest examples/python_package`

Example commands for the R package (having first opened R console by running `R` - escaped with `quit()`):

* `devtools::document("examples/r_package")`
* `devtools::check("examples/r_package")`
* `withr::with_dir("examples/r_package", {usethis::use_mit_license()})`
* ` devtools::test("examples/r_package")`

## Rendering the quarto site

The site is hosted on GitHub pages and rendered via GitHub actions. It uses a Docker environment which has the Python and R requirements.

If you wish to render it locally, please refer to the `environment.yaml` and `renv.lock` files.

### Common `reticulate` error and solution

When rendering a Quarto document containing executable python code with `reticulate`, you might encounter:

```
Error in `use_condaenv()`:
! Unable to locate conda environment 'des-rap-book'.
Backtrace:
    ▆
 1. └─reticulate::use_condaenv("des-rap-book", required = TRUE)
```

This can occur when multiple Conda or Mamba installations exist (e.g. `mambgaforge`, `miniconda3`), or if R is using a different search path than the shell. By default, `reticulate` only looks in one location for environments, which can cause problems when environments are not where `reticulate` expects.

To fix this, **set the `RETICULATE_CONDA` environment variable** to the correct Conda or Mamba executable. To find the path to your executable, run:

```
conda env list
```

Look for your environment in the list. For example, if your environment is at `/home/amy/mambaforge/envs/des-rap-book`, then your Conda executable is likely at `/home/amy/mambaforge/bin/conda`.

Set the environment variable like so:

```
export RETICULATE_CONDA=/home/amy/mambaforge/bin/conda
```

Now render your book:

```
quarto render
```

To avoid needing to set `RETICULATE_CONDA` every time you open a new terminal, add the export command to an `.Renviron` file in your project directory. This file is not tracked by Git, and is specific to you. Create the file and add:

```
RETICULATE_CONDA=/home/amy/mambaforge/bin/conda
```
