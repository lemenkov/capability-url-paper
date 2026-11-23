<!--
SPDX-FileCopyrightText: 2026 Peter Lemenkov <lemenkov@gmail.com>
SPDX-License-Identifier: CC-BY-4.0
-->

# Return by Reference: Bounding Tool-Output Context Cost in LLM Agents with Capability URLs

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24477585.svg)](https://doi.org/10.5281/zenodo.24477585)

LaTeX source, figures, and measurement harness for the paper.

- **Paper (PDF):** <https://doi.org/10.5281/zenodo.24477585>
- **Reference implementation:** [mcp-sandbox](https://github.com/lemenkov/mcp-sandbox)
- **Measurement harness:** [`bench/token_cost.py`](bench/token_cost.py)

## Build

```sh
make            # regenerates the figures, then runs pdflatex twice
```

Requires a TeX distribution with `pdflatex`, plus Python with Matplotlib for the figures.

## Reproduce the measurements

```sh
pip install tiktoken
python bench/token_cost.py                 # synthetic size sweep
python bench/token_cost.py --dir outputs/  # real files
```

## Cite

> Peter Lemenkov. *Return by Reference: Bounding Tool-Output Context Cost in LLM Agents with Capability URLs.* Preprint, Zenodo, 2026. doi:[10.5281/zenodo.24477585](https://doi.org/10.5281/zenodo.24477585)

## License

Paper text and figures: CC BY 4.0. Figures 1–3 are by Polina Lemenkova, who keeps the copyright and licenses them under CC BY 4.0.
Measurement harness: Apache-2.0. See [AUTHORS](AUTHORS) and [LICENSES/](LICENSES/).
