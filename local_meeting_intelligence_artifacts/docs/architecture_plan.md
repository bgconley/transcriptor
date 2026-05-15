# Architecture Plan — Local Evidence-Preserving Meeting Intelligence

## 1. Objective

The objective is to create a private local pipeline that turns permitted meeting recordings into an exhaustive technical/architectural report while preserving evidence, speaker attribution, and transcript fidelity.

This is not a summarizer. It is a local forensic analysis pipeline:
recording -> ASR -> diarization -> canonical transcript -> structured evidence extraction -> evidence validation -> 96GB synthesis -> independent validation -> final report.

Production posture:
- Treat this as a deterministic evidence pipeline with model-assisted stages, not as an agentic tool-using system.
- Every stage output must validate against a named schema before it is persisted or used by a downstream model.
- Unknown speaker ownership must remain unknown until corrected by transcript evidence or human review.
- Model recommendations are candidates until they pass the local runtime, schema, recall, grounding, and license gates.

## 2. Hardware Role Mapping

### 96GB GPU — Critical Thinker / Analysis Builder

Primary purpose:
- deep architectural synthesis
- section-by-section generation of the 19-section meeting report
- reconciliation of risks, constraints, requirements, implications, and open questions
- final reasoning across all structured evidence

Recommended primary model:
- Mistral Medium 3.5 128B, quantized

Recommended fallback:
- Mistral Small 4 119B NVFP4

Why:
- The 96GB card should not spend most of its time doing repetitive chunk extraction.
- It should receive curated evidence from the worker pipeline and perform the highest-value synthesis.
- It should not be asked to process the raw transcript in one giant pass as the main source of truth.

### 4000 GPU A — Comprehensive Fact Extractor

Primary purpose:
- run domain-specific extraction passes over transcript chunks
- emit strict JSON evidence records
- preserve exact quote, segment IDs, timestamps, speaker labels, and explicitness type
- run ASR/embedding/reranking jobs when idle

Recommended primary model:
- Qwen3.6-27B quantized

Secondary candidates:
- Qwen3.6-35B-A3B quantized
- Mistral Small 3.2 24B
- Gemma 4 26B-A4B

Why:
- The extractor must maximize recall, not prose quality.
- The model should work in short-to-medium windows with strict JSON schema validation.
- Domain-specific prompts improve recall more than a single broad prompt.

### 4000 GPU B — Independent Validator / Critic

Primary purpose:
- validate extracted evidence
- run missed-detail scans
- check final report sections against evidence
- find unsupported claims, mislabeled inferences, contradictions, and missing coverage
- optionally run alternate ASR/diarization verification

Recommended primary model:
- Gemma 4 31B IT NVFP4 if memory/context fit is acceptable
- Gemma 4 26B-A4B if 31B is not stable on a 20/24GB card

Secondary candidates:
- Mistral Small 3.2 24B
- Nemotron Super 49B only if TP-2 or 96GB availability allows it

Why:
- Different model-family validation reduces shared blind spots.
- The validator should not rewrite the report. It should audit the evidence relationship.

### TP-2 Across the 4000s

Default:
- Disabled.

Use TP-2 only when:
- Qwen3.6-27B or Gemma 4 31B cannot run with adequate context on one card.
- Higher precision or longer context materially improves extraction recall.
- The validator can be paused or moved temporarily.
- PCIe topology and runtime support are stable.

Do not use TP-2 merely because it is available. The pipeline benefits more from parallel extraction + validation than from a marginally larger single worker model unless benchmarks prove otherwise.

## 3. Pipeline

### Stage 0 — Ingest

Inputs:
- audio file
- meeting metadata
- participant list
- customer name
- known technical lexicon
- permission flag

Outputs:
- meeting.json
- participants.json
- known_terms.json
- recording hash

Quality gates:
- no missing file
- hash recorded
- meeting ID assigned
- no public egress

### Stage 1 — Audio Preprocessing

Tools:
- ffmpeg
- VAD
- optional denoise if benchmarked

Outputs:
- normalized 16 kHz mono diarization audio
- high-quality ASR audio
- audio-quality flags

Quality gates:
- original audio retained
- duration conserved
- preprocessing parameters logged

### Stage 2 — ASR

Primary:
- NVIDIA Parakeet, currently represented in the implementation config as nvidia/parakeet-tdt-0.6b-v3.

Fallback / alignment:
- Whisper large-v3 / large-v3-turbo
- WhisperX-style word-level alignment

Outputs:
- ASR candidate A
- ASR candidate B
- segment-level disagreements
- low-confidence terms

Quality gates:
- technical term error sampling
- numeric/IP/version/date check
- no silent omission of low-confidence regions

### Stage 3 — Diarization

Primary:
- pyannote Community-1

Optional:
- DiariZen for overlap-heavy calls

Outputs:
- RTTM
- exclusive speaker diarization if available
- speaker overlap flags
- speaker-review UI queue

Quality gates:
- speaker count sanity
- human review for important meetings
- customer/Nutanix attribution confidence

### Stage 4 — Canonical Transcript

Output must be JSONL.
Each JSONL row must validate against json_schemas/canonical_transcript_segment.schema.json.

