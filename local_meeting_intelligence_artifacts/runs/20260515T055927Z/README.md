# Model Fit Gate Run 20260515T055927Z

Status: complete, no candidate promoted.

This run executed the `LMI-000` model-fit, serving-framework, kernel-path, and
unload gate against staged assets on the two GPU hosts.

## Summary

- `10.25.0.51` / blackbird was reachable and idle, but neither Mistral builder
  candidate from the matrix was staged. Both builder profiles are blocked before
  load testing.
- `10.25.0.50` loaded and served `sakamakismile/Qwen3.6-27B-NVFP4` as an
  observed extractor candidate. It used vLLM CUTLASS NVFP4 and FlashInfer, but
  is not promoted because context tops out at `18,816` tokens and VRAM headroom
  dropped below threshold.
- `10.25.0.50` loaded and served `nvidia/Gemma-4-26B-A4B-NVFP4` as an observed
  validator fallback. It used vLLM `modelopt_fp4`, forced `TRITON_ATTN`, and
  selected `VLLM_CUTLASS` for NVFP4 MoE, but is not promoted because headroom is
  too tight and repeat JSON validity was `9/10`.
- Both test containers were stopped and both GPUs returned to idle at `2 MiB`
  used with no compute apps.

## Primary Files

- `deployment_preflight_report.json`
- `model_fit_results.json`
- `kernel_path_log_review.md`
- `model_registry_status_patch.yaml`
- `runtime_matrix_patch.yaml`
- `rejected_candidates.json`
- `endpoint_sweeps/`
- `logs/`
- `unload_verification.log`
