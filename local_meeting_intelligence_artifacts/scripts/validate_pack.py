#!/usr/bin/env python3
"""Validate the Local Meeting Intelligence artifact pack.

This script is intentionally dependency-light but expects PyYAML and
jsonschema, which are common in the implementation environment. It performs
the same checks an implementation agent should preserve in its first slice.
"""

from __future__ import annotations

import json
import sys
import warnings
from pathlib import Path
from typing import Any

import yaml

warnings.filterwarnings("ignore", category=DeprecationWarning)

from jsonschema import Draft202012Validator, FormatChecker, RefResolver


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "json_schemas"
FIXTURE_DIR = ROOT / "fixtures"
CONFIG_DIR = ROOT / "configs"

FIXTURE_SCHEMA_MAP = {
    "canonical_transcript_segment.valid.json": "canonical_transcript_segment.schema.json",
    "evidence_item.valid.json": "evidence_item.schema.json",
    "chunk_extraction_result.valid.json": "chunk_extraction_result.schema.json",
    "missed_detail_result.valid.json": "missed_detail_result.schema.json",
    "evidence_merge_result.valid.json": "evidence_merge_result.schema.json",
    "claim_map.valid.json": "claim_map.schema.json",
    "report_section.valid.json": "report_section.schema.json",
    "validation_result.valid.json": "validation_result.schema.json",
}


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def build_schema_store(schemas: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    store: dict[str, dict[str, Any]] = {}
    for name, schema in schemas.items():
        store[name] = schema
        store[(SCHEMA_DIR / name).as_uri()] = schema
        if "$id" in schema:
            store[schema["$id"]] = schema
    return store


def validate_positive_fixtures(schemas: dict[str, dict[str, Any]]) -> None:
    store = build_schema_store(schemas)
    for fixture_name, schema_name in FIXTURE_SCHEMA_MAP.items():
        fixture_path = FIXTURE_DIR / fixture_name
        schema = schemas[schema_name]
        instance = load_json(fixture_path)
        resolver = RefResolver.from_schema(schema, store=store)
        validator = Draft202012Validator(
            schema,
            resolver=resolver,
            format_checker=FormatChecker(),
        )
        errors = sorted(validator.iter_errors(instance), key=lambda error: list(error.path))
        if errors:
            print(f"FAIL fixture {fixture_name} against {schema_name}")
            for error in errors:
                path = "/".join(str(part) for part in error.path) or "<root>"
                print(f"  {path}: {error.message}")
            raise SystemExit(1)
        print(f"OK fixture {fixture_name} -> {schema_name}")


def validate_negative_cases(schemas: dict[str, dict[str, Any]]) -> None:
    store = build_schema_store(schemas)
    cases: list[tuple[str, str, dict[str, Any]]] = []

    evidence = load_json(FIXTURE_DIR / "evidence_item.valid.json")
    evidence_missing_quote_status = dict(evidence)
    evidence_missing_quote_status.pop("quote_match_status")
    cases.append((
        "evidence_missing_quote_match_status",
        "evidence_item.schema.json",
        evidence_missing_quote_status,
    ))

    canonical = load_json(FIXTURE_DIR / "canonical_transcript_segment.valid.json")
    canonical_missing_speaker_confidence = dict(canonical)
    canonical_missing_speaker_confidence.pop("speaker_confidence")
    cases.append((
        "canonical_missing_speaker_confidence",
        "canonical_transcript_segment.schema.json",
        canonical_missing_speaker_confidence,
    ))

    chunk = load_json(FIXTURE_DIR / "chunk_extraction_result.valid.json")
    chunk_extra_property = dict(chunk)
    chunk_extra_property["unexpected_model_field"] = True
    cases.append((
        "chunk_extraction_extra_property",
        "chunk_extraction_result.schema.json",
        chunk_extra_property,
    ))

    missed_detail = load_json(FIXTURE_DIR / "missed_detail_result.valid.json")
    missed_detail_extra_property = dict(missed_detail)
    missed_detail_extra_property["unexpected_model_field"] = True
    cases.append((
        "missed_detail_extra_property",
        "missed_detail_result.schema.json",
        missed_detail_extra_property,
    ))

    evidence_merge = load_json(FIXTURE_DIR / "evidence_merge_result.valid.json")
    evidence_merge_extra_property = dict(evidence_merge)
    evidence_merge_extra_property["unexpected_model_field"] = True
    cases.append((
        "evidence_merge_extra_property",
        "evidence_merge_result.schema.json",
        evidence_merge_extra_property,
    ))

    validation = load_json(FIXTURE_DIR / "validation_result.valid.json")
    validation_empty_coverage = dict(validation)
    validation_empty_coverage["coverage"] = {}
    cases.append((
        "validation_empty_coverage",
        "validation_result.schema.json",
        validation_empty_coverage,
    ))

    section = load_json(FIXTURE_DIR / "report_section.valid.json")
    section_missing_evidence = json.loads(json.dumps(section))
    section_missing_evidence["claims"][0]["supporting_evidence_ids"] = []
    section_missing_evidence["claims"][0]["supporting_segment_ids"] = []
    cases.append((
        "section_claim_missing_evidence",
        "report_section.schema.json",
        section_missing_evidence,
    ))

    claim_map = load_json(FIXTURE_DIR / "claim_map.valid.json")
    claim_map_missing_evidence = json.loads(json.dumps(claim_map))
    claim_map_missing_evidence["claims"][0]["supporting_evidence_ids"] = []
    claim_map_missing_evidence["claims"][0]["supporting_segment_ids"] = []
    cases.append((
        "claim_map_claim_missing_evidence",
        "claim_map.schema.json",
        claim_map_missing_evidence,
    ))

    for case_name, schema_name, instance in cases:
        schema = schemas[schema_name]
        resolver = RefResolver.from_schema(schema, store=store)
        validator = Draft202012Validator(
            schema,
            resolver=resolver,
            format_checker=FormatChecker(),
        )
        errors = list(validator.iter_errors(instance))
        semantic_fail = case_name in {
            "section_claim_missing_evidence",
            "claim_map_claim_missing_evidence",
        } and not semantic_section_claim_check(instance)
        if not errors and not semantic_fail:
            print(f"FAIL negative case unexpectedly passed: {case_name}")
            raise SystemExit(1)
        if semantic_fail:
            print(f"OK negative semantic case rejected: {case_name}")
            continue
        print(f"OK negative case rejected: {case_name}")


def semantic_section_claim_check(section: dict[str, Any]) -> bool:
    """Return True when section claims satisfy evidence rules."""
    for claim in section.get("claims", []):
        if claim.get("explicitness") == "not_stated":
            continue
        if not claim.get("supporting_evidence_ids") or not claim.get("supporting_segment_ids"):
            return False
    return True


def validate_schema_references() -> None:
    missing = []
    pipeline = load_yaml(CONFIG_DIR / "pipeline_config.yaml")
    for key, rel_path in pipeline.get("schemas", {}).items():
        if not (ROOT / rel_path).exists():
            missing.append((key, rel_path))
    if missing:
        for key, rel_path in missing:
            print(f"FAIL missing schema reference {key}: {rel_path}")
        raise SystemExit(1)
    print(f"OK pipeline schema references: {len(pipeline.get('schemas', {}))}")

    missing_artifacts = []
    for key, rel_path in pipeline.get("artifact_paths", {}).items():
        if not (ROOT / rel_path).exists():
            missing_artifacts.append((key, rel_path))
    if missing_artifacts:
        for key, rel_path in missing_artifacts:
            print(f"FAIL missing artifact path {key}: {rel_path}")
        raise SystemExit(1)
    print(f"OK pipeline artifact paths: {len(pipeline.get('artifact_paths', {}))}")


def main() -> int:
    schemas = {path.name: load_json(path) for path in sorted(SCHEMA_DIR.glob("*.json"))}
    for name, schema in schemas.items():
        Draft202012Validator.check_schema(schema)
        print(f"OK schema {name}")

    for path in sorted(CONFIG_DIR.glob("*.yaml")) + sorted(CONFIG_DIR.glob("*.yml")):
        load_yaml(path)
        print(f"OK yaml {path.relative_to(ROOT)}")

    validate_schema_references()
    validate_positive_fixtures(schemas)
    validate_negative_cases(schemas)
    print("PACK VALIDATION PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
