# Implementation Build Order

This is the suggested engineering sequence for turning the pack into a working
system. Each slice should produce a runnable artifact and a small benchmark or
fixture before moving on.

## Slice 1: Validation Harness

Inputs:
- `json_schemas/*.schema.json`
- sample fixture JSON documents

Outputs:
- schema validator CLI
- fixture suite
- CI or local check command

Acceptance:
- every schema compiles
- valid fixtures pass
- intentionally bad fixtures fail

## Slice 2: Ingest and Canonical Transcript

Inputs:
- recording
- meeting metadata
- participant hints
- ASR and diarization outputs

Outputs:
- `meeting.json`
- `canonical_transcript.jsonl`
- `canonical_transcript.md`

Acceptance:
- every transcript row validates
- every segment has stable ID, timestamps, speaker label, text, and hash
- low-confidence ownership is flagged

## Slice 3: Model Registry and Runtime Loader

Inputs:
- `configs/model_registry.yaml`
- local model files

Outputs:
- model availability report
- hash verification report
- license status report

Acceptance:
- missing hashes block runtime startup
- unreviewed licenses block production mode
- offline mode starts without network download

## Slice 4: Extractors

Inputs:
- canonical transcript chunks
- prompts
- model endpoints

Outputs:
- `chunk_extraction_results.jsonl`
- `evidence_items.raw.jsonl`

Acceptance:
- every result validates
- quote match rate is measured
- schema repair retries are logged

## Slice 5: Missed-Detail and Merge

Inputs:
- transcript chunks
- raw evidence

Outputs:
- `missed_detail_results.jsonl`
- `evidence_merge_result.json`
- merged registers

Acceptance:
- no source segment IDs are lost
- contradictions become ambiguity records
- scanner recall lift is measured against gold

## Slice 6: Retrieval

Inputs:
- canonical transcript
- merged evidence

Outputs:
- Postgres rows
- Qdrant vectors
- retrieval benchmark report

Acceptance:
- seeded queries retrieve expected evidence
- reranker improves or is disabled with evidence

## Slice 7: Builder and Validator

Inputs:
- report contract
- evidence registers
- retrieved excerpts

Outputs:
- section JSON
- claim maps
- validation results

Acceptance:
- all sections validate
- all validation results include claim audit and coverage
- critical findings block final assembly

## Slice 8: Final Assembly

Inputs:
- validated sections
- evidence appendix
- registers
- validation results

Outputs:
- final report
- evidence appendix
- benchmark summary

Acceptance:
- all 19 sections present
- every cited evidence ID exists
- no critical validation findings remain
