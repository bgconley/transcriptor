# Model Evidence Register

This register summarizes the researched model/component evidence and how it maps to the local meeting-intelligence architecture.

## Hardware Evidence

### NVIDIA RTX PRO 6000 Blackwell
Evidence:
- NVIDIA lists the RTX PRO 6000 Blackwell Workstation Edition with 96GB of GPU memory.
- Source: https://www.nvidia.com/en-us/products/workstations/professional-desktop-gpus/rtx-pro-6000/

Interpretation:
- This card should be reserved for the largest local synthesis model.
- It is the only card in the proposed workstation that can plausibly host 100B-class quantized models with useful context.

### NVIDIA RTX PRO 4000 Blackwell
Evidence:
- NVIDIA lists the RTX PRO 4000 Blackwell with 24GB of GDDR7 GPU memory.
- Source: https://www.nvidia.com/en-us/products/workstations/professional-desktop-gpus/rtx-pro-4000/

Interpretation:
- If the two 4000s are Blackwell PRO 4000s, they are 24GB-class worker GPUs.
- They are well suited for quantized 24B-31B worker/validator models and ASR/embedding/rerank jobs.

### NVIDIA RTX 4000 Ada
Evidence:
- NVIDIA lists the RTX 4000 Ada Generation with 20GB GDDR6 memory.
- Source: https://www.nvidia.com/en-us/products/workstations/rtx-4000/

Interpretation:
- If the two 4000s are Ada generation, the worker/validator context limits are tighter.
- In that case, prefer lower quantization, smaller chunk windows, Gemma 4 26B-A4B, or Mistral Small 3.2.

### Blackwell Runtime
Evidence:
- vLLM documentation states that Blackwell GPUs require CUDA 12.8+ and that vLLM binaries are CUDA-version specific.
- Source: https://docs.vllm.ai/en/stable/getting_started/installation/gpu/

Interpretation:
- Runtime pinning is a first-class requirement.
- Do not mix arbitrary PyTorch/CUDA/vLLM versions.
- Treat vLLM/SGLang/llama.cpp as separately benchmarked runtime tracks.

## 96GB Builder Candidates

### Mistral Medium 3.5 128B
Evidence:
- Dense 128B model.
- 256k context length.
- Instruction-following, reasoning, and coding in one set of weights.
- Configurable reasoning effort.
- Strong system-prompt adherence and JSON/function capabilities.
- Modified MIT license with exceptions for companies with large revenue.
- Source: https://huggingface.co/mistralai/Mistral-Medium-3.5-128B

Interpretation:
- Best primary 96GB synthesis builder candidate.
- It should generate final report sections from curated evidence and retrieved transcript snippets.
- It should not be used as the high-throughput chunk extractor.
- Full precision does not fit a single 96GB GPU; use a high-quality quantized/NVFP4/GGUF/runtime-specific build and benchmark.

Risks:
- License must be reviewed.
- Quantization quality must be measured.
- Reported config issues affecting long context mean exact model/config version must be pinned.

### Mistral Small 4 119B NVFP4
Evidence:
- MoE with 128 experts and 4 active.
- 119B parameters with 6.5B active per token.
- 256k context length.
- NVFP4 checkpoint.
- Apache 2.0.
- Source: https://huggingface.co/mistralai/Mistral-Small-4-119B-2603
- Source: https://huggingface.co/mistralai/Mistral-Small-4-119B-2603-NVFP4

Interpretation:
- Best 96GB fallback/speed builder.
- Apache 2.0 is attractive for corporate/on-prem usage.
- MoE efficiency may make it a practical alternative to dense 128B.

Risks:
- MoE behavior must be benchmarked for deep technical synthesis and omission rate.
- It may be faster but less comprehensive than dense Mistral Medium 3.5.

### Command A 111B
Evidence:
- 111B parameters.
- 256K context.
- Enterprise-oriented open-weights research release.
- License: CC-BY-NC with acceptable use policy.
- Source: https://huggingface.co/CohereLabs/c4ai-command-a-03-2025

Interpretation:
- Interesting 100B-class benchmark candidate, but not a normal production choice for corporate work without legal clearance.

Risk:
- Non-commercial license is likely incompatible with work usage unless a separate license is obtained.

