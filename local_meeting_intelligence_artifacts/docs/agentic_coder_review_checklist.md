# Agentic Coder Review Checklist

Use this before handing work back after each implementation slice.

## General

- The slice maps to one `tasks/implementation_backlog.yaml` ID.
- The implementation does not broaden scope beyond the slice.
- The slice has deterministic inputs and outputs.
- The acceptance command was run in the current session.
- The output artifacts are named and saved.

## Contracts

- All model outputs validate against a local schema.
- `$ref` resolution is offline only.
- JSONL files are validated row by row.
- Unknown properties are rejected where schemas set `additionalProperties: false`.
- The implementation does not silently coerce invalid model output into valid
  output without recording a repair.

## Speaker Ownership

- Unknown/generic speakers remain `unknown`.
- Low-confidence high-impact ownership requires human review.
- Customer/Nutanix/partner ownership is only assigned from transcript evidence
  or corrected speaker maps.

## Evidence Grounding

- Every final claim has evidence IDs and segment IDs, unless explicitly
  `not_stated`.
- Evidence quotes are exact or marked `normalized_match`/`unverified`.
- Contradictions are preserved as ambiguities.
- Source segment IDs survive merge and register generation.

## Runtime and Privacy

- Model revisions and hashes are pinned before production mode.
- Runtime context limits are measured on the real GPU.
- Offline mode does not perform runtime downloads.
- No-egress claims have host/network evidence, not just Docker config.

## Final Report

- All 19 sections exist.
- Every section has a validation result.
- No critical validation findings remain.
- Validation caveats are included rather than hidden.
