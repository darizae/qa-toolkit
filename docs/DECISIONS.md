# Product decisions and provenance

2026-11-22 — Active decisions:

1. **Separate open-source repo:** `darizae/qa-toolkit` / `~/repos/qa-toolkit`.
2. **Question-first flow:** API surface → nine questions per operation → approved behavioral contract → meaningful stories → stable indexed cases → test mapping → actual evidence.
3. **Python core:** one package `evidence-driven-qa`, CLI `qa-toolkit`, local stdio MCP server `qa-toolkit-mcp` / `evidence-driven-qa`.
4. **Portable Agent Skill:** project/user-level `evidence-driven-qa` following the Agent Skills specification.
5. **Open source:** MIT license across the CLI, MCP tools and skill. No required paid account, commercial dependency or checkout.
6. **Local-first safety:** MCP is read-only, project-path confined and lacks arbitrary command execution. Requirements cannot be inferred as guaranteed by OpenAPI security hints.
7. **Stable IDs:** generated from HTTP method, path and story key; no case is a test PASS until assertion quality and actual execution evidence are established.
8. **Flowstead case study:** separate private application; no source, docs, secrets or fixtures copied into public repo.
9. **Archived static reference:** conceptual analysis only; never copied, vendored, executed or published.
10. **Optional future:** official MCP Registry discovery; hosted HTTP/ChatGPT app and commercialization only if separately decided. The free local server remains a first-class release.

Package distribution details are tracked in [MCP_DISTRIBUTION.md](MCP_DISTRIBUTION.md); milestones in [ROADMAP.md](ROADMAP.md).
