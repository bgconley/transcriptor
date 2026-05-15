# Model Fit and Kernel Stress Plan

Status: first implementation gate.

This plan must run before normal pipeline implementation. Only pack validation
and a minimal model-fit/preflight runner scaffold may be built before this gate
is executed. Do not implement extraction, reporting, or final assembly until
candidate models have been either promoted or rejected with target-host proof.

## Why This Is First

The pipeline depends on local model behavior that cannot be proven from model
cards. The riskiest assumptions are fit, kernel path, quantization behavior,
long-context stability, and structured-output reliability on the actual
Blackwell hosts.

The first work item is therefore `LMI-000` in
`tasks/implementation_backlog.yaml`.

## Source-Backed Runtime Caveats

The current vLLM docs say Blackwell deployments require CUDA 12.8 or newer
compatible binaries/containers. They also document ModelOpt FP4/NVFP4 handling
under `modelopt_fp4`; the ModelOpt NVFP4 checkpoint format is described as
experimental in the API docs. vLLM also has an NVFP4 Marlin kernel path used
when native FP4 compute is unavailable, which is a path we should reject unless
it was explicitly selected for a fallback experiment.

TensorRT-LLM documents NVFP4 KV cache as a ModelOpt offline-quantization path
and notes that FP8 weight/activation quantization is required when enabling the
NVFP4 KV cache flow.

Primary references:

- https://docs.vllm.ai/en/latest/getting_started/installation/gpu/
- https://docs.vllm.ai/en/latest/api/vllm/model_executor/layers/quantization/modelopt/
- https://docs.vllm.ai/en/latest/api/vllm/model_executor/kernels/linear/nvfp4/marlin/
- https://github.com/NVIDIA/TensorRT-LLM/blob/main/docs/source/features/quantization.md

## Required Proof

Each candidate model/runtime pair must produce:

- cold-load result
- warm-reload result
- `/v1/models` model identity
- exact model revision and local path
- Docker image digest or package versions
- CUDA, driver, PyTorch, vLLM/SGLang/TensorRT-LLM versions
- selected attention backend
- selected quantization/backend path
- selected MoE backend where applicable
- KV cache dtype and capacity
- target context and maximum context that actually fits
- peak VRAM and post-load headroom
- repeated request success rate
- unload cleanup result
- structured-output quality smoke for its role

No model can be marked `approved` in `configs/model_registry.yaml` until this
evidence exists.

## Candidate Order

1. `10.25.0.51` builder fallback: Mistral Small 4 119B NVFP4.
2. `10.25.0.51` builder primary: Mistral Medium 3.5 128B quantized.
3. `10.25.0.50` extractor: Qwen3.6-27B quantized.
4. `10.25.0.50` validator: Gemma 4 31B IT NVFP4.
5. `10.25.0.50` validator fallback: Gemma 4 26B-A4B or Mistral Small 3.2 24B.

The fallback builder is tested first because it is the most direct NVFP4
question for the 96GB card and may become the practical builder even if the
dense 128B candidate is higher quality.

As of the 20260515T063220Z staging/search pass, no official
`mistralai/Mistral-Medium-3.5-128B-NVFP4` artifact was found. The Medium
profile must therefore remain `pinned_quantization_required`; do not silently
replace it with a community NVFP4 conversion, and do not add custom NVFP4
quantization work unless a later plan explicitly scopes provenance, quality,
and runtime validation for that artifact.

## Stress Procedure

For each profile in `configs/model_fit_matrix.yaml`:

1. Run deployment preflight.
2. Evict GPU-resident model containers under the authorized policy.
3. Start the candidate service with pinned image/package versions.
4. Save full startup logs.
5. Parse logs for model architecture, quantization method, attention backend,
   MoE backend, KV cache dtype, KV cache size, context length, CUDA graph
   behavior, and warnings.
6. Call `/v1/models` and save the response.
7. Run one plain chat smoke.
8. Run one role-specific structured-output smoke.
9. Run context sweep requests at the configured token lengths.
10. Run 10 repeated requests.
11. For promotion candidates, run a 30-minute soak.
12. Stop the container and verify GPU memory returns to idle.

## Automatic Rejection Conditions

Reject the candidate if:

- the endpoint reports the wrong model id
- target context repeatedly fails
- logs show unsupported architecture errors
- logs show unintended Marlin/CPU/offload fallback
- kernel or attention backend errors repeat
- post-load VRAM headroom is below the role threshold
- unload leaves a GPU compute process or high-utilization zombie
- structured JSON valid rate is below the role threshold
- unknown speakers are promoted to customer in extractor/validator tests
- runtime downloads model files in offline mode

## Outputs

Write results under the run artifact root:

```text
runs/<timestamp>/deployment_preflight_report.json
runs/<timestamp>/model_fit_results.json
runs/<timestamp>/kernel_path_log_review.md
runs/<timestamp>/runtime_matrix_patch.yaml
runs/<timestamp>/model_registry_status_patch.yaml
runs/<timestamp>/rejected_candidates.json
```

The implementation agent should not manually edit approved model status from
memory. Promotion must be derived from these result files.
