# ewoksdraw

[![Pipeline](https://github.com/ewoks-kit/ewoksdraw/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/ewoks-kit/ewoksdraw/actions/workflows/test.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License](https://img.shields.io/github/license/ewoks-kit/ewoksdraw)](https://github.com/ewoks-kit/ewoksdraw/blob/main/LICENSE.md)
[![Coverage](https://codecov.io/gh/ewoks-kit/ewoksdraw/branch/main/graph/badge.svg)](https://codecov.io/gh/ewoks-kit/ewoksdraw)

A library to generate SVG mock-ups out of Ewoks workflows.

## Quick start

Using pip:
```bash
pip install "git+https://github.com/ewoks-kit/ewoksdraw.git"
```
Using pixi:
```bash
pixi add --pypi "ewoksdraw @ git+https://github.com/ewoks-kit/ewoksdraw.git"
```

> **Note:** the layout engine is a Rust extension. Prebuilt wheels are provided for Linux (x86_64, aarch64), Windows (x64) and macOS (Intel, arm64). Installing from Git, or on any other platform, builds it from source and requires a [Rust toolchain](https://rustup.rs) and network access to GitHub.

### Python

```python
from ewoks import load_graph
from ewoksdraw import graph_to_svg

# Load a graph with `ewoks.load_graph`
graph = load_graph(...)

# Generate the SVG
graph_to_svg(graph, output_path="my_workflow.svg")
```

## License

The ewoksdraw code and Rust binding use the [MIT license](LICENSE.md). The
bundled elk-rs layout engine uses EPL-2.0; see
[third-party notices](THIRD_PARTY_NOTICES.md) for its license, attribution, and
corresponding source code.
