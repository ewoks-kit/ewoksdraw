# Third-party notices

The ewoksdraw Python code and its Rust binding are licensed under the MIT
license in [LICENSE.md](LICENSE.md).

## elk-rs (Eclipse Layout Kernel)

The compiled layout engine includes code from
[elk-rs](https://github.com/openedges/elk-rs), a Rust port of the Eclipse Layout
Kernel. This code is licensed under the Eclipse Public License 2.0 (EPL-2.0).

The corresponding source code is available under EPL-2.0 at revision
`2191680292b9565592223c22a28b5ef33c3acbad`:

- [Browse the source](https://github.com/openedges/elk-rs/tree/2191680292b9565592223c22a28b5ef33c3acbad).
- [Download the source archive](https://github.com/openedges/elk-rs/archive/2191680292b9565592223c22a28b5ef33c3acbad.tar.gz).

The layout engine is compiled directly from this revision. The upstream
[license](LICENSES/elk-rs/LICENSE) and [attribution notice](LICENSES/elk-rs/NOTICE)
are reproduced without modification and included in the wheel and source
distributions. The upstream notice describes the wider ELK project.

When updating the elk-rs revision in `rust/Cargo.toml`, update these source
links and the copies of the upstream license and notice together.
