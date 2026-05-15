# Mistral Builder Staging Run 20260515T063220Z

Status: Small NVFP4 staged; official Medium NVFP4 not found.

This run unblocked the first `10.25.0.51` builder fit target by staging the
vendor NVFP4 checkpoint for Mistral Small 4 119B.

## Mistral Small 4 119B NVFP4

- Host: `10.25.0.51` / `blackbird`
- Repo: `mistralai/Mistral-Small-4-119B-2603-NVFP4`
- Revision: `043f75a201a226d8e9cbbc3316af437ea25d3912`
- Local path:
  `/home/bgconley/models/local-meeting-intelligence/mistral-small-4-119b-nvfp4`
- Official repo files: `23`
- Official repo bytes: `70,846,520,016` (`65.98 GiB`)
- Repo-file SHA256 manifest:
  `/home/bgconley/models/local-meeting-intelligence/manifests/mistral-small-4-119b-nvfp4-043f75a201a226d8e9cbbc3316af437ea25d3912.repo-files.sha256`
- Local staging report:
  `/home/bgconley/models/local-meeting-intelligence/manifests/mistral-small-4-119b-nvfp4-043f75a201a226d8e9cbbc3316af437ea25d3912.staging.json`

The staged directory also contains `_hf_model_info.json`, a local metadata
sidecar captured during staging. It is intentionally excluded from the
repo-file SHA256 manifest.

## Mistral Medium NVFP4 Search

The official Hugging Face namespace check found no official
`mistralai/Mistral-Medium-3.5-128B-NVFP4` repo.

Official `mistralai` NVFP4 query results:

- `mistralai/Mistral-Small-4-119B-2603-NVFP4`
- `mistralai/Mistral-Large-3-675B-Instruct-2512-NVFP4`

Official `mistralai` Medium query results:

- `mistralai/Mistral-Medium-3.5-128B`
- `mistralai/Mistral-Medium-3.5-128B-EAGLE`

Community Medium NVFP4 conversions exist, but they are not official Mistral
artifacts and must not be silently substituted:

- `RecViking/Mistral-Medium-3.5-128B-NVFP4`
- `zdy1995love/Mistral-Medium-3.5-128B-NVFP4`
- `sakamakismile/Huihui-Mistral-Medium-3.5-128B-abliterated-NVFP4`

## Evidence Files

- `mistral-small-4-119b-nvfp4-043f75a201a226d8e9cbbc3316af437ea25d3912.staging.json`
- `manifests/mistral-small-4-119b-nvfp4-043f75a201a226d8e9cbbc3316af437ea25d3912.repo-files.sha256`
- `huggingface_mistral_medium_nvfp4_search.json`
- `firecrawl_mistral_medium_nvfp4_official_search.json`

## Next Action

Run the existing first builder fit profile:

`builder_fallback_mistral_small_4_119b_nvfp4_fit`

Do not implement normal extraction/reporting pipeline stages until this fit
profile either promotes or rejects the staged checkpoint with target-host
kernel, context, VRAM, structured-output, and unload evidence.
