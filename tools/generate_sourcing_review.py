#!/usr/bin/env python3
import argparse
import csv
import re
from pathlib import Path

from urllib.parse import quote_plus


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a sourcing review CSV from a KiCad BOM export."
    )
    parser.add_argument(
        "input_csv",
        type=Path,
        help="Input BOM CSV path",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Output CSV path. Defaults to <input_dir>/sourcing_review.csv",
    )
    return parser.parse_args()


def count_refs(refs: str) -> int:
    return len([r.strip() for r in refs.split(",") if r.strip()])


def infer_package(footprint: str, package: str = "") -> str:
    text = f"{footprint} {package}"

    patterns = [
        ("0402", r"0402|1005Metric"),
        ("0603", r"0603|1608Metric"),
        ("0805", r"0805|2012Metric"),
        ("1206", r"1206|3216Metric"),
        ("1210", r"1210|3225Metric"),
        ("1812", r"1812"),
        ("2512", r"2512|6332Metric"),
        ("SMA", r"\bSMA\b|DO-214AC"),
        ("SOT-23-5", r"SOT-23-5"),
        ("TSOT-23", r"TSOT-23"),
        ("DFN-8", r"DFN-8"),
        ("USON-10", r"USON-10"),
        ("SOIC-8", r"SOIC|8-Pin SOIC"),
        ("VQFN-12", r"VQFN-12"),
        ("FC2QFN-17", r"FC2QFN-17"),
        ("Crystal 3225", r"3225|3\.2x2\.5"),
        ("JST SH 4-pin", r"BM04B-SRSS|JST SH"),
        ("M.2 2230", r"M\.2.*2230|M Key socket"),
        ("CM5 connector", r"Raspberry-Pi-5-Compute-Module|ComputeModule5"),
        ("microSD socket", r"SDCARD|503398"),
        ("battery holder", r"BatteryHolder|Keystone_3034"),
    ]

    for name, pat in patterns:
        if re.search(pat, text, re.I):
            return name

    return package or ""


def missing_info(row: dict, pkg: str) -> str:
    cls = row.get("Class", "").strip()
    value = row.get("Value", "").strip()
    voltage = row.get("Voltage", "").strip()
    tol = row.get("Tolerance", "").strip()
    mpn = row.get("MPN", "").strip()
    jlcpcb_pn = row.get("jlcpcb_pn", "").strip()

    missing = []

    if cls == "capacitor":
        if not mpn and not jlcpcb_pn:
            if not voltage and "1000uF" not in value:
                missing.append("voltage")
            if not re.search(r"C0G|NP0|X7R|X5R|Y5V", " ".join(str(v) for v in row.values()), re.I):
                missing.append("dielectric")

    elif cls == "resistor":
        if not tol and not mpn and value not in {"0Ω", "0R", "0"}:
            missing.append("tolerance")

    elif cls in {"inductor", "ferrite"}:
        missing.extend(["current_rating", "dcr/impedance"])

    elif cls == "fuse":
        missing.extend(["voltage_rating", "trip/blow_characteristic"])

    elif cls in {
        "diode",
        "tvs",
        "bridge_rectifier",
        "buck",
        "load_switch",
        "power_or",
        "mosfet",
        "current_sensor",
        "poe",
        "connector",
        "magjack",
        "crystal",
        "opto",
        "logic_ic",
        "esd_protection",
    }:
        if not mpn and not jlcpcb_pn:
            missing.append("mpn_or_jlcpcb_pn")

    if not pkg and not mpn and not jlcpcb_pn and cls not in {"mechanical", ""}:
        missing.append("package")

    return ", ".join(dict.fromkeys(missing))


def suggested_search(row: dict, pkg: str) -> str:
    cls = row.get("Class", "").strip()
    value = row.get("Value", "").strip()
    mpn = row.get("MPN", "").strip()
    voltage = row.get("Voltage", "").strip()
    tol = row.get("Tolerance", "").strip()
    desc = row.get("Description", "").strip()

    if mpn and cls not in {"resistor", "capacitor"}:
        return mpn

    if cls == "resistor":
        bits = [pkg, value, tol or "1%", "resistor"]
        return " ".join(b for b in bits if b)

    if cls == "capacitor":
        dielectric = ""
        joined = " ".join(str(v) for v in row.values())
        m = re.search(r"\b(C0G|NP0|X7R|X5R|Y5V)\b", joined, re.I)
        if m:
            dielectric = m.group(1).upper()

        bits = [pkg, value, voltage, tol, dielectric, "capacitor"]
        return " ".join(b for b in bits if b)

    if cls == "led":
        return f"{pkg} {value} LED".strip()

    if cls in {"diode", "tvs", "bridge_rectifier", "fuse", "ferrite", "inductor"}:
        return " ".join(b for b in [pkg, value, desc, cls] if b)

    return mpn or " ".join(b for b in [pkg, value, cls] if b)


def review_action(row: dict, missing: str) -> str:
    jlcpcb_pn = row.get("JLCPCB_PN", "").strip()
    critical = row.get("Critical", "").strip().lower()
    cls = row.get("Class", "").strip()

    if jlcpcb_pn:
        return "already_has_jlcpcb_pn_verify_specs"

    if missing:
        return "fill_missing_info"

    if critical == "no" and cls in {"resistor", "capacitor", "led"}:
        return "use_generic_jlcpcb_part"

    if critical == "no":
        return "find_close_jlcpcb_match"

    if critical == "review":
        return "find_exact_or_equivalent_review"

    if critical == "yes":
        return "exact_part_or_manual_review"

    return "manual_review_required"


def default_output_path(input_path: Path) -> Path:
    return input_path.parent / "sourcing_review.csv"


def main() -> None:
    args = parse_args()

    input_path = args.input_csv.expanduser()
    output_path = (
        args.output.expanduser()
        if args.output is not None
        else default_output_path(input_path)
    )

    if not input_path.exists():
        raise FileNotFoundError(f"Input CSV not found: {input_path}")

    with input_path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        original_fields = reader.fieldnames or []

        if "JLCPCB_Search_URL" in original_fields or "Suggested_JLCPCB_Search" in original_fields:
            raise ValueError("Input looks like a generated sourcing review CSV. Use the original KiCad BOM export instead.")

    added_fields = [
        "Qty",
        "Package_Inferred",
        "Missing_Info",
        "Suggested_JLCPCB_Search",
        "Search_URL",
        "Review_Action",
    ]

    out_fields = original_fields + [f for f in added_fields if f not in original_fields]

    out_rows = []
    for row in rows:
        pkg = infer_package(row.get("Footprint", ""), row.get("Package", ""))
        missing = missing_info(row, pkg)

        row["Qty"] = str(count_refs(row.get("Reference", "")))
        row["Package_Inferred"] = pkg
        row["Missing_Info"] = missing
        search = suggested_search(row, pkg)

        row["Suggested_JLCPCB_Search"] = search
        row["Search_URL"] = jlcpcb_search_url(search)
        row["Review_Action"] = review_action(row, missing)

        out_rows.append(row)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=out_fields)
        writer.writeheader()
        writer.writerows(out_rows)

    print(f"Wrote {output_path}")


def jlcpcb_search_url(query: str) -> str:
    return f"https://jlcpcb.com/parts/componentSearch?searchTxt={quote_plus(query)}"


if __name__ == "__main__":
    main()