## 4000 Extractor Candidates

### Qwen3.6-27B
Evidence:
- Qwen card shows SGLang and vLLM recipes.
- Maximum context examples use 262,144 tokens with tensor parallel on 8 GPUs.
- Tool-call parser examples exist.
- Source: https://huggingface.co/Qwen/Qwen3.6-27B

Interpretation:
- Best first worker model for structured fact extraction.
- Use with 8K-32K transcript chunks on one 20/24GB card.
- Do not assume 262K practical context on a single 4000 GPU.
- Do not depend on native tool calling; use deterministic orchestration.

Risks:
- One-card quantization may affect JSON fidelity and extraction recall.
- Runtime support for the architecture must be tested on exact GPU/CUDA/framework combination.

### Qwen3.6-35B-A3B
Evidence:
- Qwen card shows maximum context examples at 262,144 tokens with tensor parallel on 8 GPUs.
- Qwen blog describes the model as 35B total / 3B active MoE.
- Source: https://huggingface.co/Qwen/Qwen3.6-35B-A3B
- Source: https://qwen.ai/blog?id=qwen3.6-35b-a3b

Interpretation:
- Worth testing as a speed-oriented extractor.
- May process repetitive chunk extraction efficiently if recall is strong.

Risks:
- Sparse/MoE low-active-parameter models can miss subtle details.
- Benchmark against Qwen3.6-27B before adopting.

### Mistral Small 3.2 24B
Evidence:
- 24B-class model with strong instruction/structured-output positioning.
- Source: https://huggingface.co/mistralai/Mistral-Small-3.2-24B-Instruct-2506

Interpretation:
- Safe fallback worker if Qwen3.6 runtime or quality is poor.
- Lower capability ceiling than Qwen3.6/Gemma4 but likely easier to run.

## Validator Candidates

### Gemma 4 31B IT NVFP4
Evidence:
- NVIDIA Gemma 4 31B IT NVFP4 card describes a 31B-class model with 256K-token context.
- It is ready for commercial/non-commercial use and references Apache 2.0 terms.
- Source: https://huggingface.co/nvidia/Gemma-4-31B-IT-NVFP4

Interpretation:
- Best independent validator if it fits on a 4000 with useful context.
- Different family from Qwen and Mistral reduces correlated blind spots.

Risks:
- 20GB Ada may not comfortably host it at useful context.
- 24GB Blackwell is more plausible, but benchmark actual VRAM and context.

### Gemma 4 26B-A4B
Evidence:
- Gemma 4 family includes 26B-A4B MoE with 25.2B total and 3.8B active parameters.
- Medium Gemma 4 models support 256K context.
- Source: https://huggingface.co/google/gemma-4-26B-A4B

Interpretation:
- Strong fallback validator for a single 4000.
- Lower active parameter count may be efficient enough for repeated validation passes.

### Nemotron Super 49B v1.5
Evidence:
- NVIDIA card describes it as a reasoning model post-trained for reasoning, RAG, and tool calling, with 128K context.
- Source: https://huggingface.co/nvidia/Llama-3_3-Nemotron-Super-49B-v1_5

Interpretation:
- Useful secondary validator/critic if TP-2 or 96GB time is available.
- Probably too large for routine one-card 4000 validation.

## Excluded / Deferred Models

### Kimi K2.6
Evidence:
- Kimi K2.6 is a very large MoE with 1T total parameters and 32B active parameters.
- Source: https://huggingface.co/moonshotai/Kimi-K2.6

Interpretation:
- Not practical for this local 96GB + 2x4000 architecture.

### Mistral Large 3 675B
Evidence:
- 675B-class model with 256k context.
- Source: https://huggingface.co/mistralai/Mistral-Large-3-675B-Instruct-2512

Interpretation:
- Too large for this local architecture.

### GLM-4.5 / GLM-4.5-Air
Evidence:
- GLM-4.5 family includes large MoE models; GLM-4.5-Air is 106B/12B-active.
- Source: https://huggingface.co/zai-org/GLM-4.5

Interpretation:
- Interesting but not a first candidate unless runtime/quantization proves easy on the 96GB card.

### GPT-OSS-120B
Evidence:
- User has direct local experience indicating Blackwell/kernel/extraction/tool-calling issues.

