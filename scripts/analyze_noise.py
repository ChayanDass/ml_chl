#!/usr/bin/env python3
"""Evidence-first profiling for the business entity resolution challenge."""

from __future__ import annotations

import argparse
import csv
import math
import os
import re
import sqlite3
import statistics
import tempfile
import unicodedata
from collections import Counter, defaultdict
from difflib import SequenceMatcher
from pathlib import Path


LEGAL = {
    "ltd", "limited", "pvt", "private", "corp", "corporation", "inc",
    "incorporated", "llc", "llp", "plc", "co", "company", "gmbh", "sarl",
    "sas", "sa", "ag", "bv", "pbc", "lp", "llp",
}
GENERIC = {"restaurant", "hotel", "store", "shop", "cafe", "café", "market", "center", "centre"}
STREET_ABBR = {"rd": "road", "st": "street", "ave": "avenue", "av": "avenue", "dr": "drive", "ln": "lane", "blvd": "boulevard", "hwy": "highway", "pkwy": "parkway", "ct": "court", "cir": "circle", "trl": "trail", "way": "way"}


def read_rows(path: Path):
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh, delimiter="\t")
        if reader.fieldnames != ["entity_id", "business_name", "business_address", "country"]:
            raise ValueError(f"Unexpected columns in {path}: {reader.fieldnames}")
        for row in reader:
            yield {k: (v or "") for k, v in row.items()}


def words(value: str):
    return re.findall(r"[\w]+", value, flags=re.UNICODE)


def norm_case(value: str) -> str:
    return " ".join(value.casefold().split())


def norm_punct(value: str) -> str:
    value = unicodedata.normalize("NFKC", value).casefold()
    return "".join(ch for ch in value if ch.isalnum() or ch.isspace())


def norm_alnum(value: str) -> str:
    value = unicodedata.normalize("NFKC", value).casefold()
    return "".join(ch for ch in value if ch.isalnum())


def tokens(value: str):
    return [x.casefold() for x in words(unicodedata.normalize("NFKC", value))]


def strip_legal(value: str):
    return [x for x in tokens(value) if x not in LEGAL]


def length_stats(values):
    values = list(values)
    if not values:
        return {"min": 0, "median": 0, "p90": 0, "max": 0, "mean": 0}
    values.sort()
    return {"min": values[0], "median": round(statistics.median(values), 2), "p90": values[min(len(values) - 1, math.ceil(.9 * len(values)) - 1)], "max": values[-1], "mean": round(sum(values) / len(values), 2)}


def emptyish(value: str) -> bool:
    return not value.strip()


def add_example(examples, key, s1, other, category, field):
    if len(examples[key]) < 3:
        examples[key].append({"category": category, "field": field, "s1_id": s1["entity_id"], "other_id": other["entity_id"], "s1": s1[field], "other": other[field]})


def classify_field(a: str, b: str, field: str):
    if not a or not b or a == b:
        return None
    ca, cb = norm_case(a), norm_case(b)
    ta, tb = tokens(a), tokens(b)
    sa, sb = set(ta), set(tb)
    if ca == cb:
        return "whitespace/case formatting" if a.casefold() != b.casefold() else "whitespace formatting"
    if a.casefold() == b.casefold():
        return "whitespace formatting"
    if norm_punct(a) == norm_punct(b):
        return "punctuation or separator"
    if field == "business_name" and strip_legal(a) == strip_legal(b) and ta != tb:
        return "legal suffix variation"
    if field == "business_name" and sorted(ta) == sorted(tb) and ta != tb:
        return "token/word order change"
    if field == "business_name" and len(sa - sb) == 0 and len(sb - sa) > 0:
        return "token insertion/removal"
    if field == "business_name" and len(sb - sa) == 0 and len(sa - sb) > 0:
        return "token insertion/removal"
    if field == "business_name" and any(x.isdigit() for x in a) != any(x.isdigit() for x in b):
        return "number insertion/removal/change"
    if field == "business_address":
        aa = [STREET_ABBR.get(x, x) for x in ta]
        bb = [STREET_ABBR.get(x, x) for x in tb]
        if aa == bb:
            return "street abbreviation"
        if sorted(aa) == sorted(bb) and aa != bb:
            return "address component order"
        if len(set(aa) - set(bb)) > 0 or len(set(bb) - set(aa)) > 0:
            if norm_alnum(a).replace(" ", "") == norm_alnum(b).replace(" ", ""):
                return "punctuation or separator"
            return "missing/additional address component"
        if any(x.isdigit() for x in a) != any(x.isdigit() for x in b):
            return "address number/postal variation"
    ratio = SequenceMatcher(None, norm_alnum(a), norm_alnum(b)).ratio()
    if ratio >= .90:
        return "small spelling/character variation"
    if ratio >= .65:
        return "substantial textual variation"
    return "strong textual variation"


