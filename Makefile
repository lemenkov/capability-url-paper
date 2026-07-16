# SPDX-FileCopyrightText: 2026 Peter Lemenkov <lemenkov@gmail.com>
# SPDX-License-Identifier: CC0-1.0

all:
	python fig01_plot_inline_vs_reference.py
	python fig02_plot_output_publishing.py
	python fig03_plot_routing_policy.py
	pdflatex article_capability_urls.tex
	# We have to run it twice for cross-references. Any place where LaTeX
	# has to refer to a number it won't know until it has read further down
	# the document.
	pdflatex article_capability_urls.tex

