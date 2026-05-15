# Deployment Environment

This workflow is planned for two GPU hosts on the private LAN. Do not model it
as one local three-GPU workstation.

Last verified: `2026-05-15T05:41:43Z`.

## Hosts

`10.25.0.50` / `620-01` is the dual-RTX-PRO-4000 host. It should own the
control plane, canonical storage, ASR/diarization candidate services, chunk
extraction, independent validation, and operator UI. Its ZFS pool `tank` was
verified online with about `3.08T` free during the May 15, 2026 check.

`10.25.0.51` / `blackbird` is the RTX PRO 6000 Blackwell Max-Q host. It should
own large-context builder/synthesis work unless a local benchmark promotes a
different placement.

## Eviction Authorization

The owner has authorized eviction of present GPU-resident model workloads for
this deployment. Eviction is limited to model/runtime containers that occupy
GPU memory. Do not stop app stacks, databases, object stores, Open WebUI,
Parallax, Structura, Datum, or other non-model services unless the owner
explicitly authorizes that broader shutdown.

On May 15, 2026, the following model containers were stopped and left with
`restart=no`:

- `10.25.0.50`: `planner-sglang`, `reviewer-sglang`
- `10.25.0.51`: `qwen36-35b-a3b-bf16-server`

After eviction, all three GPUs reported no compute processes and `2 MiB` used
memory. Treat this as a timestamped fact, not a permanent state. Re-probe
before every run.

## Current Port Implications

Known service ports to preserve:

- `10.25.0.50:3000`: Open WebUI
- `10.25.0.50:8080`: agent orchestrator
- `127.0.0.1:18000` on `10.25.0.50`: Parallax API
- `127.0.0.1:8000` on `10.25.0.50`: Structura API
- `127.0.0.1:8001` on `10.25.0.50`: Datum API

Recommended meeting-intelligence ports:

- `10.25.0.50:18100`: ASR/diarization service
- `10.25.0.50:18120`: extractor service
- `10.25.0.50:18121`: validator service
- `10.25.0.50:18180`: orchestration API
- `10.25.0.51:18130`: large-context builder service

Do not assume historical Qwen `:18002` endpoints are live. Probe `/v1/models`
before calling any model endpoint.

## Required Deployment Preflight

Each workflow run must save a preflight report with:

- SSH reachability for both hosts
- Docker model container status and restart policies
- `nvidia-smi` memory/utilization/process output
- `/v1/models` responses for every expected model endpoint
- ZFS `tank` status on `10.25.0.50`
- port availability for the chosen service layout
- exact model revision/hash/license status from the model registry

The run must stop if the target GPUs are occupied by an unknown workload, if a
required model endpoint returns a different model id than expected, or if ZFS
canonical storage is not mounted.
