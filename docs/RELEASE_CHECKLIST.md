# v0.1.0 release record — 2026-11-22

**Status: published on GitHub, PyPI and the official MCP Registry.**

## Completed publication gates

- [x] PyPI package name `evidence-driven-qa` and version `0.1.0` verified
- [x] Fresh Python 3.13 virtual-environment wheel installation and CLI smoke
- [x] 12 local tests passed, including negative case validation and an actual MCP stdio client session
- [x] `ruff check src tests` clean
- [x] Build generated both wheel and sdist; `twine check dist/*` passed
- [x] `server.json` validated with official `mcp-publisher validate`
- [x] README PyPI ownership marker matches `io.github.darizae/evidence-driven-qa`
- [x] Original synthetic OpenAPI, reviewed answers, and indexed-case example committed
- [x] No reconstructed-archive code or private Flowstead assets included
- [x] GitHub annotated `v0.1.0` tag and release published
- [x] PyPI `0.1.0` wheel and sdist uploaded and remotely verified
- [x] Official MCP Registry entry `io.github.darizae/evidence-driven-qa@0.1.0` published and remotely confirmed **active**

## Release references

- Git source: https://github.com/darizae/qa-toolkit/commit/0e888d34515592fea0b3b77ad6b186309b32b7b8
- GitHub release: https://github.com/darizae/qa-toolkit/releases/tag/v0.1.0
- PyPI: https://pypi.org/project/evidence-driven-qa/0.1.0/
- MCP Registry API: https://registry.modelcontextprotocol.io/v0.1/servers?search=io.github.darizae/evidence-driven-qa

## Future milestones, not release claims

- [ ] Agent skill exercise on an unrelated second application
- [ ] Assertion-level proof, real test execution adapters and recorded evidence
- [ ] Playwright artifact import, consolidated reports and additional surface adapters
- [ ] Optional hosted HTTP MCP app

No current CLI or MCP operation should be interpreted as proof of executed integration-test coverage.