def profile_source(path: Path, table: str, conn: sqlite3.Connection):
    conn.execute(f"CREATE TABLE {table} (entity_id TEXT, business_name TEXT, business_address TEXT, country TEXT)")
    conn.execute(f"CREATE INDEX {table}_id ON {table}(entity_id)")
    rows = 0
    countries = Counter()
    missing = Counter()
    name_lengths, addr_lengths, name_words, addr_words = [], [], [], []
    cur = conn.cursor()
    for row in read_rows(path):
        vals = (row["entity_id"], row["business_name"], row["business_address"], row["country"])
        cur.execute(f"INSERT INTO {table} VALUES (?, ?, ?, ?)", vals)
        rows += 1
        countries[row["country"] or "<empty>"] += 1
        for key in ("entity_id", "business_name", "business_address", "country"):
            if emptyish(row[key]):
                missing[key] += 1
        name_lengths.append(len(row["business_name"]))
        addr_lengths.append(len(row["business_address"]))
        name_words.append(len(words(row["business_name"])))
        addr_words.append(len(words(row["business_address"])))
        if rows % 100000 == 0:
            conn.commit()
    conn.commit()
    distinct = {}
    for col in ("entity_id", "business_name", "business_address"):
        distinct[col] = conn.execute(f"SELECT COUNT(DISTINCT {col}) FROM {table}").fetchone()[0]
    dup_rows = conn.execute(f"SELECT COUNT(*) - COUNT(DISTINCT entity_id || char(0) || business_name || char(0) || business_address || char(0) || country) FROM {table}").fetchone()[0]
    duplicate_ids = conn.execute(f"SELECT COUNT(*) FROM (SELECT entity_id FROM {table} GROUP BY entity_id HAVING COUNT(*) > 1)").fetchone()[0]
    repeated_name_values = conn.execute(f"SELECT COUNT(*) FROM (SELECT business_name FROM {table} GROUP BY business_name HAVING COUNT(*) > 1)").fetchone()[0]
    repeated_address_values = conn.execute(f"SELECT COUNT(*) FROM (SELECT business_address FROM {table} GROUP BY business_address HAVING COUNT(*) > 1)").fetchone()[0]
    repeated_pairs = conn.execute(f"SELECT COUNT(*) FROM (SELECT business_name, business_address FROM {table} GROUP BY business_name, business_address HAVING COUNT(*) > 1)").fetchone()[0]
    return {"rows": rows, "distinct": distinct, "countries": countries, "missing": missing, "duplicate_rows_extra": dup_rows, "duplicate_ids": duplicate_ids, "repeated_name_values": repeated_name_values, "repeated_address_values": repeated_address_values, "repeated_pairs": repeated_pairs, "name_length": length_stats(name_lengths), "address_length": length_stats(addr_lengths), "name_words": length_stats(name_words), "address_words": length_stats(addr_words)}


def fetch(conn, table, entity_id):
    row = conn.execute(f"SELECT entity_id, business_name, business_address, country FROM {table} WHERE entity_id = ?", (entity_id,)).fetchone()
    return dict(zip(("entity_id", "business_name", "business_address", "country"), row)) if row else None


