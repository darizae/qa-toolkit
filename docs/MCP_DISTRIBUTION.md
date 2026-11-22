# MCP distribution — free and open source

This toolkit provides a **local, read-only MCP stdio server** as part of the open-source Python distribution. It does not require a subscription, login, paid plan, or hosted account.

## Three complementary ways to use it

1. **Python CLI:** `qa-toolkit surface`, `qa-toolkit cases`, and `qa-toolkit audit`.
2. **Local MCP:** `qa-toolkit-mcp --project /absolute/path` (or `uvx evidence-driven-qa --project /absolute/path`). It exposes read-only tools to coding agents.
3. **Portable skill:** `npx skills add darizae/qa-toolkit --skill evidence-driven-qa`.

The CLI and MCP share the same deterministic modules. The agent skill asks and answers the product-intent questions; the tools safely extract API declarations and index reviewed answers.

## Official MCP Registry

The MCP Registry is a **metadata discovery index, not an execution service**. Publication requires (a) an actually available PyPI package; (b) a `server.json` satisfying the current registry schema; (c) a PyPI README marker `mcp-name: io.github.darizae/evidence-driven-qa`; (d) publisher authentication and registry validation.

The repository includes `server.json` and the README marker. The `evidence-driven-qa` entry point serves MCP through stdio, as does `qa-toolkit-mcp`.

See:
- [MCP official registry guide](https://github.com/modelcontextprotocol/registry/tree/main/docs)
- [Package types and PyPI ownership](https://github.com/modelcontextprotocol/registry/blob/main/docs/modelcontextprotocol-io/package-types.mdx)
- [Authentication and namespace rules](https://github.com/modelcontextprotocol/registry/blob/main/docs/modelcontextprotocol-io/authentication.mdx)
- [PyPI publishing guide](https://docs.pypi.org/publishing/publishing-to-pypi/)

## Hosted apps and monetization

A **local stdio MCP server** does not automatically become a hosted ChatGPT app or a cloud service. A hosted HTTP app needs a deployment, authentication, consent, tenant scoping, operational controls, privacy policy, and platform review. We can consider one in the future, but it is not required for the current product.

The current direction is **free, MIT-licensed, open-source distribution**. No paid features or checkout are planned for this release. An independent future service can be considered separately, subject to platform rules.

## Security and scope

All tool file requests are constrained to a designated project root. No arbitrary command execution, test running, network calls or file edits are exposed over MCP. Unknown policy requirements must be resolved from the user's project specifications, not inferred from API declarations alone.
