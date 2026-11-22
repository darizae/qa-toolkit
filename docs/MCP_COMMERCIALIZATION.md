# MCP distribution and commercial options (2026-11-22)

## What MCP is

Model Context Protocol (MCP) allows an agent to call a tool server. It is a transport and tool contract, not a merchant-of-record or automatic payment system. The official MCP Registry is a **metadata index**; packages or hosted services live elsewhere.

## Distribution layers

1. **Local Python CLI and stdio MCP server:** same MIT-licensed read-only core, package and manual client configuration. No account or payment required. The prototype exists.
2. **PyPI + MCP Registry:** publish an actual built/tested Python package and validated `server.json` package metadata, then use the official MCP publishing process. **Not published yet.** Registry ownership uses its documented namespace/authentication rules.
3. **Remote MCP app:** secure HTTPS Streamable HTTP endpoint, OAuth/account-based authentication, project/workspace scoping, secret redaction, rate limits, audit logs, deletion controls, deployment monitoring and privacy policy. **Not implemented.**
4. **Commercial service:** subscriptions or usage-based plans for hosted execution, evidence retention, multiple repos and team workflows. Own accounts, checkout and entitlements live on an approved external service; no payment logic in the local core.

## Critical platform policy

As checked 2026-11-22, OpenAI's ChatGPT plugin guidance forbids selling or promoting digital subscriptions/services inside ChatGPT plugin experiences, even via indirect in-plugin upsells; existing independently purchased paid account entitlements may be used after sign-in. The permitted external checkout documentation is primarily for eligible physical goods and does **not** override the digital-services restriction. A paid QA SaaS is plausible as an independent website/service, but do not use the ChatGPT plugin to purchase or upsell it unless platform policy explicitly permits that later.

A ChatGPT app requires separately hosted MCP functionality, OpenAI-specific packaging/review and relevant policies; a local stdio MCP server alone is not a ChatGPT marketplace listing. Claude Code plugins have separate distribution mechanics. Neither registry nor directory implies acceptance or revenue sharing.

## Go-to-market hypothesis

- Free: local audit, open skill, core evidence schema and client adapters.
- Potential paid: managed scheduled QA, private historical reports, team policies, security review and support.
- Evidence of demand before billing: at least two independent projects, demonstrated caught faults, reproducible reports, install experience and user interviews.

## Useful official references

- [MCP Registry](https://github.com/modelcontextprotocol/registry)
- [MCP Registry publisher docs](https://github.com/modelcontextprotocol/registry/tree/main/docs)
- [OpenAI plugin guidelines](https://developers.openai.com/plugins/plugin-guidelines)
- [OpenAI plugin packaging](https://developers.openai.com/plugins/build/plugins)
- [OpenAI plugin developer terms](https://openai.com/policies/developer-apps-terms/)
- [Claude Code plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)

Verify all platform rules again before requesting publication or enabling billing.
