# Services layout

Each service has its own `pyproject.toml` and isolated `uv` environment.

This is recommended for GitOps + Kubernetes projects because:

- dependencies stay isolated per service;
- deployment lifecycle is independent;
- upgrades and rollbacks are safer.

If you need shared tooling, add a thin root-level workspace later, but keep runtime dependencies per service.
