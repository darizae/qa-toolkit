# Open-source release checklist

- [ ] Package name available on PyPI and version synchronized in package, docs and MCP manifest
- [ ] Clean virtual environment installation with Python 3.11+ plus wheel/sdist inspection
- [ ] Unit and negative/security tests pass, including rejecting invalid and incomplete case answers
- [ ] MCP stdio client protocol smoke: initialize, list tools, invoke surface/cases/audit
- [ ] Agent Skill instructions and setup paths reviewed
- [ ] Independently authored synthetic OpenAPI, requirements, questionnaire and case registry
- [ ] No reconstructed archived or private Flowstead code, docs, fixtures, secrets or credentials
- [ ] `server.json` schema and PyPI ownership marker validated
- [ ] GitHub repository tagged with release commit
- [ ] PyPI wheel and source distribution published and remotely verified
- [ ] MCP Registry listing published and remotely verified (if publisher auth available)
- [ ] Roadmap / issue statuses revised with actual evidence

The official MCP Registry indexes metadata only; PyPI hosts the installable distribution. Publishing both is separate from building a hosted ChatGPT app.
