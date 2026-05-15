# Testing Strategy

This document defines the minimum test coverage an agentic coder should create
while implementing the workflow.

## Test Pyramid

1. Schema and contract tests
   - Compile every JSON Schema.
   - Validate positive fixtures.
   - Validate negative cases for missing required fields, additional
     properties, invalid enum values, and unsupported claim publication.

2. Pure unit tests
   - Hashing and metadata creation.
   - Chunk boundary logic.
   - Quote matching.
   - Speaker ownership rules.
   - Evidence ID and claim ID generation.
   - Register generation.

3. Boundary tests
   - Model registry blocks unpinned or unlicensed models in production mode.
   - Runtime probes record measured facts instead of assumed context.
   - Deployment preflight rejects unexpected model residency, mismatched model
     IDs, missing ZFS storage, or occupied required ports.
   - Model responses with reasoning traces or malformed JSON are rejected.
   - Unknown speakers are never converted to customer by default.

4. Integration tests with fixtures
   - Canonical transcript fixture through extraction fixture.
   - Evidence merge fixture through report section fixture.
   - Report section fixture through validation fixture.

5. End-to-end tests
   - One short synthetic meeting with known facts.
   - One adversarial transcript with ambiguous speaker ownership.
   - One seeded unsupported final claim that must fail validation.

## Required Negative Tests

- evidence item missing `quote_match_status` fails.
- canonical transcript segment missing `speaker_confidence` fails.
- extraction, missed-detail, and evidence-merge wrappers with extra
  non-schema properties fail.
- report claim missing evidence IDs fails unless explicitness is `not_stated`.
- validation result with empty coverage object fails.
- unknown speaker ownership cannot be promoted to customer without human-review
  correction evidence.
- final assembly fails when any validation result has a critical finding.

## Required Test Commands

At minimum:

```bash
python -m pip install -r requirements-validation.txt
python scripts/validate_pack.py
pytest
```

If GPU/runtime tests are available:

```bash
pytest tests/test_runtime_probe.py -m gpu
pytest tests/test_end_to_end.py -m integration
```

## Evidence to Capture

Every benchmark or end-to-end run should write:

- command line
- git SHA or artifact pack version
- model registry revision
- runtime versions
- GPU inventory
- input meeting IDs
- output paths
- metrics
- pass/fail gate result
