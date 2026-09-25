#!/usr/bin/env python3
import json
import os
import subprocess

ROOT = '/home/vikaspal/Desktop/ml_chl/6ab10eb3b23ba_student_resource/student_resource'
DATASET = os.path.join(ROOT, 'dataset')
OUTDIR = '/home/vikaspal/Desktop/ml_chl/reports/dataset_analysis'
FILES = {
    'train_source1': os.path.join(DATASET, 'train', 'train_source1.tsv'),
    'train_source2': os.path.join(DATASET, 'train', 'train_source2.tsv'),
    'train_source3': os.path.join(DATASET, 'train', 'train_source3.tsv'),
    'train_ground_truth': os.path.join(DATASET, 'train', 'train_ground_truth.tsv'),
    'test_source1': os.path.join(DATASET, 'test', 'test_source1.tsv'),
    'test_source2': os.path.join(DATASET, 'test', 'test_source2.tsv'),
    'test_source3': os.path.join(DATASET, 'test', 'test_source3.tsv'),
}


def run_shell(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=False)
    return result.stdout.strip()


def file_stats(path):
    out = run_shell(f"wc -l '{path}'")
    row_count = int(out.split()[0]) - 1
    empties = run_shell(f"awk -F'\\t' 'NR==1{{next}} {{for(i=1;i<=NF;i++) if($i==\"\") empty[i]++}} END{{for(i=1;i<=NF;i++) print empty[i]}}' '{path}'")
    empty_values = [int(x) for x in empties.splitlines() if x.strip()]
    return {
        'total_lines': int(out.split()[0]),
        'data_rows': row_count,
        'empty_values': empty_values,
    }


def source_id_uniqueness(path):
    out = run_shell(f"awk -F'\\t' 'NR>1 {{if($1 != \"\") c[$1]++}} END{{dup=0; for(k in c) if(c[k]>1) dup++; print length(c); print dup}}' '{path}'")
    lines = [line.strip() for line in out.splitlines() if line.strip()]
    if len(lines) < 2:
        return {'unique_ids': 0, 'duplicate_ids': 0}
    return {'unique_ids': int(lines[0]), 'duplicate_ids': int(lines[1])}


def country_counts(path):
    out = run_shell(f"awk -F'\\t' 'NR==1{{for(i=1;i<=NF;i++) if($i==\"country\") cidx=i; next}} {{if($cidx != \"\") cnt[$cidx]++}} END{{for(k in cnt) print k, cnt[k]}}' '{path}'")
    # awk uses field index with $cidx, but we want country labels, not index. this is intentionally compact and relies on value order.
    # Replace with a correct awk block using the actual country field value.
    out = run_shell(f"awk -F'\\t' 'NR==1{{for(i=1;i<=NF;i++) if($i==\"country\") cidx=i; next}} {{if($(cidx) != \"\") cnt[$(cidx)]++}} END{{for(k in cnt) print k, cnt[k]}}' '{path}'")
    counts = {}
    for line in out.splitlines():
        if not line.strip():
            continue
        parts = line.split()
        if len(parts) >= 2:
            counts[parts[0]] = int(parts[1])
    return counts


def ground_truth_summary(path):
    cmd = "awk -F'\\t' 'NR==1{next} { rows++; if($2 == \"\") empty++; else { nonempty++; n = split($2, a, \",\"); count[n]++; if(match($2,/S2-/)) s2++; if(match($2,/S3-/)) s3++; if(match($2,/S2-/) && match($2,/S3-/)) both++; } if($1 != \"\") s1[$1]++ } END{ print rows; print nonempty; print empty; print length(s1); print s2; print s3; print both; for(k in count) print k, count[k] }' '" + path + "'"
    out = run_shell(cmd)
    lines = [line.strip() for line in out.splitlines() if line.strip()]
    if not lines:
        return {}
    summary = {
        'rows': int(lines[0]),
        'nonempty_matches': int(lines[1]),
        'empty_matches': int(lines[2]),
        'unique_s1': int(lines[3]),
        'rows_with_s2': int(lines[4]),
        'rows_with_s3': int(lines[5]),
        'rows_with_both': int(lines[6]),
    }
    dist = {}
    for line in lines[7:]:
        parts = line.split()
        if len(parts) >= 2:
            dist[parts[0]] = int(parts[1])
    summary['match_count_distribution'] = dist
    return summary


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    summary = {}
    for name, path in FILES.items():
        if name == 'train_ground_truth':
            summary[name] = ground_truth_summary(path)
        else:
            summary[name] = {
                'path': path,
                'row_count': file_stats(path)['data_rows'],
                'country_counts': country_counts(path),
                'entity_id_integrity': source_id_uniqueness(path),
            }
    with open(os.path.join(OUTDIR, 'dataset_summary.json'), 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    print(json.dumps({
        'train_source1': summary['train_source1'],
        'train_source2': summary['train_source2'],
        'train_source3': summary['train_source3'],
        'train_ground_truth': summary['train_ground_truth'],
        'test_source1': summary['test_source1'],
        'test_source2': summary['test_source2'],
        'test_source3': summary['test_source3'],
    }, ensure_ascii=False, indent=2)[:18000])

if __name__ == '__main__':
    main()
