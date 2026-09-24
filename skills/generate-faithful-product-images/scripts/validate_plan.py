#!/usr/bin/env python3
"""Validate a reference-faithful ecommerce product-image plan."""

from __future__ import annotations

import json
import re
import sys
from itertools import combinations
from pathlib import Path
from typing import Any


VALID_TASK_MODES = {
    "carousel_set",
    "hero",
    "scene_only",
    "detail_only",
    "dimension_graphic",
    "sku_preview",
    "background_edit",
    "targeted_edit",
    "custom",
}
VALID_CLASSES = {"S", "C", "K", "D"}
VALID_CONFIDENCE = {"high", "medium", "low"}
VALID_RISK_LEVELS = {"low", "medium", "high"}
VALID_ROUTES = {
    "generative_reconstruction",
    "generative_edit",
    "intact_source_reuse",
    "retained_asset_composite",
    "deterministic_layout",
    "mixed",
}
VALID_FIDELITY = {"reference_faithful", "pixel_locked"}
VALID_SET_MODES = {
    "single_product",
    "heterogeneous_set",
    "bulk_multipack",
    "multi_sku_combined",
}
VALID_SKU_MODES = {"single_sku", "multi_sku_combined"}
VALID_QUANTITY_MODES = {"piece_sum", "hierarchical_pack"}
VALID_REPRESENTATIONS = {
    "exact_items",
    "exact_composite",
    "representative_stack",
    "carton_label",
    "not_applicable",
}
VALID_SLOT_KINDS = {
    "full_set",
    "hero",
    "detail",
    "scene",
    "dimension",
    "sku_preview",
    "background_edit",
    "targeted_edit",
    "custom",
}
VALID_FORMATS = {"png", "jpg", "jpeg", "webp", "tif", "tiff"}
IDENTITY_FIELDS = {
    "outline",
    "geometry",
    "material",
    "surface",
    "color",
    "orientation",
    "use",
}
PIXEL_CAPABILITIES = {
    "original_image_reuse",
    "cutout",
    "mask",
    "layered_composite",
}
COMPOSITE_ROUTES = {
    "intact_source_reuse",
    "retained_asset_composite",
    "deterministic_layout",
    "mixed",
}
SLOT_RE = re.compile(r"^P[1-9][0-9]*$")
RATIO_RE = re.compile(r"^\s*([0-9]+(?:\.[0-9]+)?)\s*:\s*([0-9]+(?:\.[0-9]+)?)\s*$")


def load_plan(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"plan file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}"
        ) from exc
    if not isinstance(data, dict):
        raise ValueError("plan root must be a JSON object")
    return data


def positive_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def string_list(value: Any) -> bool:
    return isinstance(value, list) and all(nonempty_string(item) for item in value)


def parse_ratio(value: Any) -> float | None:
    if not isinstance(value, str):
        return None
    match = RATIO_RE.fullmatch(value)
    if not match:
        return None
    left, right = float(match.group(1)), float(match.group(2))
    if left <= 0 or right <= 0:
        return None
    return left / right


def add_type_error(errors: list[str], value: Any, label: str) -> bool:
    if not isinstance(value, bool):
        errors.append(f"{label} must be true or false")
        return True
    return False


