### General guidelines

<a href="https://github.com/ewoks-kit/.github/blob/main/shared/CONTRIBUTING.md" target="_blank">CONTRIBUTING.md</a>

### Pixi

This project is managed by [Pixi](https://pixi.prefix.dev/) with a single environment (`default`).

We reproduce below the most relevant commands. For more, see [Pixi's Getting Started](https://pixi.prefix.dev/latest/getting_started/)

#### Install the project

```bash
pixi install
pixi update
```

#### Run the tests

```bash
pixi run test
pixi run test-lowest
pixi run lint
pixi run typecheck
pixi run full-ci
```

#### Run the example

Turn a workflow into a SVG

```
pixi run graph-to-svg <workflow_path>
```

If `workflow_name` is not given, `ewoksdraw` will use a test workflow.


#### Add dependencies

```bash
pixi add <package_name>
```

By default, this will install the conda package (if there is one). To install from PyPI:

```bash
pixi add --pypi <package_name>
```