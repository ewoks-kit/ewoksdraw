# ewoksdraw

[![Pipeline](https://github.com/ewoks-kit/ewoksdraw/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/ewoks-kit/ewoksdraw/actions/workflows/test.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License](https://img.shields.io/github/license/ewoks-kit/ewoksdraw)](https://github.com/ewoks-kit/ewoksdraw/blob/main/LICENSE.md)
[![Coverage](https://codecov.io/gh/ewoks-kit/ewoksdraw/branch/main/graph/badge.svg)](https://codecov.io/gh/ewoks-kit/ewoksdraw)

A library to generate SVG mock-ups out of Ewoks workflows.

## Quick start

```bash
pip install "git+https://github.com/ewoks-kit/ewoksdraw.git"
```

```python
from ewokscore import load_graph
from ewoksdraw import graph_to_svg

# Load a graph with Ewokscore 5.1
graph = load_graph(...)

# Generate the SVG document
svg = graph_to_svg(graph)

with open("my_workflow.svg", "w", encoding="utf-8") as stream:
    stream.write(svg)
```