def validate(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    if data.get("plan_version") != 2:
        errors.append("plan_version must be 2")

    task_mode = data.get("task_mode")
    if task_mode not in VALID_TASK_MODES:
        errors.append("task_mode is missing or unsupported")

    platforms = data.get("platforms")
    if not string_list(platforms) or not platforms:
        errors.append("platforms must be a non-empty array of strings")

    if not nonempty_string(data.get("group_id")):
        errors.append("group_id must be a non-empty string")

    sku_mode = data.get("sku_mode")
    if sku_mode not in VALID_SKU_MODES:
        errors.append("sku_mode must be single_sku or multi_sku_combined")

    combined_requested = data.get("combined_sku_requested", False)
    if add_type_error(errors, combined_requested, "combined_sku_requested"):
        combined_requested = False

    set_mode = data.get("set_mode")
    if set_mode not in VALID_SET_MODES:
        errors.append("set_mode is missing or unsupported")

    declared = data.get("declared_count")
    if not positive_int(declared):
        errors.append("declared_count must be a positive integer")

    if not nonempty_string(data.get("count_basis")):
        errors.append("count_basis must identify what declared_count means")

    quantity_model = data.get("quantity_model")
    if not isinstance(quantity_model, dict):
        errors.append("quantity_model must be an object")
        quantity_model = {}
    quantity_mode = quantity_model.get("mode")
    if quantity_mode not in VALID_QUANTITY_MODES:
        errors.append("quantity_model.mode must be piece_sum or hierarchical_pack")
    representation = quantity_model.get("representation")
    if representation not in VALID_REPRESENTATIONS:
        errors.append("quantity_model.representation is missing or unsupported")
    if not nonempty_string(quantity_model.get("equation")):
        errors.append("quantity_model.equation must state the confirmed quantity equation")

    units_per_pack = quantity_model.get("units_per_pack")
    total_sales_units = quantity_model.get("total_sales_units")
    if quantity_mode == "hierarchical_pack":
        if not positive_int(units_per_pack):
            errors.append("hierarchical_pack requires positive units_per_pack")
        if not positive_int(total_sales_units):
            errors.append("hierarchical_pack requires positive total_sales_units")
        if (
            positive_int(declared)
            and positive_int(units_per_pack)
            and positive_int(total_sales_units)
            and declared * units_per_pack != total_sales_units
        ):
            errors.append(
                "hierarchical quantity failed: declared_count × units_per_pack "
                "!= total_sales_units"
            )

    if set_mode == "single_product":
        if declared != 1:
            errors.append("single_product requires declared_count = 1")
        if quantity_mode != "piece_sum":
            errors.append("single_product requires quantity_model.mode = piece_sum")
    if set_mode == "heterogeneous_set":
        if not positive_int(declared) or not 2 <= declared <= 11:
            errors.append("heterogeneous_set requires declared_count from 2 to 11")
        if quantity_mode != "piece_sum":
            errors.append("heterogeneous_set requires quantity_model.mode = piece_sum")
        if representation != "exact_items":
            errors.append("heterogeneous_set requires representation = exact_items")
    if set_mode == "multi_sku_combined" and sku_mode != "multi_sku_combined":
        errors.append("multi_sku_combined set_mode requires matching sku_mode")
    if sku_mode == "multi_sku_combined" and set_mode != "multi_sku_combined":
        errors.append("multi_sku_combined sku_mode requires matching set_mode")
    if sku_mode == "multi_sku_combined" and not combined_requested:
        errors.append("combined multi-SKU work requires explicit combined_sku_requested = true")
    if sku_mode == "single_sku" and combined_requested:
        errors.append("single_sku cannot set combined_sku_requested = true")

    requested = data.get("requested_output_count")
    if not positive_int(requested):
        errors.append("requested_output_count must be a positive integer")

    has_dimensions = data.get("has_dimensions")
    if add_type_error(errors, has_dimensions, "has_dimensions"):
        has_dimensions = False
    if has_dimensions and not nonempty_string(data.get("dimension_source")):
        errors.append("has_dimensions is true but dimension_source is missing")

    output_spec = data.get("output_spec")
    if not isinstance(output_spec, dict):
        errors.append("output_spec must be an object")
        output_spec = {}
    ratio_value = parse_ratio(output_spec.get("aspect_ratio"))
    if ratio_value is None:
        errors.append("output_spec.aspect_ratio must look like 1:1 or 4:5")

    target_width = output_spec.get("target_width")
    target_height = output_spec.get("target_height")
    if (target_width is None) != (target_height is None):
        errors.append("target_width and target_height must be supplied together")
    if target_width is not None and not positive_int(target_width):
        errors.append("output_spec.target_width must be a positive integer")
    if target_height is not None and not positive_int(target_height):
        errors.append("output_spec.target_height must be a positive integer")
    if (
        ratio_value is not None
        and positive_int(target_width)
        and positive_int(target_height)
        and abs((target_width / target_height) - ratio_value) > 0.005
    ):
        errors.append("target dimensions do not match output_spec.aspect_ratio")

    for key in ("min_width", "min_height", "max_bytes"):
        value = output_spec.get(key)
        if value is not None and not positive_int(value):
            errors.append(f"output_spec.{key} must be a positive integer")
    format_value = output_spec.get("format")
    if format_value is not None and (
        not isinstance(format_value, str)
        or format_value.lower().lstrip(".") not in VALID_FORMATS
    ):
        errors.append("output_spec.format is unsupported")

    fidelity = data.get("fidelity_mode")
    if fidelity not in VALID_FIDELITY:
        errors.append("fidelity_mode must be reference_faithful or pixel_locked")

    fragile_features = data.get("fragile_features", [])
    if not string_list(fragile_features):
        errors.append("fragile_features must be an array of non-empty strings")
        fragile_features = []

    requests_new_angle = data.get("requests_new_angle", False)
    if add_type_error(errors, requests_new_angle, "requests_new_angle"):
        requests_new_angle = False
    previous_drift = data.get("previous_identity_drift", False)
    if add_type_error(errors, previous_drift, "previous_identity_drift"):
        previous_drift = False

    override = data.get("user_slot_override", False)
    if add_type_error(errors, override, "user_slot_override"):
        override = False

    method = data.get("method")
    if not isinstance(method, dict):
        errors.append("method must be an object")
        method = {}
    risk_level = method.get("risk_level")
    if risk_level not in VALID_RISK_LEVELS:
        errors.append("method.risk_level must be low, medium, or high")
    triggers = method.get("automatic_triggers", [])
    if not string_list(triggers):
        errors.append("method.automatic_triggers must be an array of non-empty strings")
        triggers = []
    route = method.get("route")
    if route not in VALID_ROUTES:
        errors.append("method.route is missing or unsupported")
    capabilities = method.get("available_capabilities", [])
    if not string_list(capabilities):
        errors.append("method.available_capabilities must be an array of non-empty strings")
        capabilities = []
    capability_set = set(capabilities)

    claims_pixels = method.get("claims_pixel_preservation", False)
    if add_type_error(errors, claims_pixels, "method.claims_pixel_preservation"):
        claims_pixels = False
    original_reference_used = method.get("original_reference_used")
    if original_reference_used is not True:
        errors.append("method.original_reference_used must be true")
    full_visual_qa = method.get("full_visual_qa")
    if full_visual_qa is not True:
        errors.append("method.full_visual_qa must be true")

    if route == "generative_reconstruction" and "generative_image" not in capability_set:
        errors.append("generative_reconstruction route lacks generative_image capability")
    if route == "generative_edit" and "generative_edit" not in capability_set:
        errors.append("generative_edit route lacks generative_edit capability")
    if route == "intact_source_reuse" and "original_image_reuse" not in capability_set:
        errors.append("intact_source_reuse route lacks original_image_reuse capability")
    if route == "retained_asset_composite" and not (
        capability_set & {"cutout", "mask", "layered_composite"}
    ):
        errors.append("retained_asset_composite lacks cutout, mask, or layered_composite")
    if route == "deterministic_layout" and "deterministic_layout" not in capability_set:
        errors.append("deterministic_layout route lacks deterministic_layout capability")
    if route == "mixed" and len(capability_set) < 2:
        errors.append("mixed route requires at least two actually available capabilities")

    if claims_pixels:
        if fidelity != "pixel_locked":
            errors.append("a pixel-preservation claim requires fidelity_mode = pixel_locked")
        if not (capability_set & PIXEL_CAPABILITIES):
            errors.append("pixel preservation requires an actual preserving capability")
        if route in {"generative_reconstruction", "generative_edit"}:
            errors.append("a generative-only route cannot claim pixel preservation")
    if fidelity == "pixel_locked":
        if not (capability_set & PIXEL_CAPABILITIES):
            errors.append("pixel_locked fidelity requires source reuse, mask, cutout, or composite")
        if route in {"generative_reconstruction", "generative_edit"}:
            errors.append("pixel_locked fidelity cannot use a generative-only route")

    if has_dimensions and "deterministic_layout" not in capability_set:
        errors.append("reliable dimensions require deterministic_layout capability")
    if representation == "exact_composite" and not (
        capability_set & {"cutout", "mask", "layered_composite", "deterministic_layout"}
    ):
        errors.append("exact_composite representation lacks a deterministic composite capability")
    if representation in {"representative_stack", "carton_label"} and (
        "deterministic_layout" not in capability_set
    ):
        errors.append(f"{representation} requires deterministic_layout for exact quantity text")

    skus = data.get("skus")
    if not isinstance(skus, list) or not skus:
        errors.append("skus must be a non-empty array")
        skus = []
    sku_ids: set[str] = set()
    for index, sku in enumerate(skus, start=1):
        prefix = f"skus[{index}]"
        if not isinstance(sku, dict):
            errors.append(f"{prefix} must be an object")
            continue
        sku_id = sku.get("id")
        if not nonempty_string(sku_id):
            errors.append(f"{prefix}.id must be a non-empty string")
            continue
        if sku_id in sku_ids:
            errors.append(f"duplicate SKU id: {sku_id}")
        sku_ids.add(sku_id)
        if not nonempty_string(sku.get("reference")):
            errors.append(f"{sku_id}.reference must identify an original authority")
        if sku.get("confidence") not in VALID_CONFIDENCE:
            errors.append(f"{sku_id}.confidence must be high, medium, or low")
        if sku.get("confidence") == "low":
            errors.append(f"{sku_id} has low identity confidence; ask one blocking question")

    if sku_mode == "single_sku" and len(sku_ids) != 1:
        errors.append("single_sku mode requires exactly one SKU record")
    if sku_mode == "multi_sku_combined" and len(sku_ids) < 2:
        errors.append("multi_sku_combined mode requires at least two SKU records")

    items = data.get("items")
    if not isinstance(items, list) or not items:
        errors.append("items must be a non-empty array")
        items = []

    item_ids: set[str] = set()
    sales_ids: set[str] = set()
    represented_sku_ids: set[str] = set()
    sales_total = 0
    for index, item in enumerate(items, start=1):
        prefix = f"items[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{prefix} must be an object")
            continue
        item_id = item.get("id")
        if not nonempty_string(item_id):
            errors.append(f"{prefix}.id must be a non-empty string")
            continue
        if item_id in item_ids:
            errors.append(f"duplicate item id: {item_id}")
        item_ids.add(item_id)

        item_class = item.get("class")
        if item_class not in VALID_CLASSES:
            errors.append(f"{item_id}.class must be one of S, C, K, D")

        if not nonempty_string(item.get("name")):
            errors.append(f"{item_id}.name must be a non-empty string")

        quantity = item.get("quantity")
        if not positive_int(quantity):
            errors.append(f"{item_id}.quantity must be a positive integer")

        confidence = item.get("confidence")
        if confidence not in VALID_CONFIDENCE:
            errors.append(f"{item_id}.confidence must be high, medium, or low")
        if item.get("critical") is True and confidence == "low":
            errors.append(f"{item_id} is critical but low confidence; ask one blocking question")

        if item_class == "S":
            sales_ids.add(item_id)
            if positive_int(quantity):
                sales_total += quantity
            sku_id = item.get("sku_id")
            if sku_id not in sku_ids:
                errors.append(f"{item_id}.sku_id must reference a declared SKU")
            else:
                represented_sku_ids.add(sku_id)
            if not nonempty_string(item.get("reference")):
                errors.append(f"{item_id} is a sales item without an original reference")
            identity = item.get("identity")
            if not isinstance(identity, dict):
                errors.append(f"{item_id}.identity must be an object")
            else:
                for field in sorted(IDENTITY_FIELDS):
                    if not nonempty_string(identity.get(field)):
                        errors.append(f"{item_id}.identity.{field} must be recorded")
        if item_class in {"K", "C", "D"} and item.get("counts_toward_set") is True:
            errors.append(f"{item_id} counts toward the sale and must be classified as S")

    if quantity_mode == "piece_sum" and positive_int(declared) and sales_total != declared:
        errors.append(
            f"sales-item equation failed: S quantity sum {sales_total} "
            f"!= declared_count {declared}"
        )
    if (
        quantity_mode == "hierarchical_pack"
        and positive_int(total_sales_units)
        and sales_total != total_sales_units
    ):
        errors.append(
            f"hierarchical sales-item equation failed: S quantity sum {sales_total} "
            f"!= total_sales_units {total_sales_units}"
        )
    if set_mode == "heterogeneous_set" and len(sales_ids) < 2:
        errors.append("heterogeneous_set requires at least two distinct sales-item records")
    if sku_mode == "multi_sku_combined" and represented_sku_ids != sku_ids:
        errors.append("combined multi-SKU plan must contain a sales item for every SKU")

    slots = data.get("slots")
    if not isinstance(slots, list) or not slots:
        errors.append("slots must be a non-empty array")
        slots = []

    slot_map: dict[str, dict[str, Any]] = {}
    slot_product_ids: dict[str, set[str]] = {}
    scene_slots: list[dict[str, Any]] = []
    exact_content_present = False
    exact_quantity_text_present = False
    for index, slot in enumerate(slots, start=1):
        prefix = f"slots[{index}]"
        if not isinstance(slot, dict):
            errors.append(f"{prefix} must be an object")
            continue
        slot_id = slot.get("id")
        if not isinstance(slot_id, str) or not SLOT_RE.fullmatch(slot_id):
            errors.append(f"{prefix}.id must look like P1, P2, ...")
            continue
        if slot_id in slot_map:
            errors.append(f"duplicate slot id: {slot_id}")
        slot_map[slot_id] = slot

        kind = slot.get("kind")
        if kind not in VALID_SLOT_KINDS:
            errors.append(f"{slot_id}.kind is missing or unsupported")
        if not nonempty_string(slot.get("objective")):
            errors.append(f"{slot_id}.objective must be a non-empty string")

        product_ids = slot.get("product_ids")
        if not isinstance(product_ids, list):
            errors.append(f"{slot_id}.product_ids must be an array")
            product_ids = []
        valid_product_ids = [value for value in product_ids if nonempty_string(value)]
        slot_product_ids[slot_id] = set(valid_product_ids)
        if len(valid_product_ids) != len(product_ids):
            errors.append(f"{slot_id}.product_ids must contain only non-empty strings")
        if len(valid_product_ids) != len(set(valid_product_ids)):
            errors.append(f"{slot_id}.product_ids contains duplicates")
        unknown = set(valid_product_ids) - sales_ids
        if unknown:
            errors.append(
                f"{slot_id} references unknown or non-sales ids: "
                f"{', '.join(sorted(unknown))}"
            )

        if kind == "scene":
            axes = slot.get("scene_axes")
            if not isinstance(axes, dict):
                errors.append(f"{slot_id}.scene_axes must be an object")
            else:
                populated = {
                    key: str(value).strip()
                    for key, value in axes.items()
                    if nonempty_string(value)
                }
                if len(populated) < 4:
                    errors.append(f"{slot_id}.scene_axes must record at least four axes")
                slot["_validated_scene_axes"] = populated
            scene_slots.append(slot)

        requires_exact_text = slot.get("requires_exact_text", False)
        requires_exact_logo = slot.get("requires_exact_logo", False)
        if not isinstance(requires_exact_text, bool):
            errors.append(f"{slot_id}.requires_exact_text must be true or false")
            requires_exact_text = False
        if not isinstance(requires_exact_logo, bool):
            errors.append(f"{slot_id}.requires_exact_logo must be true or false")
            requires_exact_logo = False
        if kind == "dimension":
            if not has_dimensions:
                errors.append(f"{slot_id} is a dimension slot without reliable data")
            requires_exact_text = True
        if requires_exact_text:
            exact_content_present = True
            if not nonempty_string(slot.get("text_source")):
                errors.append(f"{slot_id} exact text requires text_source")
            if slot.get("layout_method") != "deterministic_layout":
                errors.append(f"{slot_id} exact content requires deterministic_layout")
            if "deterministic_layout" not in capability_set:
                errors.append(f"{slot_id} exact content lacks deterministic_layout capability")
            if kind == "sku_preview" or slot.get("text_role") == "quantity":
                exact_quantity_text_present = True
        if requires_exact_logo:
            exact_content_present = True
            if not nonempty_string(slot.get("logo_source")):
                errors.append(f"{slot_id} exact Logo requires logo_source")
            if slot.get("layout_method") != "deterministic_layout":
                errors.append(f"{slot_id} exact content requires deterministic_layout")
            if "deterministic_layout" not in capability_set:
                errors.append(f"{slot_id} exact content lacks deterministic_layout capability")

    if (
        representation in {"representative_stack", "carton_label"}
        and not exact_quantity_text_present
    ):
        errors.append(
            f"{representation} requires an output slot with exact deterministic quantity text"
        )

    for first, second in combinations(scene_slots, 2):
        first_axes = first.get("_validated_scene_axes", {})
        second_axes = second.get("_validated_scene_axes", {})
        keys = set(first_axes) | set(second_axes)
        differences = sum(first_axes.get(key) != second_axes.get(key) for key in keys)
        if differences < 3:
            errors.append(
                f"scene concepts {first.get('id')} and {second.get('id')} "
                "must differ on at least three recorded axes"
            )

    outputs = data.get("final_outputs")
    if not isinstance(outputs, list):
        errors.append("final_outputs must be an array")
        outputs = []
    valid_outputs = [
        value for value in outputs if isinstance(value, str) and SLOT_RE.fullmatch(value)
    ]
    if len(valid_outputs) != len(outputs):
        errors.append("final_outputs must contain only slot ids such as P1 or P2")
    if len(valid_outputs) != len(set(valid_outputs)):
        errors.append("final_outputs contains duplicate slot ids")
    unknown_outputs = set(valid_outputs) - set(slot_map)
    if unknown_outputs:
        errors.append(
            "final_outputs references unknown slots: " + ", ".join(sorted(unknown_outputs))
        )
    if positive_int(requested) and len(outputs) != requested:
        errors.append(
            f"final output count {len(outputs)} != requested_output_count {requested}"
        )

    if not override:
        expected = {f"P{i}" for i in range(1, 7)}
        if task_mode != "carousel_set":
            errors.append("the default six-slot contract requires task_mode = carousel_set")
        if requested != 6:
            errors.append(
                "default plan requires requested_output_count = 6 unless "
                "user_slot_override is true"
            )
        if set(slot_map) != expected:
            errors.append("default plan must contain exactly P1 through P6")
        if set(valid_outputs) != expected:
            errors.append("default final_outputs must contain exactly P1 through P6")
        for full_slot in ("P1", "P4"):
            slot = slot_map.get(full_slot)
            if slot:
                if slot.get("kind") != "full_set":
                    errors.append(f"{full_slot} must have kind full_set")
                if slot_product_ids.get(full_slot, set()) != sales_ids:
                    errors.append(f"{full_slot} must include every sales-item id")
        p5 = slot_map.get("P5")
        if p5 and p5.get("kind") != "scene":
            errors.append("P5 must have kind scene in the default plan")
        p6 = slot_map.get("P6")
        if p6:
            expected_kind = "dimension" if has_dimensions else "scene"
            if p6.get("kind") != expected_kind:
                errors.append(
                    f"P6 must have kind {expected_kind} for the current dimension state"
                )

    task_kind_rules = {
        "scene_only": {"scene"},
        "detail_only": {"detail"},
        "dimension_graphic": {"dimension"},
        "sku_preview": {"sku_preview"},
        "background_edit": {"background_edit"},
        "targeted_edit": {"targeted_edit"},
        "hero": {"hero", "full_set"},
    }
    if task_mode in task_kind_rules:
        allowed_kinds = task_kind_rules[task_mode]
        wrong_kinds = [
            slot_id
            for slot_id, slot in slot_map.items()
            if slot_id in valid_outputs and slot.get("kind") not in allowed_kinds
        ]
        if wrong_kinds:
            errors.append(
                f"task_mode {task_mode} has incompatible slots: "
                + ", ".join(sorted(wrong_kinds))
            )
    if task_mode == "dimension_graphic" and not has_dimensions:
        errors.append("dimension_graphic requires reliable dimensions")

    required_triggers: set[str] = set()
    if set_mode == "heterogeneous_set" and positive_int(declared) and declared >= 8:
        required_triggers.add("high_piece_count")
    if quantity_mode == "hierarchical_pack":
        required_triggers.add("hierarchical_pack")
    effective_total = total_sales_units if positive_int(total_sales_units) else declared
    if (
        set_mode == "bulk_multipack"
        and positive_int(effective_total)
        and effective_total > 11
        and representation in {"exact_items", "exact_composite"}
    ):
        required_triggers.add("high_exact_quantity")
    if sku_mode == "multi_sku_combined":
        required_triggers.add("multi_sku_combined")
    if task_mode in {"background_edit", "targeted_edit"}:
        required_triggers.add("targeted_edit")
    if fragile_features:
        required_triggers.add("fragile_identity")
    if requests_new_angle:
        required_triggers.add("new_angle")
    if previous_drift:
        required_triggers.add("previous_identity_drift")
    if fidelity == "pixel_locked":
        required_triggers.add("pixel_locked")
    if exact_content_present or has_dimensions:
        required_triggers.add("exact_content")

    missing_triggers = required_triggers - set(triggers)
    if missing_triggers:
        errors.append(
            "method.automatic_triggers is missing: "
            + ", ".join(sorted(missing_triggers))
        )
    if (triggers or required_triggers) and risk_level != "high":
        errors.append("automatic risk triggers require method.risk_level = high")

    composite_required = required_triggers & {
        "high_piece_count",
        "high_exact_quantity",
        "hierarchical_pack",
        "multi_sku_combined",
    }
    if composite_required and route not in COMPOSITE_ROUTES:
        errors.append(
            "high-count, hierarchical, or combined-SKU work requires source reuse, "
            "retained compositing, deterministic layout, or a mixed route"
        )

    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_plan.py /absolute/path/to/plan.json", file=sys.stderr)
        return 2
    try:
        data = load_plan(Path(sys.argv[1]))
    except ValueError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1

    errors = validate(data)
    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    sales_total = sum(
        item["quantity"] for item in data["items"] if item.get("class") == "S"
    )
    print(
        "PASS: "
        f"group={data['group_id']} "
        f"set_mode={data['set_mode']} "
        f"declared_count={data['declared_count']} "
        f"sales_total={sales_total} "
        f"slots={len(data['slots'])} "
        f"final_outputs={len(data['final_outputs'])}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
