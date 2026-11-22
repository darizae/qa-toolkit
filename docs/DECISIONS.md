# Product decisions and provenance

2026-11-22 — Initial direction:

1. **Separate public repo:** `darizae/qa-toolkit`, locally at `~/repos/qa-toolkit`; do not add code or docs to Flowstead to distribute this product.
2. **Python core:** one package, `evidence-driven-qa` (distribution name provisional until PyPI availability is verified), with `qa-toolkit` CLI and optional `qa-toolkit-mcp` stdio adapter.
3. **Portable Agent Skill:** `skills/evidence-driven-qa/SKILL.md`, manual project/user-level installation initially. Marketplace manifests are deferred until validated against target platforms.
4. **Open core:** MIT license for independently authored starter. Paid value, if developed, will be in managed services, support and team features; no billing implemented.
5. **Flowstead case study:** real user-owned example, currently private; never copy its code, docs or fixtures into this public repository. Publish only independent synthetic examples and redacted evidence with authorization.
6. **Static archived reference:** analyzed for abstract engineering principles only. No reconstructed source, documentation, naming, implementation, data, auth or infrastructure artifacts may enter this project.
7. **Truth in QA:** static references cannot certify coverage; model uncertainty and evidence explicitly.
8. **Safety:** MCP v0 is local stdio, read-only, bounded to a project path, with no execution or network operations. Future remote MCP requires authentication, tenant-level isolation and reviewed tools.

Tradeoffs: this first public commit deliberately implements only conservative discovery instead of pretending to provide autonomous testing. Version and product name can change before a stable PyPI release.
