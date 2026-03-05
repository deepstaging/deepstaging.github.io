# deepstaging.github.io

Public documentation site for the Deepstaging ecosystem. Aggregates documentation from:

- [Deepstaging](https://deepstaging.github.io/deepstaging/) — Source generators for effects modules, strong IDs, configuration, and more
- [Deepstaging.Roslyn](https://deepstaging.github.io/roslyn/) — Fluent toolkit for building Roslyn source generators, analyzers, and code fixes
- [Deepstaging.Web](https://deepstaging.github.io/web/) — Source generators for full-stack web applications

## Local development

```bash
./build/docs.sh serve    # Landing page only
./build/docs.sh build    # Build all sites
```

## How it works

Each private repo triggers a `repository_dispatch` event when docs change. The deploy workflow checks out all repos, builds each site into a subdirectory, and deploys the combined output to GitHub Pages.

## License

SPDX-License-Identifier: RPL-1.5
