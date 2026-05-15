# Handoff Readiness Assessment

Status: ready for an agentic coder to implement and test the workflow.

Production status: not production-ready until the runtime, model registry,
license, no-egress, golden-set, and end-to-end report gates are proven on the
target two-host GPU environment.

## Why This Is Ready for Implementation Handoff

- The implementation entrypoint is explicit in `AGENT_HANDOFF.md`.
- Work is decomposed into ordered slices in `tasks/implementation_backlog.yaml`.
- Each slice has owner scope, inputs, outputs, acceptance commands, and pass
  criteria.
- Stage interfaces are expressed as JSON Schemas in `json_schemas/`.
- Positive fixtures exist for the core schemas.
- Generated negative checks reject missing evidence/coverage and unsupported
  claim publication.
- The report contract defines the required 19-section output shape.
- The model and runtime claims are marked as candidates until local proof is
  captured.
- The deployment topology is explicit for `10.25.0.50` and `10.25.0.51`,
  including authorized GPU model eviction and required preflight checks.
- The first implementation task is now model fit/kernel stress (`LMI-000`), so
  candidate model/runtime assumptions must be proven before pipeline stages are
  built.

## First Agent Actions

Run these commands from the artifact-pack root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-validation.txt
python scripts/validate_pack.py
```

Then implement `LMI-001` from `tasks/implementation_backlog.yaml` before any
model or runtime work. The schema harness is the safety rail for every later
stage.

## Handoff Boundaries

An implementation agent may:

- create the actual Python package/module structure
- add pytest coverage
- convert `scripts/validate_pack.py` into a package CLI
- create runtime probes and benchmark runners
- instantiate Postgres/Qdrant storage from the provided contracts
- copy `configs/model_registry.template.yaml` to a pinned local registry

An implementation agent must not:

- weaken schemas to pass invalid model output
- treat unknown speakers as customer-owned
- publish final claims without evidence IDs and transcript segment IDs
- treat candidate model cards as target-hardware proof
- claim production no-egress mode without host/network evidence
- skip the golden-set benchmark gate before production use

## Remaining Blockers Before Production

- Exact model revisions, licenses, local paths, and SHA256 hashes must be
  pinned in a real `configs/model_registry.yaml`.
- `configs/model_fit_matrix.yaml` must be executed and each candidate must be
  promoted or rejected from measured fit/kernel/context/stability evidence.
- Runtime matrix values must be measured on the target two-host GPU environment, including
  context length, KV-cache behavior, peak VRAM, latency, failure modes, driver
  version, CUDA version, and inference runtime version.
- The deployment preflight must be captured for each run because GPU residency
  and exposed model endpoints can drift.
- ASR and diarization quality must be benchmarked against representative
  meeting audio, including overlap and ambiguous ownership cases.
- Offline/no-egress mode must be proven outside the application layer.
- The golden-set benchmark must prove recall, attribution, claim support,
  validation blocking, and all 19 final report sections.
