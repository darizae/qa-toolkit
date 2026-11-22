# MCP distribution — free and open source

**Official MCP Registry listing:** `io.github.darizae/evidence-driven-qa@0.1.0` — published 2026-11-22.

- Registry: https://registry.modelcontextprotocol.io/v0.1/servers?search=io.github.darizae/evidence-driven-qa
- Python package: https://pypi.org/project/evidence-driven-qa/0.1.0/
- GitHub release: https://github.com/darizae/qa-toolkit/releases/tag/v0.1.0

The toolkit includes a **local, read-only MCP stdio server** under the MIT license. It has no subscription, account, or paywall.

## Three complementary interfaces

1. **CLI:** `qa-toolkit surface`, `qa-toolkit cases` and `qa-toolkit audit`.
2. **Local MCP:** `qa-toolkit-mcp --project /absolute/path` or `uvx evidence-driven-qa --project /absolute/path`. It exposes local read-only tools to coding agents.
3. **Agent Skill:** `npx skills add darizae/qa-toolkit --skill evidence-driven-qa`.

The same deterministic modules power CLI and MCP. The portable skill guides the agent in understanding intended behavior, designing stories and indexing scenarios.

## MCP Registry publishing

`server.json` declares the GitHub-owned namespace `io.github.darizae/evidence-driven-qa`, PyPI package `evidence-driven-qa`, version `0.1.0` and stdio transport. PyPI confirms ownership via the README's `mcp-name: io.github.darizae/evidence-driven-qa` marker.

Registry submission used `mcp-publisher validate server.json`, GitHub-token namespace authentication and `mcp-publisher publish server.json`. The Registry verified the package and returned an active listing.

The Registry is a discovery index; code installs from PyPI. An MCP Registry listing **is not** the same as a hosted ChatGPT app.

## Free-first future

An optional hosted Streamable HTTP server could be considered with account authorization, tenant isolation and platform review. This is neither necessary nor currently implemented. The local CLI, skill and MCP server are intended to remain freely usable.

## Security

All MCP tool file requests are constrained to an explicit project root. No arbitrary command execution, test running, network access, file edits, credential retrieval or remote integrations are exposed by the current tools. OpenAPI declarations are treated as hints, not authorization truth.

## References

- [MCP Registry publisher guide](https://github.com/modelcontextprotocol/registry/tree/main/docs)
- [MCP PyPI package verification](https://github.com/modelcontextprotocol/registry/blob/main/docs/modelcontextprotocol-io/package-types.mdx)
- [MCP publisher authentication](https://github.com/modelcontextprotocol/registry/blob/main/docs/modelcontextprotocol-io/authentication.mdx)
