# Production Readiness Notes

This pack is closer to implementation-ready after the v0.2 hardening pass, but
it is not production-ready until the gates below are satisfied on the real
workstation.

## Readiness Rating

- Architecture: strong.
- Model recommendations: plausible candidates, not final selections.
- Schemas and prompts: now buildable enough for a harness.
- Runtime plan: still requires local proof.
- Deployment plan: template only.

## Must-Pass Gates

1. Hardware Inventory
   - Confirm exact GPU names, VRAM, PCIe topology, driver, CUDA, and container
     runtime.
   - Record inventory in `hardware_inventory.yaml`.

2. Model Registry
   - Copy `configs/model_registry.template.yaml` to `configs/model_registry.yaml`.
   - Pin exact revisions, local paths, licenses, quantization sources, and
     SHA256 manifests.
   - Mark each model as `candidate`, `approved`, or `rejected`.

3. Runtime Matrix
   - Fill `configs/runtime_matrix.yaml` with exact vLLM, SGLang, and
     llama.cpp/GGUF versions tested.
   - Record max context, KV-cache capacity, VRAM, tokens/sec, and failure modes.

4. Schema Harness
   - Validate every JSONL row and every model response against the schema named
     in `configs/pipeline_config.yaml`.
   - Reject model responses with commentary, reasoning traces, missing wrapper
     fields, or unknown properties.
   - Load all local schemas into an offline registry before validation so
     `$ref` resolution never attempts a network fetch.

5. Golden Set
   - Annotate at least 5 meetings before selecting production models.
   - Include corrected speaker maps, technical terms, gold requirements, risks,
     open questions, decisions, action items, environment facts, and seeded bad
     claims.

6. ASR and Diarization Proof
   - Benchmark Parakeet against Whisper/WhisperX on the user's real meeting
     audio.
   - Measure technical term errors, numeric/IP/version/date errors, and
     speaker ownership reversals.

7. Claim Validation
   - The validator must catch seeded unsupported claims and omitted critical
     facts.
   - Empty coverage objects are invalid.
   - Any critical finding blocks final publication.

8. No-Egress Proof
   - Pre-stage all model files.
   - Start services with offline flags.
   - Verify DNS and outbound traffic are blocked at the host or network layer.
   - Confirm no runtime model download occurs.

9. Human Review Queue
   - Low-confidence speaker ownership, ambiguous customer/Nutanix attribution,
     and high-impact ASR disagreements must be routed to review before final
     assembly.

## Recommended Implementation Order

1. Implement schema validation utilities.
2. Implement canonical transcript JSONL and segment hashing.
3. Build the model registry loader and hash verifier.
4. Build ASR/diarization comparison and speaker-review export.
5. Build domain extraction with retry and repair.
6. Build missed-detail scanning and consolidation.
7. Build Postgres persistence and Qdrant indexing.
8. Build section synthesis and claim-map validation.
9. Build validation, repair, final assembly, and benchmark reporting.

## Remaining Risks

- 100B-class quantized builder quality on one 96GB card is unproven.
- 31B NVFP4 validator fit on a single 20/24GB 4000 is unproven.
- Qwen3.6 27B structured JSON reliability must be tested with thinking output
  disabled or stripped before validation.
- pyannote Community-1 has access/terms requirements and should be staged
  offline before no-egress mode.
- Docker Compose `internal: true` is not enough to prove no public egress.
- The workbook is a v0.1 planning matrix and should not be treated as the
  implementation source of truth.
