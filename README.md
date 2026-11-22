<div align="center">

# 🧭 Evidence-Driven QA

### From API surfaces to test stories to traceable evidence.

**Discover · Question · Specify · Index · Audit**

[![PyPI](https://img.shields.io/pypi/v/evidence-driven-qa?label=PyPI)](https://pypi.org/project/evidence-driven-qa/)
[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](https://pypi.org/project/evidence-driven-qa/)
[![License: MIT](https://img.shields.io/badge/License-MIT-22a06b)](LICENSE)
[![MCP Registry](https://img.shields.io/badge/MCP_Registry-listed-654ff0)](https://registry.modelcontextprotocol.io/v0.1/servers?search=io.github.darizae/evidence-driven-qa)
[![Agent Skills](https://img.shields.io/badge/Agent_Skills-portable-blueviolet)](skills/evidence-driven-qa/SKILL.md)
[![Open Source](https://img.shields.io/badge/open_source-forever-2ea043)](LICENSE)

**An open-source Python CLI, local MCP server and portable Agent Skill for systematic QA planning.**

[Quick start](#-quick-start) · [The methodology](#-how-it-works) · [Agent setup](#-agent-setup) · [MCP setup](#-mcp-server-setup) · [Documentation](#-documentation)

</div>

---

## ✦ The idea

Great integration tests begin **before** writing test code. First map the actual API surface. For every operation ask: *who may do this, who must be denied, what conditions and relationships must hold, what changes, and what observable result would prove it?* Convert the answers into test stories, assign durable case IDs, and then inspect the existing test suite.

```text
    OPENAPI / SOURCE CONTRACT
              │
              ▼
   ① DISCOVER TESTABLE SURFACE
      endpoints · actors · states
              │
              ▼
   ② ASK & ANSWER QUESTIONS
      allowed? forbidden? conditions?
      relationships? effects? proof?
              │
              ▼
   ③ DESIGN TEST STORIES
      positive · negative · edge cases
              │
              ▼
   ④ CREATE INDEXED CASES
      stable IDs · expected evidence
              │
              ▼
   ⑤ AUDIT EXISTING TESTS
      reference matching (not a PASS)
              │
              ▼
   ⑥ IMPLEMENT → EXECUTE → REPORT
         planned next stages
```

The design is **agent-assisted, deterministic at the tool boundary**. AI agents reason about semantics and ask for missing product decisions. The Python core extracts the surface, validates reviewed stories, generates consistent case IDs and searches existing test sources. It never guesses an authorization policy from OpenAPI or treats a matching test ID as proof of a passing test.

## ✦ Quick start

Install the package (Python 3.11+):

```bash
pip install evidence-driven-qa
```

Or run without a permanent installation using `uvx`:

```bash
uvx --from evidence-driven-qa qa-toolkit --help
```

**1 · Discover the HTTP API surface** from a saved local OpenAPI JSON file:

```bash
qa-toolkit surface --openapi openapi.json --json > qa-surface.json
```

This produces an editable per-endpoint questionnaire: declared routes, input parameters, response codes, available testing topics, and questions about intended behavior.

**2 · Answer the contract questions and write test stories.** Give `qa-surface.json` and the application's requirements to your agent. Ask it to complete the `contract` and `stories` fields using evidence from your project's specification, and to flag ambiguous requirements. Review its answers before compiling them.

**3 · Create indexed test cases:**

```bash
qa-toolkit cases --answers qa-surface.json > INDEXED_TEST_PLAN.md
```

Or use `--json` to produce a machine-readable registry. Generated IDs are deterministic for each `method + path + story key` and every new case starts as `specified_unverified`.

**4 · Audit the tests that already exist:**

```bash
qa-toolkit audit --plan INDEXED_TEST_PLAN.md --tests tests/ --json
```

The audit finds potential matches in pytest/Vitest/Playwright test source files. A reference is marked `referenced_unverified`, not covered or passed. Assertion-level review and executed test evidence are separate stages.

> **Try the independent synthetic example:** [example API contract](examples/synthetic-api/CONTRACT.md), [OpenAPI file](examples/synthetic-api/openapi.json), [reviewed answers](examples/synthetic-api/answers.json). These are fictitious fixtures, not production data.

```bash
qa-toolkit surface --openapi examples/synthetic-api/openapi.json
qa-toolkit cases --answers examples/synthetic-api/answers.json
```

## ✦ How it works

The workflow is **endpoint-by-endpoint**, but not merely endpoint-by-endpoint testing. Resource *relationships*, *states*, and *actors* matter as much as HTTP routes.

| Step | Questions the agent answers | Output |
| --- | --- | --- |
| **Surface discovery** | What endpoints, verbs, parameters, responses and security declarations exist? | OpenAPI inventory |
| **Intended behavior** | What user/business capability should this operation provide? | Requirement-backed contract |
| **Allowed vs forbidden** | Who is permitted? Who must be denied, including anonymous and foreign owners? | Actor/access matrix |
| **Conditions & relationships** | Which resource IDs, ownership, tenant, parent/child relations and lifecycle states must hold? | Test-data dimensions |
| **Side effects & observability** | What changes or stays unchanged? How do we prove that from HTTP and persistent state? | Concrete assertion targets |
| **Stories & case IDs** | Which positive, forbidden, invalid, missing and transition scenarios expose a meaningful bug? | Stable indexed cases |
| **Audit & evidence** | Which existing tests actually assert these outcomes and which have run? | References now; verified execution planned |

### More than security testing

Test stories can target **authentication and authorization**, **input validation**, **business rules**, **resource isolation**, **information disclosure**, **pagination and filtering**, **async queues and timeouts**, **idempotency and retries**, **concurrency**, **data integrity**, **error contracts**, **rate limiting**, **exports**, **compatibility**, **accessibility** and **failure recovery**. Select applicable dimensions—not a mechanically generated Cartesian product of every possible input.

For example, a negative authorization story may require checking both the rejected status **and** that the response reveals nothing about a foreign record. For an asynchronous job, the required proof may include a real queued state followed by an eventual completion in a disposable environment. See the [complete methodology](docs/WORKFLOW.md).

## ✦ Agent setup

The skill supplies a reusable workflow for discovering contract gaps and writing meaningful, indexed test stories. It can work with any agent that supports the [Agent Skills standard](https://agentskills.io/specification).

**Install to supported coding agents:**

```bash
npx skills add darizae/qa-toolkit --skill evidence-driven-qa
```

Or install manually:

```bash
# Claude Code — user-level
mkdir -p ~/.claude/skills/evidence-driven-qa
cp skills/evidence-driven-qa/SKILL.md ~/.claude/skills/evidence-driven-qa/

# Codex / cross-agent project-level
mkdir -p .agents/skills/evidence-driven-qa
cp skills/evidence-driven-qa/SKILL.md .agents/skills/evidence-driven-qa/
```

**Suggested first agent instruction:**

> Use the evidence-driven-qa skill. Discover the testable API surface, inspect the requirements for each endpoint, answer who is allowed or denied and under which conditions, then design positive/negative/edge test stories. Produce stable case IDs and audit existing tests. Call out any unresolved business rules; do not assume implementation behavior is the intended contract.

### Model and coding-agent ecosystem

The toolkit does not depend on a particular language model. Via compatible coding agents or MCP-capable hosts, it is suitable for workflows using these common model families:

| Model family | Example agent/host |
| --- | --- |
| **OpenAI GPT models** (GPT-6, GPT-5 series, GPT-4o) | Codex and other MCP-aware clients |
| **Anthropic Claude** (Opus, Sonnet, Haiku) | Claude Code, Claude Desktop |
| **Google Gemini** (Pro, Flash) | Gemini CLI and compatible agent hosts |
| **Meta Llama, Qwen, Mistral, DeepSeek** | Local or hosted models through MCP-capable agent runtimes |
| **xAI Grok** | MCP-capable agent integrations |

**MCP integration is provided by the host or agent runtime, not by model weights themselves.** The generic skill can also be read as instructions by agents without MCP support.

## ✦ MCP server setup

The Python distribution also provides **`qa-toolkit-mcp`**, a local, read-only **stdio** server using the same core as the CLI. No hosted account, API key, or commercial license is required.

**Claude Code**

```bash
claude mcp add --transport stdio qa-toolkit -- \
  uvx --from evidence-driven-qa qa-toolkit-mcp --project /absolute/path/to/your/project
```

**Codex CLI**

```bash
codex mcp add qa-toolkit -- \
  uvx --from evidence-driven-qa qa-toolkit-mcp --project /absolute/path/to/your/project
```

**Generic MCP stdio client configuration** (replace the project path):

```json
{
  "mcpServers": {
    "qa-toolkit": {
      "command": "uvx",
      "args": [
        "--from", "evidence-driven-qa",
        "qa-toolkit-mcp",
        "--project", "/absolute/path/to/your/project"
      ]
    }
  }
}
```

The MCP server exposes four read-only tools:

| Tool | Purpose |
| --- | --- |
| `qa_capabilities` | List operations and current evidence limits |
| `qa_discover_api_surface` | Load a local OpenAPI JSON file and return the questionnaire |
| `qa_compile_indexed_cases` | Compile reviewed answers into indexed case records |
| `qa_audit_case_references` | Match case IDs against test-source references |

All paths are restricted to the selected project root. The MCP tools do not launch applications, run shell commands, modify files, access credentials, or connect to external services. The local stdio package is distinct from a hosted HTTPS ChatGPT app.

## ✦ Open-source by design

**MIT-licensed.** Free to use, study, modify, fork, redistribute and build upon—including commercial use under the terms of the license. The MCP server is part of the same open-source project; no subscription or paid account is needed.

**Contributions welcome:** bug reports, adapters, security improvements, documentation and reproducible examples. Open an [issue](https://github.com/darizae/qa-toolkit/issues) before substantial API or schema changes.

This is an early release of the **discovery and planning workflow**. Test generation into project-native source, controlled test execution, browser evidence ingestion and HTML reports are on the [roadmap](docs/ROADMAP.md). No current command claims to verify or certify test coverage.

## ✦ Documentation

| Document | Why it matters |
| --- | --- |
| [QA methodology](docs/WORKFLOW.md) | API questions, equivalence classes and story generation |
| [Product contract](docs/PRODUCT_SPEC.md) | Scope and architecture |
| [Case & evidence schema](docs/EVIDENCE_MODEL.md) | Traceability and status semantics |
| [Roadmap](docs/ROADMAP.md) | Features and GitHub issue tracking |
| [MCP distribution](docs/MCP_DISTRIBUTION.md) | Registry and free local server strategy |
| [Release checklist](docs/RELEASE_CHECKLIST.md) | Release hygiene |
| [Flowstead case study](examples/flowstead/README.md) | Private real-world validation plan |

Development:

```bash
python -m pip install -e '.[dev]'
python -m unittest discover -s tests -v
ruff check src tests
```

**Provenance:** All distributed code and examples in this repository were authored independently. The public package contains no reconstructed archived source, archived documentation, or private Flowstead fixtures.

---

<div align="center">

**Better questions → better test stories → better evidence.**

[GitHub](https://github.com/darizae/qa-toolkit) · [Issues](https://github.com/darizae/qa-toolkit/issues) · [MIT License](LICENSE)

</div>

<!-- mcp-name: io.github.darizae/evidence-driven-qa -->
