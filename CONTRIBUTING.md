# Contributing

[General guidelines](https://github.com/ewoks-kit/.github/blob/main/shared/CONTRIBUTING.md)

## Pixi

### Development setup

Prerequisites:

- Stable [Rust](https://rustup.rs/) with `cargo` and `rustfmt` on `PATH`.
- Native compiler/linker: `build-essential` on Debian/Ubuntu, Xcode Command Line
  Tools on macOS, or Visual Studio C++ Build Tools with Windows SDK on Windows.

From the repository root:

```bash
pixi install
```

Pixi installs the development dependencies and builds the Rust extension in
editable mode. Release wheels are not used for this checkout.

### Run tests and checks

```bash
pixi run test
pixi run test-lowest
pixi run lint
pixi run typecheck
pixi run full-ci
```

### Run the example

```bash
pixi run graph-to-svg <workflow_path>
```

### Manage dependencies

```bash
pixi update
pixi add <package_name>         # Conda
pixi add --pypi <package_name>  # PyPI
```

## Updating elk-rs

When updating the elk-rs revision in `rust/Cargo.toml`, update the revision
and source links in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) and the
copies of the upstream [license](LICENSES/elk-rs/LICENSE) and
[attribution notice](LICENSES/elk-rs/NOTICE) together.
