# Changelog

## v0.2 - Implementation-Readiness Hardening

Added:
- agentic coder handoff brief
- ordered implementation backlog with acceptance commands
- testing strategy and review checklist
- executable pack validation script
- validation bootstrap dependencies
- handoff readiness assessment
- wrapper schemas for chunk extraction, missed-detail scanning, evidence merge, claim maps, and canonical transcript segments
- required coverage and claim-audit fields in validation results
- stricter report-section schema with integrity notes and required subsection coverage
- model registry template with revision, quantization, license, and hash placeholders
- runtime matrix for vLLM, SGLang, and GGUF/llama.cpp acceptance testing
- deterministic orchestrator state machine
- baseline Postgres schema
- 19-section report contract
- production readiness notes and build order
- valid JSON fixtures for schema harness development
- manifest documenting source-of-truth artifacts

Changed:
- claim schemas now enforce evidence IDs and segment IDs for claims unless explicitness is `not_stated`
- unknown/generic speakers now remain `speaker_org: unknown`; they no longer default to customer
- builder prompt always requires structured JSON output
- extractor, merger, scanner, and validator prompts now reference specific schemas
- benchmark manifest now includes ASR, diarization, repair-loop, and unknown-speaker gates
- Docker Compose skeleton now uses digest placeholders, secrets, health checks, and model registry mounts
- architecture plan now distinguishes candidate model-card evidence from local runtime proof

Not changed:
- workbook remains the v0.1 decision matrix and has not been edited
- model choices remain candidates until local benchmarks promote or reject them
