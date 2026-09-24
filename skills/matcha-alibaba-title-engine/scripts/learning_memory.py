#!/usr/bin/env python3
"""Validate and append immutable records to the matcha title learning memory."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SECTION_RULES = {
    "research_observations": (
        "evidence_id",
        {
            "evidence_id", "observed_at", "platform", "query", "product_sku",
            "category_route", "product_match", "phrases", "signal", "url",
            "limitation", "status",
        },
    ),
    "title_decisions": (
        "decision_id",
        {
            "decision_id", "decided_at", "product_sku", "category_route", "title",
            "primary_phrase", "secondary_phrases", "model_version", "evidence_ids",
            "status",
        },
    ),
    "learned_patterns": (
        "pattern_id",
        {
            "pattern_id", "synthesized_at", "category_route", "pattern", "direction",
            "confidence", "evidence_ids", "limitations", "status",
        },
    ),
    "model_reviews": (
        "review_id",
        {
            "review_id", "reviewed_at", "category_route", "old_version", "new_version",
            "decision", "weight_changes", "evidence_ids", "reason", "status",
        },
    ),
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def stable_id(prefix: str, payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(encoded.encode("utf-8")).hexdigest()[:12]
    return f"{prefix}-{digest}"


def atomic_write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def load_memory(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise ValueError(f"Learning memory not found: {path}")
    value = json.loads(path.read_text(encoding="utf-8"))
    validate_memory(value)
    return value


def validate_memory(value: dict[str, Any]) -> None:
    if not isinstance(value, dict) or value.get("schema_version") != 1:
        raise ValueError("Learning memory must be a schema_version 1 object")
    if not isinstance(value.get("linked_state"), dict):
        raise ValueError("linked_state must be an object")
    if not isinstance(value.get("baseline_evidence"), list):
        raise ValueError("baseline_evidence must be a list")

    baseline_ids = set()
    for record in value["baseline_evidence"]:
        evidence_id = record.get("evidence_id") if isinstance(record, dict) else None
        if not evidence_id or evidence_id in baseline_ids:
            raise ValueError("baseline_evidence contains a missing or duplicate evidence_id")
        baseline_ids.add(evidence_id)

    for section, (id_key, required) in SECTION_RULES.items():
        records = value.get(section)
        if not isinstance(records, list):
            raise ValueError(f"{section} must be a list")
        seen = set()
        for index, record in enumerate(records):
            if not isinstance(record, dict):
                raise ValueError(f"{section}[{index}] must be an object")
            missing = required.difference(record)
            if missing:
                raise ValueError(f"{section}[{index}] is missing: {sorted(missing)}")
            record_id = record[id_key]
            if not isinstance(record_id, str) or not record_id or record_id in seen:
                raise ValueError(f"{section} contains a missing or duplicate {id_key}")
            seen.add(record_id)
            for list_key in ("phrases", "secondary_phrases", "evidence_ids", "weight_changes"):
                if list_key in record and not isinstance(record[list_key], list):
                    raise ValueError(f"{section}[{index}].{list_key} must be a list")


def append_record(
    memory: dict[str, Any], section: str, id_key: str, record: dict[str, Any]
) -> str:
    for existing in memory[section]:
        if existing[id_key] != record[id_key]:
            continue
        if existing == record:
            return "duplicate"
        raise ValueError(f"Conflicting record ID: {record[id_key]}")
    memory[section].append(record)
    memory["updated_at"] = utc_now()
    return "appended"


def add_research_parser(subparsers: Any) -> None:
    parser = subparsers.add_parser("append-research", help="Append one dated marketplace observation")
    parser.add_argument("--evidence-id")
    parser.add_argument("--observed-at", required=True)
    parser.add_argument("--platform", required=True)
    parser.add_argument("--query", required=True)
    parser.add_argument("--product-sku", required=True)
    parser.add_argument("--category-route", required=True)
    parser.add_argument("--product-match", choices=("exact", "close", "partial"), required=True)
    parser.add_argument("--phrase", action="append", default=[])
    parser.add_argument("--signal", required=True)
    parser.add_argument("--url")
    parser.add_argument("--limitation", default="")


def add_decision_parser(subparsers: Any) -> None:
    parser = subparsers.add_parser("append-decision", help="Append one formal title decision")
    parser.add_argument("--decision-id")
    parser.add_argument("--decided-at", required=True)
    parser.add_argument("--product-sku", required=True)
    parser.add_argument("--category-route", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--primary-phrase", required=True)
    parser.add_argument("--secondary-phrase", action="append", default=[])
    parser.add_argument("--model-version", required=True)
    parser.add_argument("--evidence-id", action="append", required=True)


def add_pattern_parser(subparsers: Any) -> None:
    parser = subparsers.add_parser("append-pattern", help="Append a synthesized recurring pattern")
    parser.add_argument("--pattern-id")
    parser.add_argument("--synthesized-at", required=True)
    parser.add_argument("--category-route", required=True)
    parser.add_argument("--pattern", required=True)
    parser.add_argument("--direction", choices=("promote", "confirm", "demote", "mixed"), required=True)
    parser.add_argument("--confidence", choices=("directional", "eligible"), required=True)
    parser.add_argument("--evidence-id", action="append", required=True)
    parser.add_argument("--limitations", default="")


def add_review_parser(subparsers: Any) -> None:
    parser = subparsers.add_parser("append-review", help="Append a model or weight review")
    parser.add_argument("--review-id")
    parser.add_argument("--reviewed-at", required=True)
    parser.add_argument("--category-route", required=True)
    parser.add_argument("--old-version", required=True)
    parser.add_argument("--new-version", required=True)
    parser.add_argument("--decision", required=True)
    parser.add_argument("--weight-change", action="append", default=[])
    parser.add_argument("--evidence-id", action="append", required=True)
    parser.add_argument("--reason", required=True)
    parser.add_argument("--status", choices=("applied", "deferred", "no-change"), required=True)


def record_for(args: argparse.Namespace) -> tuple[str, str, dict[str, Any]]:
    if args.command == "append-research":
        record = {
            "observed_at": args.observed_at,
            "platform": args.platform,
            "query": args.query,
            "product_sku": args.product_sku,
            "category_route": args.category_route,
            "product_match": args.product_match,
            "phrases": args.phrase,
            "signal": args.signal,
            "url": args.url,
            "limitation": args.limitation,
            "status": "raw",
        }
        record["evidence_id"] = args.evidence_id or stable_id("research", record)
        return "research_observations", "evidence_id", record
    if args.command == "append-decision":
        record = {
            "decided_at": args.decided_at,
            "product_sku": args.product_sku,
            "category_route": args.category_route,
            "title": args.title,
            "primary_phrase": args.primary_phrase,
            "secondary_phrases": args.secondary_phrase,
            "model_version": args.model_version,
            "evidence_ids": args.evidence_id,
            "status": "active",
        }
        record["decision_id"] = args.decision_id or stable_id("decision", record)
        return "title_decisions", "decision_id", record
    if args.command == "append-pattern":
        record = {
            "synthesized_at": args.synthesized_at,
            "category_route": args.category_route,
            "pattern": args.pattern,
            "direction": args.direction,
            "confidence": args.confidence,
            "evidence_ids": args.evidence_id,
            "limitations": args.limitations,
            "status": "active",
        }
        record["pattern_id"] = args.pattern_id or stable_id("pattern", record)
        return "learned_patterns", "pattern_id", record
    if args.command == "append-review":
        record = {
            "reviewed_at": args.reviewed_at,
            "category_route": args.category_route,
            "old_version": args.old_version,
            "new_version": args.new_version,
            "decision": args.decision,
            "weight_changes": args.weight_change,
            "evidence_ids": args.evidence_id,
            "reason": args.reason,
            "status": args.status,
        }
        record["review_id"] = args.review_id or stable_id("review", record)
        return "model_reviews", "review_id", record
    raise ValueError(f"Unsupported append command: {args.command}")


def main() -> int:
    script_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--memory", type=Path, default=script_root / "assets" / "learning-memory.json"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("validate", help="Validate the knowledge-base schema and IDs")
    subparsers.add_parser("summary", help="Print record counts and current model state")
    add_research_parser(subparsers)
    add_decision_parser(subparsers)
    add_pattern_parser(subparsers)
    add_review_parser(subparsers)
    args = parser.parse_args()

    try:
        memory = load_memory(args.memory)
        if args.command == "validate":
            print(json.dumps({"status": "valid", "memory": str(args.memory)}, ensure_ascii=False, indent=2))
            return 0
        if args.command == "summary":
            result = {
                "memory": str(args.memory),
                "updated_at": memory.get("updated_at"),
                "learning_policy_version": memory["linked_state"].get("learning_policy_version"),
                "current_title_model_version": memory["linked_state"].get("current_title_model_version"),
                "counts": {
                    "baseline_evidence": len(memory["baseline_evidence"]),
                    **{section: len(memory[section]) for section in SECTION_RULES},
                },
            }
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 0

        section, id_key, record = record_for(args)
        status = append_record(memory, section, id_key, record)
        if args.command == "append-review" and args.status == "applied":
            if args.old_version == args.new_version:
                raise ValueError("An applied review must create a new model version")
            memory["linked_state"]["current_title_model_version"] = args.new_version
        validate_memory(memory)
        if status == "appended":
            atomic_write_json(args.memory, memory)
        print(json.dumps({"status": status, id_key: record[id_key]}, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False, indent=2))
        return 1


if __name__ == "__main__":
    sys.exit(main())
