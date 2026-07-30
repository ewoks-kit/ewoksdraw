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

### Pixi

```bash
pixi install
pixi run test
pixi run test-lowest
pixi run lint
pixi run typecheck
pixi run full-ci
pixi run graph-to-svg acyclic1
```

### Python

```python
from ewoks import load_graph
from ewoksdraw import graph_to_svg

# Load a graph with `ewoks.load_graph`
graph = load_graph(...)

# Generate the SVG
graph_to_svg(graph, output_path="my_workflow.svg")
```
