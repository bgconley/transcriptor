# Local Meeting Intelligence Artifact Pack

Pack status: v0.2 implementation-readiness hardening pass.

This pack is still not a drop-in production system. It is now closer to a
buildable implementation package: stage outputs have explicit schemas, runtime
and model registry templates are present, and production gates are called out.

Purpose: build a private, local, evidence-preserving meeting-analysis pipeline for corporate call recordings.

Core design:
- `10.25.0.50` / `620-01`: dual RTX PRO 4000 Blackwell host for control plane, ASR/diarization, extraction, validation, storage, and operator UI.
- `10.25.0.51` / `blackbird`: RTX PRO 6000 Blackwell Max-Q host for large-context builder/synthesis.
- CPU/control plane: deterministic orchestration, schema validation, evidence storage, retrieval, report assembly, audit logging, and cross-host preflight.

Primary model decision:
- 96GB builder candidate: Mistral Medium 3.5 128B, quantized.
- 96GB fallback/speed candidate: Mistral Small 4 119B NVFP4.
- 4000 extractor candidate: Qwen3.6-27B quantized.
- 4000 validator candidate: Gemma 4 31B IT NVFP4 if it fits, otherwise Gemma 4 26B-A4B or Mistral Small 3.2 24B.
- TP-2 across the 4000s is not the default. Use it only for targeted extraction benchmarks or if one-card model/context quality is inadequate.

Production hardening decisions added in v0.2:
- Unknown or generic speakers must remain `speaker_org: unknown`; they must not default to `customer`.
- Every model output has a wrapper schema, not just item-level schemas.
- Builder output is always structured JSON plus embedded Markdown; free-form Markdown is not an accepted production output.
- Every final claim requires evidence IDs and segment IDs, unless explicitly labeled `not_stated`.
- Model cards are evidence for candidacy, not proof of local fit. Exact quantization, runtime, context, latency, and license status must be pinned and benchmarked.
- The Docker Compose file is a skeleton with fail-closed placeholders; image digests, secrets, host firewall egress rules, and model hashes are required before use.
- Deployment is a two-host topology, not one three-GPU box. GPU model eviction
  is authorized, but non-model app/data services must be preserved unless
  explicitly authorized.

Included artifacts:
- MANIFEST_v0.2.md: source-of-truth map and template/readiness status.
- CHANGELOG.md: v0.2 hardening summary.
- AGENT_HANDOFF.md: start-here handoff brief for implementation agents.
- requirements-validation.txt: minimal dependencies for validating the pack
  before implementation scaffolding exists.
- local_meeting_intelligence_model_matrix.xlsx: role-by-role model matrix, evidence sources, benchmark rubric, and backlog.
- docs/architecture_plan.md: pipeline and hardware architecture.
- docs/model_evidence_register.md: researched evidence and interpretation by model/component.
- docs/report_contract.md: required 19-section output contract and evidence expectations.
- docs/production_readiness.md: build order, gates, and remaining production blockers.
- docs/deployment_environment.md: two-host deployment posture, eviction policy,
  ports, and required preflight.
- docs/testing_strategy.md: required unit, boundary, integration, and end-to-end tests.
- docs/agentic_coder_review_checklist.md: per-slice review checklist.
- docs/handoff_readiness_assessment.md: direct implementation-handoff status
  and remaining production blockers.
- configs/pipeline_config.yaml: candidate model/runtime/endpoint layout.
- configs/benchmark_manifest.yaml: golden transcript benchmark plan.
- configs/docker_compose_skeleton.yml: local service skeleton.
- configs/model_registry.template.yaml: offline model registry and license/hash template.
- configs/runtime_matrix.yaml: runtime acceptance matrix.
- configs/deployment_topology.yaml: host roles, eviction authorization,
  current timestamped GPU-free state, and deployment preflight requirements.
- configs/orchestrator_state_machine.yaml: deterministic stage/state contract.
- configs/postgres_schema.sql: baseline relational schema for transcript, evidence, reports, and validations.
- json_schemas/*.schema.json: evidence, report section, and validation result schemas.
- prompts/*.txt: extractor, merger, 96GB builder, and validator prompts.
- fixtures/*.valid.json: minimal positive fixtures for schema harness development.
- tasks/implementation_backlog.yaml: ordered implementation slices with acceptance commands.
- scripts/validate_pack.py: local pack/schema/config validation script.

Operational note:
The models should not choose tools. Python orchestration should call fixed extractors, validators, retrievers, and builders. Models emit structured records; the control plane validates, retries, stores, and assembles.

Workbook note:
The workbook remains the v0.1 decision matrix and source register. The v0.2
docs/configs/schemas in this directory supersede it for implementation detail.
