# Kernel Path Log Review

Run: `20260515T055927Z`

## Builder Profiles

The two blackbird builder profiles were not load-tested because neither `mistralai/Mistral-Small-4-119B-2603-NVFP4` nor `mistralai/Mistral-Medium-3.5-128B` was staged on `10.25.0.51`. The host was reachable and the RTX PRO 6000 was idle.

## Qwen 27B NVFP4 Observed Extractor

- Observed model: `sakamakismile/Qwen3.6-27B-NVFP4`; matrix expected `Qwen/Qwen3.6-27B`.
- vLLM: `0.19.1rc1.dev29+g93726b2a1.d20260404` from `voipmonitor/vllm:cu130`.
- Architecture: `Qwen3_5ForConditionalGeneration`.
- Quantization: `compressed-tensors` with NVFP4-packed checkpoint config.
- NVFP4 GEMM: `NvFp4LinearBackend.VLLM_CUTLASS`.
- Attention: FlashInfer selected for language attention; FlashAttention logged for VIT/MM encoder attention.
- Linear attention: Triton/FLA GDN prefill kernel.
- KV cache dtype: `fp8`; GPU KV cache size: `18,816` tokens.
- Load memory: `17.62 GiB`; peak observed GPU memory during sweep: `23,711 MiB` used, `279 MiB` free.
- No Marlin fallback was observed.

Result: serving works with no-thinking prompt controls, but the candidate is **not promoted** because it does not satisfy the matrix identity, cannot reach 32K/65K context, and has less than the required headroom.

## Gemma 26B A4B NVFP4 Observed Validator Fallback

- Observed model: `nvidia/Gemma-4-26B-A4B-NVFP4`; matrix expected `google/gemma-4-26B-A4B`.
- vLLM: `0.20.2rc1.dev9+g01d4d1ad3` from `vllm-gemma4-pr40391:cu130`.
- Architecture: `Gemma4ForConditionalGeneration`.
- Quantization: `modelopt_fp4`; logs explicitly detected an experimental ModelOpt NVFP4 checkpoint.
- Attention: `TRITON_ATTN` forced because heterogeneous head dimensions would otherwise risk mixed-backend numerical divergence.
- NVFP4 MoE backend: `VLLM_CUTLASS`, selected from candidates including FlashInfer, Marlin, and emulation.
- KV cache dtype: `fp8`.
- Load memory: `16.83 GiB`; peak observed GPU memory during sweep: `23,330 MiB` used, `660 MiB` free.
- Warnings: uncalibrated FP8 KV scaling factors; `w1_weight_scale_2` mismatch warning; initial launch failed when Docker GPU device mapping was combined with inner `CUDA_VISIBLE_DEVICES=1`.

Result: serving works, but the candidate is **not promoted** because 32K prompt+output exceeds max by one token, observed headroom is below threshold, and repeat JSON validity was `9/10` due one fenced JSON response.

## Unload

Both test containers were stopped with restart policy `no`. After unload, both `.50` GPUs reported `2 MiB` used, `0%` utilization, and no compute apps.
