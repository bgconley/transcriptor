# Manifest v0.2

This manifest identifies the implementation source of truth for the local
meeting intelligence pack.

## Primary Source of Truth

- `README.md`: pack overview and hardening posture.
- `AGENT_HANDOFF.md`: implementation-agent start-here instructions.
- `docs/architecture_plan.md`: end-to-end pipeline architecture and production amendments.
- `docs/report_contract.md`: required 19-section final report contract.
- `docs/production_readiness.md`: readiness gates and remaining blockers.
- `docs/deployment_environment.md`: two-host deployment posture, eviction policy, ports, and preflight.
- `docs/model_fit_kernel_stress_plan.md`: first-gate model/runtime/kernel fit proof plan.
- `docs/implementation_build_order.md`: recommended engineering sequence.
- `docs/testing_strategy.md`: required test coverage and negative cases.
- `docs/agentic_coder_review_checklist.md`: per-slice review checklist.
- `docs/handoff_readiness_assessment.md`: direct handoff status, first actions, and production blockers.
- `tasks/implementation_backlog.yaml`: ordered agentic implementation slices and acceptance commands.
- `configs/pipeline_config.yaml`: active pipeline config and schema map.
- `configs/deployment_topology.yaml`: host roles, GPU eviction policy, and deployment preflight contract.
- `configs/model_fit_matrix.yaml`: candidate model/runtime/context/kernel stress matrix that must run before normal pipeline implementation.
- `configs/orchestrator_state_machine.yaml`: deterministic stage contract.
- `json_schemas/*.schema.json`: machine-readable output contracts.
- `prompts/*.txt`: model-stage prompts aligned to the schemas.

## Templates Requiring Local Pinning

- `configs/model_registry.template.yaml`: copy to `configs/model_registry.yaml` and pin exact model revisions, hashes, licenses, and local paths.
- `configs/runtime_matrix.yaml`: fill with measured runtime versions, context limits, KV-cache capacity, VRAM, and failure modes.
- `configs/docker_compose_skeleton.yml`: compose skeleton only; do not run without image digests, secrets, host firewall egress controls, and model registry.

## Implementation Support

- `configs/postgres_schema.sql`: baseline relational schema.
- `fixtures/*.valid.json`: positive fixtures for schema harness development.
- `scripts/validate_pack.py`: executable pack validation script.
- `requirements-validation.txt`: minimal Python dependencies for running the pack validation script.
- `configs/benchmark_manifest.yaml`: golden-set benchmark targets and pass/fail gates.
- `docs/model_evidence_register.md`: researched source register and candidate interpretation.

## Background Planning Artifact

- `local_meeting_intelligence_model_matrix.xlsx`: v0.1 decision matrix. Useful for review, but v0.2 docs/configs/schemas supersede it for implementation details.

## Do Not Treat As Production-Ready Until

- every model has a pinned revision and SHA256 manifest
- runtime matrix is filled from the target two-host GPU environment
- no-egress proof is captured
- the schema harness validates all stage outputs
- the golden set passes the production gates
- all 19 report sections and validators operate against real transcript evidence
