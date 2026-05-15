# Agent Handoff

You are implementing the Local Meeting Intelligence workflow from this artifact
pack. Treat this directory as the product/spec input, not as generated notes.

## Start Here

1. Read `MANIFEST_v0.2.md`.
2. Read `docs/production_readiness.md`.
3. Read `docs/deployment_environment.md`.
4. Read `configs/deployment_topology.yaml`.
5. Read `docs/model_fit_kernel_stress_plan.md`.
6. Read `configs/model_fit_matrix.yaml`.
7. Read `tasks/implementation_backlog.yaml`.
8. Run `python scripts/validate_pack.py` from this directory.
9. Implement the backlog in order unless the user explicitly reorders it.

## Environment Bootstrap

From this directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-validation.txt
python scripts/validate_pack.py
```

The implementation project can later replace this bootstrap with its own
`pyproject.toml`, but it must preserve the same validation gates.

## Non-Negotiable Rules

- Do not default unknown speakers to customer.
- Do not let models choose tools or pipeline stages.
- Do not persist model output before schema validation.
- Do not publish a final report with any critical validation finding.
- Do not claim no-egress mode without host-level proof.
- Do not treat model-card context length as usable local context.
- Do not treat the workbook as the implementation source of truth; it is a
  v0.1 planning artifact.
- GPU model eviction is authorized for this workflow, but only for model/runtime
  containers occupying GPU memory. Preserve app stacks and data services unless
  the owner explicitly authorizes broader shutdown.
- Do not implement normal pipeline stages before `LMI-000` proves or rejects
  model fit, serving framework, kernel path, context, and unload behavior on the
  target hosts.

## Expected Implementation Shape

The implementation should be a deterministic Python workflow with narrowly
scoped services:

- `schema_harness`: local JSON Schema registry, JSON/JSONL validation, fixture
  checks, and negative fixture checks.
- `ingest`: meeting metadata, recording hashes, participant hints, known terms.
- `transcript`: ASR comparison, diarization, speaker review export, canonical
  transcript JSONL.
- `model_registry`: exact model revisions, local paths, license status, SHA256
  manifests, offline verification.
- `extraction`: chunking, domain extraction, missed-detail scans, retry/repair.
- `evidence`: consolidation, ambiguity tracking, Postgres persistence, Qdrant
  indexing.
- `reporting`: section synthesis, claim maps, validation, repair, final
  assembly.
- `benchmarks`: golden-set metrics and runtime matrix updates.

Keep modules small enough that each can be tested independently. The schemas in
`json_schemas/` are the API between stages.

## First Implementation Slice

Run `LMI-000` first. This is the model fit, serving framework, and kernel stress
gate. It must prove or reject the candidate model/runtime pairs in
`configs/model_fit_matrix.yaml` before extraction, reporting, or final assembly
implementation begins.

Only after `LMI-000` has produced `model_fit_results.json`,
`kernel_path_log_review.md`, and model-registry/runtime-matrix status patches
should the implementation move to the schema harness.

## First Coding Slice

Build the schema harness first. It should:

- load all schemas from `json_schemas/` into an offline registry
- validate every `fixtures/*.valid.json`
- validate every YAML config parses
- validate every JSON schema compiles
- fail if any `$ref` attempts a network fetch
- include at least one negative fixture or generated negative test per core
  schema

The pack already includes `scripts/validate_pack.py` as a reference check. A
real implementation can use it directly or replace it with a packaged CLI, but
it must preserve the same gates.

## Deployment Preflight

Before any model benchmark or end-to-end workflow run, write a
`deployment_preflight_report.json` that verifies both hosts from
`configs/deployment_topology.yaml`: SSH reachability, Docker model-container
state, restart policies, `nvidia-smi`, expected `/v1/models` responses, free
ports, and ZFS `tank` availability on `10.25.0.50`.

## Acceptance Evidence Format

Each completed slice should produce:

- commands run
- exit codes
- output artifact paths
- changed files
- known limitations
- next slice recommendation

Do not write "done" unless the acceptance command for the slice has passed in
the current run.

## Handoff Stop Points

Stop and ask for owner input if:

- model licenses are not acceptable for the intended use
- the target two-host environment cannot fit a recommended model at required context
- pyannote access cannot be staged offline
- ASR/diarization quality cannot meet speaker ownership gates
- a final report requires unsupported product capabilities to sound complete