Interpretation:
- Exclude from recommended production path.

## ASR / Diarization / Retrieval

### NVIDIA Parakeet ASR
Evidence:
- NVIDIA Parakeet ASR collection describes strong ASR accuracy and efficient inference.
- Source: https://huggingface.co/collections/nvidia/parakeet-asr

Interpretation:
- Primary ASR candidate for English technical calls.

### WhisperX
Evidence:
- WhisperX provides fast ASR with word-level timestamps and speaker diarization.
- Source: https://github.com/m-bain/whisperx

Interpretation:
- Use for alignment and timestamp fidelity, even if Parakeet is primary ASR.

### pyannote Community-1
Evidence:
- pyannote Community-1 reports improvement over speaker-diarization-3.1 and provides exclusive speaker diarization output.
- Source: https://huggingface.co/pyannote/speaker-diarization-community-1

Interpretation:
- Primary diarization model.

### DiariZen
Evidence:
- DiariZen v2 supports overlap-heavy diarization, including up to four simultaneous speakers.
- Source: https://huggingface.co/BUT-FIT/diarizen-wavlm-large-s80-md-v2

Interpretation:
- Benchmark for overlap-heavy calls.

### Qwen3-Embedding-8B
Evidence:
- 8B embedding model, 32k context, up to 4096-dimensional embeddings, 100+ languages.
- Source: https://huggingface.co/Qwen/Qwen3-Embedding-8B

Interpretation:
- Strong evidence retrieval embedding candidate.

### BGE Reranker v2-M3
Evidence:
- Cross-encoder reranker directly scores query/passage similarity.
- Source: https://huggingface.co/BAAI/bge-reranker-v2-m3

Interpretation:
- Use after vector retrieval before builder/validator context assembly.

## Long Context Reliability

### Lost in the Middle
Evidence:
- The paper finds performance is often highest when relevant information appears at the beginning or end of context and degrades when information is in the middle.
- Source: https://arxiv.org/abs/2307.03172

### RULER
Evidence:
- RULER reports that models can perform well on simple needle-in-a-haystack but degrade as context length and task complexity increase.
- Source: https://arxiv.org/abs/2404.06654

Interpretation:
- Do not rely on raw long-context prompting.
- Use chunked extraction, evidence consolidation, retrieval, and validation.

## v0.2 Implementation Caveats

These caveats are binding for implementation until local benchmarks replace
them with measured facts.

### Candidate vs Approved Status

All model recommendations in this register are candidates. A model becomes
approved only after it has:
- a pinned model revision
- a pinned quantization source
- a model-file hash manifest
- a reviewed license status
- a runtime/load test on the target GPU
- a schema-valid output test
- golden-set quality metrics

### Context Claims

Advertised context length is not an operating context. The operating context is
the largest context that fits the target runtime/GPU with acceptable KV-cache
capacity, latency, stability, and quality. This is especially important for
Qwen3.6 and 100B-class Mistral candidates whose model cards include large
context examples on multi-GPU configurations.

### Structured JSON

Model-family claims about JSON or tool calling are not enough for this pipeline.
Each model must be tested against the local schemas in `json_schemas/` with the
exact prompts in `prompts/`. Thinking/reasoning traces must not appear in JSON
outputs.

### ASR and Diarization

NVIDIA Parakeet is represented in the hardened config by
`nvidia/parakeet-tdt-0.6b-v3`, but this is still a benchmark candidate rather
than a final production choice. It must be compared against Whisper large-v3 or
large-v3-turbo plus WhisperX-style alignment on real meeting audio.

pyannote Community-1 is a strong local diarization candidate, but access terms,
Hugging Face token authorization, and offline staging must be handled before
no-egress mode. If the official namespace is gated in the deployment
environment, record the authorized alternate namespace in the model registry.

### Hardware Fit

The RTX PRO 6000 Blackwell 96GB and RTX PRO 4000 Blackwell 24GB facts support
the proposed role split. They do not prove that Mistral Medium 3.5 128B,
Mistral Small 4 119B NVFP4, Qwen3.6 27B, or Gemma 4 31B NVFP4 will meet the
target context and latency on the exact workstation. The runtime matrix is the
source of truth after benchmarking.
