#!/usr/bin/env python3
"""Aggregate private seg-eval-metrics outputs, giving each image equal weight."""
import json
import math
from pathlib import Path
import statistics

GROUPS = ('raw', 'target_informed_neighbor_corrected')


def aggregate(documents, team, batch_id, dataset_ids):
    if not documents or len(documents) != len(dataset_ids) or len(set(dataset_ids)) != len(dataset_ids):
        raise ValueError('Provide one unique dataset ID for every metrics file.')
    result = dict(schema_version=1, team=team, batch_id=batch_id,
                  input_dataset_ids=dataset_ids, file_count=len(documents), stddev='population')
    for group in GROUPS:
        rows = []
        for document in documents:
            row = document.get(group)
            if not isinstance(row, dict) or not isinstance(row.get('dice'), (int, float)):
                raise ValueError(f'Missing {group} metrics or Dice score.')
            for key, value in row.items():
                if value is not None and (isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value)):
                    raise ValueError(f'Invalid {group}.{key}.')
            if not 0 <= row['dice'] <= 1:
                raise ValueError(f'Invalid {group} Dice score.')
            rows.append(row)
        result[group] = {}
        for key in sorted(set().union(*(row.keys() for row in rows))):
            values = [row[key] for row in rows if row.get(key) is not None]
            result[group][key] = {
                'mean': statistics.fmean(values) if values else None,
                'std': statistics.pstdev(values) if values else None,
                'n': len(values),
            }
    return result


def main():
    config = json.loads(Path('config.json').read_text())
    paths = config['metrics']
    ids = config['input_dataset_ids']
    if isinstance(ids, str):
        ids = json.loads(ids)
    if not isinstance(paths, list) or not all(isinstance(path, str) for path in paths):
        raise ValueError('metrics must be an array of staged metrics.json paths.')
    documents = [json.loads(Path(path).read_text()) for path in paths]
    output = aggregate(documents, config['team'], config['batch_id'], ids)
    Path('aggregate').mkdir(exist_ok=True)
    Path('aggregate/aggregate.json').write_text(json.dumps(output, indent=2, allow_nan=False) + '\n')


if __name__ == '__main__':
    main()