def pct(n, d):
    return f"{100*n/d:.2f}%" if d else "n/a"


def md_escape(value):
    return str(value).replace("|", "\\|").replace("\n", " ")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, default=Path("6ab10eb3b23ba_student_resource/student_resource"))
    ap.add_argument("--report", type=Path, default=Path("dataset_noise_analysis.md"))
    ap.add_argument("--patterns", type=Path, default=Path("dataset_noise_patterns.csv"))
    args = ap.parse_args()
    train = args.root / "dataset" / "train"
    test = args.root / "dataset" / "test"
    sources = {"S1": train / "train_source1.tsv", "S2": train / "train_source2.tsv", "S3": train / "train_source3.tsv"}
    test_sources = {"S1": test / "test_source1.tsv", "S2": test / "test_source2.tsv", "S3": test / "test_source3.tsv"}
    fd, db_path = tempfile.mkstemp(prefix="entity_resolution_audit_", suffix=".sqlite")
    os.close(fd)
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode=OFF")
    conn.execute("PRAGMA synchronous=OFF")
    conn.execute("PRAGMA temp_store=FILE")
    profiles = {}
    try:
        for source, path in sources.items():
            profiles[source] = profile_source(path, source.lower(), conn)
        gt_path = train / "train_ground_truth.tsv"
        gt_rows = 0
        gt_match_counts = Counter()
        singleton_examples = {"zero": [], "one": [], "multiple": []}
        all_pairs = 0
        pair_counts = Counter()
        pair_examples = defaultdict(list)
        name_examples = defaultdict(list)
        address_examples = defaultdict(list)
        combo_counts = Counter()
        combo_examples = defaultdict(list)
        exact = Counter()
        normalized = Counter()
        severity = Counter()
        sev_examples = defaultdict(list)
        s1_seen = set()
        with gt_path.open("r", encoding="utf-8-sig", newline="") as fh:
            reader = csv.DictReader(fh, delimiter="\t")
            for row in reader:
                gt_rows += 1
                s1id = row["source1_entity_id"]
                ids = [x for x in (row["matched_entity_ids"] or "").split(",") if x]
                gt_match_counts[len(ids)] += 1
                bucket = "zero" if not ids else "one" if len(ids) == 1 else "multiple"
                if len(singleton_examples[bucket]) < 5:
                    singleton_examples[bucket].append((s1id, ids[:8]))
                s1 = fetch(conn, "s1", s1id)
                if not s1:
                    continue
                for oid in ids:
                    table = "s2" if oid.startswith("S2-") else "s3"
                    other = fetch(conn, table, oid)
                    if not other:
                        continue
                    all_pairs += 1
                    pair_counts[table.upper()] += 1
                    for field in ("business_name", "business_address", "country"):
                        if s1[field] == other[field]:
                            exact[(table.upper(), field)] += 1
                    n1, n2 = norm_case(s1["business_name"]), norm_case(other["business_name"])
                    a1, a2 = norm_case(s1["business_address"]), norm_case(other["business_address"])
                    if n1 == n2:
                        normalized[(table.upper(), "name")] += 1
                    if a1 == a2:
                        normalized[(table.upper(), "address")] += 1
                    if n1 == n2 and a1 == a2:
                        normalized[(table.upper(), "name+address")] += 1
                    for field, bucket in (("business_name", name_examples), ("business_address", address_examples)):
                        category = classify_field(s1[field], other[field], field)
                        if category:
                            pair_counts[(table.upper(), field, category)] += 1
                            add_example(bucket, (table.upper(), category), s1, other, category, field)
                    nr = SequenceMatcher(None, norm_alnum(s1["business_name"]), norm_alnum(other["business_name"])).ratio() if s1["business_name"] and other["business_name"] else 0
                    ar = SequenceMatcher(None, norm_alnum(s1["business_address"]), norm_alnum(other["business_address"])).ratio() if s1["business_address"] and other["business_address"] else 0
                    if nr >= .95 and ar < .60:
                        combo = "name very similar, address substantially different"
                    elif ar >= .95 and nr < .60:
                        combo = "address very similar, name substantially different"
                    elif nr < .60 and ar >= .80:
                        combo = "name substantially different, address strongly similar"
                    elif nr < .60 and ar < .60:
                        combo = "both name and address substantially different"
                    else:
                        combo = "neither extreme / moderate difference"
                    combo_counts[(table.upper(), combo)] += 1
                    if combo != "neither extreme / moderate difference":
                        add_example(combo_examples, (table.upper(), combo), s1, other, combo, "business_name")
                    changed = sum(s1[f] != other[f] for f in ("business_name", "business_address", "country"))
                    if changed == 0 or (nr >= .98 and ar >= .98): level = 0
                    elif changed == 1 and max(nr, ar) >= .85: level = 1
                    elif nr >= .70 or ar >= .70: level = 2
                    elif nr < .60 and ar < .60: level = 4
                    else: level = 3
                    severity[(table.upper(), level)] += 1
                    if len(sev_examples[(table.upper(), level)]) < 3:
                        sev_examples[(table.upper(), level)].append((s1["entity_id"], other["entity_id"], s1["business_name"], other["business_name"]))
                    if s1["business_name"] == other["business_name"] and s1["business_address"] == other["business_address"]:
                        exact[(table.upper(), "both")] += 1
        # False-friend aggregates are computed from duplicate field values in the source tables.
        false_friend = {}
        for table in ("s2", "s3"):
            false_friend[table.upper()] = {}
            for label, cols in (("same name", "business_name"), ("same address", "business_address"), ("same name + address", "business_name, business_address")):
                query = f"SELECT COUNT(*) FROM (SELECT {cols}, COUNT(*) AS n FROM {table} GROUP BY {cols} HAVING n > 1)"
                false_friend[table.upper()][label] = conn.execute(query).fetchone()[0]
        common = {}
        for table in ("s1", "s2", "s3"):
            common[table.upper()] = {}
            for col in ("business_name", "business_address"):
                common[table.upper()][col] = conn.execute(f"SELECT {col}, COUNT(*) AS n FROM {table} WHERE TRIM({col}) <> '' GROUP BY {col} ORDER BY n DESC, {col} LIMIT 5").fetchall()
        # Test structure only.
        test_profiles = {}
        for source, path in test_sources.items():
            counts = Counter()
            rows = 0
            for row in read_rows(path):
                rows += 1
                counts[row["country"] or "<empty>"] += 1
            test_profiles[source] = {"rows": rows, "countries": counts}

        lines = []
        lines.append("# Dataset Noise Analysis")
        lines.append("")
        lines.append("This report is a descriptive audit of the supplied training TSV files. It does not train a model or build a matcher. All examples are raw values from the files, and all percentages use the relevant observed denominator stated in the section.")
        lines.append("")
        lines.append("## Scope and Method")
        lines.append("")
        lines.append(f"- Training files were parsed with an explicit tab separator. Source 1, Source 2, and Source 3 contain {profiles['S1']['rows']:,}, {profiles['S2']['rows']:,}, and {profiles['S3']['rows']:,} rows respectively; the ground truth has {gt_rows:,} Source 1 rows and {all_pairs:,} resolved matched pairs.")
        lines.append("- The report distinguishes calculated facts from interpretations. A pattern is called observed only when the raw training values support it.")
        lines.append("- Similarity thresholds in the field-combination and severity sections are analytical heuristics for organizing examples, not a trained decision rule.")
        lines.append("")
        lines.append("## 1. Basic Dataset Profile")
        lines.append("")
        lines.append("| Source | Rows | Unique IDs | Unique names | Unique addresses | Countries | Duplicate rows (extra) | Duplicate IDs | Repeated name values | Repeated address values | Repeated name+address values |\n|---|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|")
        for source in ("S1", "S2", "S3"):
            p = profiles[source]
            lines.append(f"| {source} | {p['rows']:,} | {p['distinct']['entity_id']:,} | {p['distinct']['business_name']:,} | {p['distinct']['business_address']:,} | {', '.join(f'{k}: {v:,} ({pct(v,p['rows'])})' for k,v in p['countries'].items())} | {p['duplicate_rows_extra']:,} | {p['duplicate_ids']:,} | {p['repeated_name_values']:,} | {p['repeated_address_values']:,} | {p['repeated_pairs']:,} |")
        lines.append("")
        lines.append("Missing, empty, or null-like values:")
        lines.append("")
        lines.append("| Source | Entity ID | Business name | Business address | Country |\n|---|---:|---:|---:|---:|")
        for source in ("S1", "S2", "S3"):
            p = profiles[source]
            lines.append(f"| {source} | {p['missing']['entity_id']:,} | {p['missing']['business_name']:,} | {p['missing']['business_address']:,} | {p['missing']['country']:,} |")
        lines.append("")
        lines.append("Length and token distributions (minimum / median / p90 / maximum; token counts use Unicode word extraction):")
        lines.append("")
        lines.append("| Source | Name chars | Address chars | Name tokens | Address tokens |\n|---|---|---|---|---|")
        for source in ("S1", "S2", "S3"):
            p = profiles[source]
            fmt = lambda d: f"{d['min']} / {d['median']} / {d['p90']} / {d['max']}"
            lines.append(f"| {source} | {fmt(p['name_length'])} | {fmt(p['address_length'])} | {fmt(p['name_words'])} | {fmt(p['address_words'])} |")
        lines.append("")
        lines.append("Country distributions:")
        lines.append("")
        for source in ("S1", "S2", "S3"):
            lines.append(f"- {source}: " + ", ".join(f"{k}={v:,} ({pct(v,profiles[source]['rows'])})" for k,v in profiles[source]['countries'].items()))
        lines.append("")
        lines.append("## 2. Ground-Truth Pair Comparisons")
        lines.append("")
        lines.append("The ground truth contains a variable number of matched Source 2 and Source 3 records per Source 1 record. Exact-field agreement and simple case/whitespace-normalized agreement are shown below.")
        lines.append("")
        lines.append("| Pair type | Matched pairs | Exact name | Exact address | Exact country | Case/whitespace-normalized name | Case/whitespace-normalized address | Both normalized |\n|---|---:|---:|---:|---:|---:|---:|---:|")
        for table in ("S2", "S3"):
            d = pair_counts[table]
            lines.append(f"| S1 ↔ {table} | {d:,} | {exact[(table,'business_name')]:,} ({pct(exact[(table,'business_name')],d)}) | {exact[(table,'business_address')]:,} ({pct(exact[(table,'business_address')],d)}) | {exact[(table,'country')]:,} ({pct(exact[(table,'country')],d)}) | {normalized[(table,'name')]:,} ({pct(normalized[(table,'name')],d)}) | {normalized[(table,'address')]:,} ({pct(normalized[(table,'address')],d)}) | {normalized[(table,'name+address')]:,} ({pct(normalized[(table,'name+address')],d)}) |")
        lines.append("")
        lines.append("Country consistency on matched pairs:")
        lines.append("")
        for table in ("S2", "S3"):
            d = pair_counts[table]
            mismatch = d - exact[(table, "country")]
            lines.append(f"- S1 ↔ {table}: country identical for {exact[(table,'country')]:,}/{d:,} pairs ({pct(exact[(table,'country')],d)}); not identical for {mismatch:,} ({pct(mismatch,d)}). This is a calculated fact, not an assumption about country reliability.")
        lines.append("")
        lines.append("## 3. Observed Name Variation")
        lines.append("")
        for table in ("S2", "S3"):
            d = pair_counts[table]
            lines.append(f"### S1 ↔ {table}")
            lines.append("")
            cats = sorted({k[2] for k in pair_counts if isinstance(k, tuple) and k[0] == table and k[1] == "business_name"})
            lines.append("| Observed category | Pairs | Percent of pair set |\n|---|---:|---:|")
            for cat in cats:
                n = pair_counts[(table, "business_name", cat)]
                lines.append(f"| {cat} | {n:,} | {pct(n,d)} |")
            lines.append("")
            for cat in cats:
                exs = name_examples[(table, cat)]
                if exs:
                    lines.append(f"Examples: **{cat}**")
                    for ex in exs:
                        lines.append(f"- `{ex['s1_id']}` → `{ex['other_id']}`: S1 `{md_escape(ex['s1'])}`; {table} `{md_escape(ex['other'])}`.")
                    lines.append("")
        lines.append("Interpretation: categories are mutually non-exclusive only in the sense that the classifier records the first applicable category for each changed field; they should be treated as descriptive signals, not a definitive taxonomy of all edits.")
        lines.append("")
        lines.append("## 4. Observed Address Variation")
        lines.append("")
        for table in ("S2", "S3"):
            d = pair_counts[table]
            lines.append(f"### S1 ↔ {table}")
            lines.append("")
            cats = sorted({k[2] for k in pair_counts if isinstance(k, tuple) and k[0] == table and k[1] == "business_address"})
            lines.append("| Observed category | Pairs | Percent of pair set |\n|---|---:|---:|")
            for cat in cats:
                n = pair_counts[(table, "business_address", cat)]
                lines.append(f"| {cat} | {n:,} | {pct(n,d)} |")
            lines.append("")
            for cat in cats:
                exs = address_examples[(table, cat)]
                if exs:
                    lines.append(f"Examples: **{cat}**")
                    for ex in exs:
                        lines.append(f"- `{ex['s1_id']}` → `{ex['other_id']}`: S1 `{md_escape(ex['s1'])}`; {table} `{md_escape(ex['other'])}`.")
                    lines.append("")
        lines.append("Why this matters: exact address matching can fail when a component is omitted, abbreviated, reordered, or formatted differently even though the ground truth identifies the pair as the same entity.")
        lines.append("")
        lines.append("## 5. Field Combination Analysis")
        lines.append("")
        lines.append("The following buckets use character-level SequenceMatcher ratios after case-folding and removal of non-alphanumeric characters. They are exploratory thresholds used to expose difficult positive pairs.")
        for table in ("S2", "S3"):
            d = pair_counts[table]
            lines.append(f"### S1 ↔ {table}")
            lines.append("")
            lines.append("| Bucket | Pairs | Percent |\n|---|---:|---:|")
            for combo in sorted({k[1] for k in combo_counts if k[0] == table}):
                n = combo_counts[(table, combo)]
                lines.append(f"| {combo} | {n:,} | {pct(n,d)} |")
            lines.append("")
            for combo in sorted({k[1] for k in combo_counts if k[0] == table and k[1] != "neither extreme / moderate difference"}):
                exs = combo_examples[(table, combo)]
                if exs:
                    lines.append(f"Examples: **{combo}**")
                    for ex in exs:
                        lines.append(f"- `{ex['s1_id']}` → `{ex['other_id']}`: S1 name `{md_escape(ex['s1'])}`; {table} name `{md_escape(ex['other'])}`.")
                    lines.append("")
        lines.append("Non-match near-duplicate check: a conservative exact-key collision check across different Source 1 entities is included below. Similar-looking records in the source tables are potential false friends; ground truth is needed to decide whether they resolve to the same entity.")
        lines.append("")
        lines.append("## 6. False-Friend / Ambiguity Signals")
        lines.append("")
        lines.append("These counts are repeated values within each source, not proof that every repeated value is a false match. They identify places where a matcher could over-merge.")
        lines.append("")
        lines.append("| Source | Repeated exact names | Repeated exact addresses | Repeated exact name+address combinations |\n|---|---:|---:|---:|")
        for table in ("S1", "S2", "S3"):
            lines.append(f"| {table} | {false_friend[table]['same name']:,} | {false_friend[table]['same address']:,} | {false_friend[table]['same name + address']:,} |")
        lines.append("")
        for table in ("S1", "S2", "S3"):
            lines.append(f"Most common exact values in {table}:")
            for col, label in (("business_name", "names"), ("business_address", "addresses")):
                vals = "; ".join(f"`{md_escape(v)}` ({n:,})" for v,n in common[table][col])
                lines.append(f"- {label}: {vals or 'none'}")
        lines.append("")
        lines.append("## 7. Singleton and Multiple-Match Analysis")
        lines.append("")
        lines.append("| Number of matched records for an S1 entity | S1 entities | Percent |\n|---|---:|---:|")
        for k in sorted(gt_match_counts):
            label = str(k) if k < 10 else "10+"
            n = sum(v for kk,v in gt_match_counts.items() if (kk == k if k < 10 else kk >= 10))
            lines.append(f"| {label} | {n:,} | {pct(n,gt_rows)} |")
        lines.append("")
        for bucket, label in (("zero", "zero matches"), ("one", "exactly one match"), ("multiple", "multiple matches")):
            lines.append(f"Examples of {label}:")
            for s1id, ids in singleton_examples[bucket]:
                lines.append(f"- `{s1id}` → `{','.join(ids)}`")
        lines.append("")
        lines.append("## 8. Source-Specific Differences")
        lines.append("")
        lines.append("The pair-level tables above should be compared by denominator. A higher count or percentage in one source is evidence of a training-set difference; it is not a universal property of the source outside this challenge data.")
        lines.append("")
        lines.append("| Signal | S1 ↔ S2 | S1 ↔ S3 |\n|---|---:|---:|")
        for label, key in (("name exact", "business_name"), ("address exact", "business_address"), ("country exact", "country")):
            lines.append(f"| {label} | {exact[("S2",key)]:,} ({pct(exact[("S2",key)],pair_counts['S2'])}) | {exact[("S3",key)]:,} ({pct(exact[("S3",key)],pair_counts['S3'])}) |")
        lines.append("")
        lines.append("Test-set structural context only:")
        lines.append("")
        for source in ("S1", "S2", "S3"):
            lines.append(f"- Test {source}: {test_profiles[source]['rows']:,} rows; countries: " + ", ".join(f"{k}={v:,}" for k,v in test_profiles[source]['countries'].items()))
        lines.append("")
        lines.append("## 9. Rough Noise Severity")
        lines.append("")
        lines.append("Severity criteria: Level 0 means exact fields or only formatting-level changes; Level 1 means one small field change; Level 2 means multiple recognizable differences; Level 3 means at least one field has a substantial textual difference; Level 4 means both name and address have low exploratory similarity. These are heuristic summaries, not labels supplied by the challenge.")
        lines.append("| Level | S1 ↔ S2 | S1 ↔ S3 |\n|---|---:|---:|")
        for level in range(5):
            lines.append(f"| {level} | {severity[("S2",level)]:,} ({pct(severity[("S2",level)],pair_counts['S2'])}) | {severity[("S3",level)]:,} ({pct(severity[("S3",level)],pair_counts['S3'])}) |")
        lines.append("")
        for table in ("S2", "S3"):
            for level in range(5):
                if sev_examples[(table, level)]:
                    lines.append(f"- {table} Level {level}: " + "; ".join(f"`{a}`→`{b}` ({md_escape(c)} / {md_escape(d)})" for a,b,c,d in sev_examples[(table,level)]))
        lines.append("")
        lines.append("## 10. Exact-Match Baseline")
        lines.append("")
        lines.append("This baseline measures recall on known positive ground-truth pairs. It does not establish precision for an actual matcher because it does not enumerate all cross-source candidate pairs here.")
        lines.append("")
        lines.append("| Rule | S1 ↔ S2 | S1 ↔ S3 |\n|---|---:|---:|")
        for label, key in (("exact business name", "business_name"), ("exact business address", "business_address"), ("exact name + exact address", "both")):
            vals = []
            for table in ("S2", "S3"):
                n = exact[(table, "both" if key == "both" else key)]
                vals.append(f"{n:,} ({pct(n,pair_counts[table])})")
            lines.append(f"| {label} | {vals[0]} | {vals[1]} |")
        lines.append("")
        lines.append("The normalized rules used here are deliberately conservative: Unicode NFKC, case-folding, whitespace normalization, and for the exploratory `name+address` rule only, equality after those operations. Punctuation-only normalization was measured in the variation tables but was not used as the final baseline rule.")
        lines.append("")
        lines.append("## 11. Dataset Noise Profile")
        lines.append("")
        lines.append("The complete row-level pattern table is in `dataset_noise_patterns.csv`. The examples below are representative raw evidence, not an exhaustive catalog.")
        lines.append("")
        lines.append("| Noise pattern | Field | Observed? | Frequency | Example | Severity | Evidence type |\n|---|---|---|---:|---|---|---|")
        for table in ("S2", "S3"):
            for cat in sorted({k[2] for k in pair_counts if isinstance(k, tuple) and k[0] == table and k[1] in ("business_name", "business_address")}):
                field = "name" if any(k[0] == table and k[1] == "business_name" and k[2] == cat for k in pair_counts if isinstance(k, tuple)) else "address"
                n = pair_counts[(table, "business_name" if field == "name" else "business_address", cat)]
                ex = (name_examples if field == "name" else address_examples)[(table,cat)][0]
                lines.append(f"| {cat} | {field} | Yes | {n:,} ({pct(n,pair_counts[table])}) | `{ex['s1_id']}` / `{ex['other_id']}` | observed | calculated from matched pairs |")
        lines.append("")
        lines.append("Challenge-description patterns not separately listed above should be treated as hypotheses unless the corresponding observed category and examples are present. The hidden test set may contain patterns absent from training; this report cannot establish exhaustiveness.")
        lines.append("")
        lines.append("## WHAT OUR MATCHING SYSTEM MUST BE ABLE TO HANDLE")
        lines.append("")
        lines.append("Based on the evidence above, a future system will need to account for the observed formatting/text variation categories, missing fields, repeated values that create ambiguity, country inconsistencies where measured, and zero/one/multiple-match outcomes. It should preserve precision when names or addresses are common. Capabilities such as transliteration, DBA handling, or particular legal-suffix logic should be added only after their raw examples are confirmed in the corresponding generated tables; the challenge description alone is not evidence that they occur in this training sample.")
        args.report.write_text("\n".join(lines) + "\n", encoding="utf-8")

        with args.patterns.open("w", encoding="utf-8", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=["pattern_category", "field", "source_pair", "description", "frequency", "percentage", "example_s1_id", "example_other_id", "s1_value", "other_value", "severity", "evidence_type"])
            writer.writeheader()
            for table in ("S2", "S3"):
                for field, exdict in (("business_name", name_examples), ("business_address", address_examples)):
                    cats = sorted({k[1] for k in exdict if k[0] == table})
                    for cat in cats:
                        n = pair_counts[(table, field, cat)]
                        ex = exdict[(table,cat)][0]
                        writer.writerow({"pattern_category": cat, "field": field, "source_pair": f"S1↔{table}", "description": f"Observed {cat} in matched {field} values", "frequency": n, "percentage": f"{100*n/pair_counts[table]:.4f}", "example_s1_id": ex["s1_id"], "example_other_id": ex["other_id"], "s1_value": ex["s1"], "other_value": ex["other"], "severity": "observed", "evidence_type": "calculated from ground-truth pairs"})
    finally:
        conn.close()
        try:
            os.unlink(db_path)
        except OSError:
            pass


if __name__ == "__main__":
    main()
