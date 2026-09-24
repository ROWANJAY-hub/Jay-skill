#!/usr/bin/env python3
"""Validate aggregate group and output counts for multi-group image requests."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from validate_plan import validate as validate_plan  # noqa: E402


def positive_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"invalid JSON in {path} at line {exc.lineno}, "
            f"column {exc.colno}: {exc.msg}"
        ) from exc
    if not isinstance(data, dict):
        raise ValueError(f"JSON root must be an object: {path}")
    return data


def validate(data: dict[str, Any], batch_path: Path) -> list[str]:
    errors: list[str] = []

    if data.get("batch_version") != 1:
        errors.append("batch_version must be 1")

    requested_groups = data.get("requested_group_count")
    if not positive_int(requested_groups):
        errors.append("requested_group_count must be a positive integer")

    requested_total = data.get("requested_total_outputs")
    if not positive_int(requested_total):
        errors.append("requested_total_outputs must be a positive integer")

    outputs_per_group = data.get("outputs_per_group")
    if outputs_per_group is not None and not positive_int(outputs_per_group):
        errors.append("outputs_per_group must be a positive integer when supplied")

    groups = data.get("groups")
    if not isinstance(groups, list) or not groups:
        errors.append("groups must be a non-empty array")
        return errors

    if positive_int(requested_groups) and len(groups) != requested_groups:
        errors.append(
            f"group count {len(groups)} != requested_group_count {requested_groups}"
        )

    seen_group_ids: set[str] = set()
    total_outputs = 0
    base_dir = batch_path.parent
    for index, group in enumerate(groups, start=1):
        prefix = f"groups[{index}]"
        if not isinstance(group, dict):
            errors.append(f"{prefix} must be an object")
            continue
        group_id = group.get("group_id")
        if not nonempty_string(group_id):
            errors.append(f"{prefix}.group_id must be a non-empty string")
            continue
        if group_id in seen_group_ids:
            errors.append(f"duplicate group_id: {group_id}")
        seen_group_ids.add(group_id)

        raw_plan_path = group.get("plan")
        if not nonempty_string(raw_plan_path):
            errors.append(f"{group_id}.plan must be a non-empty path")
            continue
        plan_path = Path(raw_plan_path)
        if not plan_path.is_absolute():
            plan_path = (base_dir / plan_path).resolve()

        try:
            plan = load_json(plan_path)
        except ValueError as exc:
            errors.append(f"{group_id}: {exc}")
            continue

        if plan.get("group_id") != group_id:
            errors.append(
                f"{group_id}: plan group_id {plan.get('group_id')!r} does not match"
            )

        plan_errors = validate_plan(plan)
        errors.extend(f"{group_id}: {error}" for error in plan_errors)

        plan_count = plan.get("requested_output_count")
        if positive_int(plan_count):
            total_outputs += plan_count
            if positive_int(outputs_per_group) and plan_count != outputs_per_group:
                errors.append(
                    f"{group_id}: requested_output_count {plan_count} "
                    f"!= outputs_per_group {outputs_per_group}"
                )

    if positive_int(requested_total) and total_outputs != requested_total:
        errors.append(
            f"aggregate output count {total_outputs} "
            f"!= requested_total_outputs {requested_total}"
        )

    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_batch.py /absolute/path/to/batch.json", file=sys.stderr)
        return 2
    batch_path = Path(sys.argv[1]).resolve()
    try:
        data = load_json(batch_path)
    except ValueError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1

    errors = validate(data, batch_path)
    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        "PASS: "
        f"groups={data['requested_group_count']} "
        f"total_outputs={data['requested_total_outputs']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