Required fields:
- meeting_id
- segment_id
- start_time
- end_time
- speaker_label
- speaker_name
- speaker_org
- raw_text
- normalized_text
- asr_confidence
- diarization_confidence
- overlap
- technical_terms_detected
- correction_notes

The final analysis should cite segment IDs, not vague prose locations.

### Stage 5 — Domain Extraction

Run each chunk through narrow extractors:
- participant/speaker map
- business context
- customer environment
- current infrastructure
- workloads/applications
- networking
- storage/data
- security/compliance/governance
- operations/support
- migration
- DR/BC
- cost/commercial
- Nutanix/NC2/Azure guidance
- requirements/constraints/design drivers
- risks/gaps/open questions
- decisions
- action items

Each chunk-level extraction output must validate against json_schemas/chunk_extraction_result.schema.json. Each evidence item inside it must validate against json_schemas/evidence_item.schema.json.

### Stage 6 — Missed-Detail Scanner

The scanner receives:
- transcript chunk
- evidence extracted from that chunk

It answers:
- What relevant technical/architectural/operational/commercial/security/migration details in this chunk were missed?
- If none, it must return an empty evidence_items array and explain coverage confidence.

This pass is mandatory in the proposed production path, but the claim that it materially improves recall must be proven by the golden-set benchmark. If the scanner does not improve critical-fact recall enough to justify cost and false positives, keep it as a gated high-importance meeting pass instead of a universal pass.

### Stage 7 — Evidence Consolidation

Merge:
- duplicate facts
- repeated requirements
- synonymous product names
- repeated risks
- repeated open questions

Do not merge:
- contradictions
- low-confidence speaker attributions
- transcript facts with architectural implications
- risks with open questions unless both are preserved

Output must validate against json_schemas/evidence_merge_result.schema.json.

### Stage 8 — Retrieval

Store:
- transcript segments in Postgres
- evidence items in Postgres
- embeddings in Qdrant
- optional relationships in Neo4j

Use:
- Qwen3-Embedding-8B
- BGE reranker v2-M3

Retrieval is used for synthesis and validation, not as a substitute for exhaustive extraction.

### Stage 9 — 96GB Section Synthesis

Generate each report section independently.

Inputs:
- section-specific evidence
- retrieved transcript excerpts
- global speaker map
- requirements/risk/open-question/action tables
- report contract
- explicit instruction to preserve transcript-stated vs inferred vs implication distinctions

Output:
- section_draft.json validating against json_schemas/report_section.schema.json
- claim_map.json validating against json_schemas/claim_map.schema.json
- section_evidence_map.json

### Stage 10 — Independent Validation

Validator receives:
- section draft
- claim list
- evidence used by each claim
- raw transcript excerpts

Validator checks:
- unsupported claims
- overstatements
- missing evidence
- mislabeled inferences
- speaker attribution errors
- omitted critical facts
- contradictions
- section-specific coverage

The validator emits json_schemas/validation_result.schema.json only.

### Stage 11 — Repair and Final Assembly

Repair rules:
- remove unsupported claims
- downgrade transcript-stated claims to inference if needed
- add missing evidence
- add "not stated in transcript" where material facts are absent
- preserve unresolved open questions
- do not hide validation caveats

Final outputs:
- final_report.md
- evidence_appendix.json
- requirements_register.json
- risk_register.json
- open_questions.json
- action_items.json
- validation_results.json

## 4. Production Hardening Amendments

These amendments supersede looser wording elsewhere in this pack.

### Speaker Ownership

Do not default unknown speakers to customer. Unknown or generic speakers remain
`speaker_org: unknown`. If a claim assigns ownership of a requirement, risk,
decision, or action item and the speaker identity is low confidence, the item
must require human review before it can appear as a customer-owned or
Nutanix-owned final claim.

### Structured Output

All model stages emit strict JSON. Markdown report prose is embedded inside
`report_section.schema.json` and is not accepted as standalone builder output.
The orchestrator renders final Markdown only after schema validation and
validator approval.

### Runtime Proof

A model card is not proof of local fit. Before promotion from candidate to
approved, each model/runtime pair must record:
- exact model revision
- quantization source and hash manifest
- runtime version and CUDA/PyTorch variant
- max accepted context on the target GPU
- measured KV-cache capacity when available
- peak VRAM, latency, and tokens/sec
- first-pass schema-valid rate
- golden-set quality metrics

### Egress and Privacy

The no-egress claim is only valid after host-level verification. Docker
`internal: true` is useful but insufficient on its own. Production deployment
must include host firewall or network namespace egress denial, offline model
cache verification, and proof that pyannote/Hugging Face tokens are not needed
after model staging.

### Build Order

Build in this order:
1. Hardware inventory and runtime matrix.
2. Offline model registry and hash manifests.
3. ASR/diarization comparison and canonical transcript JSONL.
4. Schema harness for every model output.
5. Domain extractors plus missed-detail scanner.
6. Evidence consolidation and retrieval index.
7. Section builder and claim map.
8. Independent validator and repair loop.
9. Final assembler and benchmark report.
