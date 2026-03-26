import os, json
import csv
import re
from tabulate import tabulate
from constants import (
    CSV_INST
)

def csv_shape_check(pred_rows, gt_rows):
    # check if the predicted csv has different length in each row
    if not pred_rows or not pred_rows[0]:
        return False
    
    # check if each row has the same number of fields
    num_fields = len(pred_rows[0])
    if False in [len(r) == num_fields for r in pred_rows]:
        return False
    
    # check if the shape of predicted csv matches the ground truth csv
    if len(pred_rows) != len(gt_rows) or any(
        len(pred_rows[i]) != len(gt_rows[i]) for i in range(len(gt_rows))
    ):
        return False
    
    return True
    
def compare_csv_with_ground_truth(metadata, pred_json, gt_csv_dir):
    results = metadata.copy()
    # stats
    stats = {
        # overall
        'total_cnt': 0,
        'format_success_cnt': 0,
        # value
        'total_value_cnt': 0,
        'A_MAPE': 0.0,
        'APE_sum': 0.0
    }
    chart_types = ['bar', 'line', 'scatter', 'pie', 'radar']
    stats_by_type = {ct: stats.copy() for ct in ['all'] + chart_types}
    
    pred_json = json.load(open(pred_json))
        
    for image_name, v in results.items():
        figure_id = image_name
        gt_csv_path = os.path.join(gt_csv_dir, figure_id.rsplit(".", 1)[0] + ".csv")
        assert os.path.exists(gt_csv_path)
        with open(gt_csv_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f, delimiter=",", skipinitialspace=True)
            gt_rows = list(reader)

        has_class = gt_rows[0][0].strip().lower() == "class"
        cur_value_cnt = (len(gt_rows) - 1) * (len(gt_rows[0]) - int(has_class))
        chart_type = v['chart_type']
        for ct in ['all', chart_type]:
            stats_by_type[ct]['total_cnt'] += 1
            stats_by_type[ct]['total_value_cnt'] += cur_value_cnt
        
        pred_payload = pred_json[figure_id]['response']

        has_csv = True
        if '```csv\n' not in pred_payload:
            has_csv = False
        pred_payload = pred_payload.split('```csv\n')[-1]
        if '\n```' not in pred_payload:
            has_csv = False
        
        if not has_csv:
            for ct in ['all', chart_type]:
                stats_by_type[ct]['APE_sum'] += 1.0 * cur_value_cnt
            
            results[image_name]['format_success'] = False
            continue
                
        pred_payload = pred_payload.split('\n```')[0].strip()
        pred_rows = list(csv.reader(pred_payload.splitlines(), delimiter=',', skipinitialspace=True, quotechar='"'))
        if not csv_shape_check(pred_rows, gt_rows):
            for ct in ['all', chart_type]:
                stats_by_type[ct]['APE_sum'] += 1.0 * cur_value_cnt
            results[image_name]['format_success'] = False
            continue
        
        results[image_name]['format_success'] = True
        for ct in ['all', chart_type]:
            stats_by_type[ct]['format_success_cnt'] += 1
            
        # compare numerical values
        results[image_name]['total_values'] = 0
        gt_value_list = []
        pred_value_list = []
        ape_list = []
        # parse gt values first
        for i in range(1, len(pred_rows)):
            for j in range(int(has_class), len(gt_rows[0])):
                regex = r"\s*([-+]?(?:\d+\.\d*|\.\d+|\d+)).*"
                gt_value = gt_rows[i][j].strip()
                match = re.match(regex, gt_value)
                gt_value = float(match.group(1))
                gt_value_list.append(gt_value)
        # then parse pred values
        for i in range(1, len(pred_rows)):
            for j in range(int(has_class), len(gt_rows[0])):
                regex = r"[^0-9+-]*([-+]?(?:\d+\.\d*|\.\d+|\d+)).*"
                pred_value = pred_rows[i][j].strip()
                match = re.match(regex, pred_value)
                if not match:
                    pred_value_list.append(None)
                    continue
                try:
                    pred_value = float(match.group(1))
                    pred_value_list.append(pred_value)
                except:
                    pred_value_list.append(None)
                    print(f"ValueError in {image_name} at row {i}, col {j}: pred '{pred_value}' vs gt '{gt_value_list[len(pred_value_list) - 1]}'")
        
        assert len(gt_value_list) == len(pred_value_list), f"Value list length mismatch in {image_name}: pred {len(pred_value_list)} vs gt {len(gt_value_list)}"
        
        # mape calculation
        max_gt_value = max(abs(v) for v in gt_value_list if abs(v) > 1e-6) if any(abs(v) > 1e-6 for v in gt_value_list) else 1.0
        if chart_type == 'scatter':
            gt_value_x = gt_value_list[0::2]
            gt_value_y = gt_value_list[1::2]
            max_gt_value_x = max(abs(v) for v in gt_value_x if abs(v) > 1e-6) if any(abs(v) > 1e-6 for v in gt_value_x) else 1.0
            max_gt_value_y = max(abs(v) for v in gt_value_y if abs(v) > 1e-6) if any(abs(v) > 1e-6 for v in gt_value_y) else 1.0
        for i in range(len(gt_value_list)):
            if chart_type == 'scatter':
                max_gt_value = max_gt_value_x if i % 2 == 0 else max_gt_value_y
            results[image_name]['total_values'] += 1
            pred_value = pred_value_list[i]
            gt_value = gt_value_list[i]
            if pred_value is None:
                ape_list.append(1.0)
                continue
            
            pe = min(1.0, abs(pred_value - gt_value) / max_gt_value)
            ape_list.append(pe)
        
        assert results[image_name]['total_values'] == cur_value_cnt
        assert len(ape_list) == cur_value_cnt
        
        results[image_name]['A_MAPE'] = sum(ape_list) / cur_value_cnt if cur_value_cnt > 0 else None
        
        for ct in ['all', chart_type]:
            stats_by_type[ct]['APE_sum'] += sum(ape_list)

    # calculate MAPE
    for ct in stats_by_type:
        total_value_cnt = stats_by_type[ct]['total_value_cnt']
        APE_sum = stats_by_type[ct]['APE_sum']
        stats_by_type[ct]['A_MAPE'] = APE_sum / total_value_cnt if total_value_cnt > 0 else None

    print("Comparing numerical values...")
    # print summary statistics table
    headers = [
        "Chart Type", "Total", "Format Success Rate", "Total Values", "Adaptive MAPE"
    ]
    data = [
        [
            ct,
            stats_by_type[ct]['total_cnt'],
            f"{(stats_by_type[ct]['format_success_cnt'] / stats_by_type[ct]['total_cnt'] * 100):.2f}%" if stats_by_type[ct]['total_cnt'] > 0 else "N/A",
            stats_by_type[ct]['total_value_cnt'],
            f"{stats_by_type[ct]['A_MAPE']*100:.2f}%" if stats_by_type[ct]['A_MAPE'] is not None else "N/A"
        ]
        for ct in stats_by_type
    ]
    print(tabulate(data, headers=headers, tablefmt="grid"))

    return results

def csv_query_helper(csv_path):
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=",")
        rows = list(reader)

    if not rows or not rows[0]:
        raise ValueError(f"csv is empty or missing header: {csv_path}")

    header = rows[0]
    num_fields = len(header)
    assert False not in [
        len(r) == num_fields for r in rows[1:]
    ], f"csv rows have different number of fields: {csv_path}"
    first_col_name = header[0]
    has_class = first_col_name.strip().lower() == "class"

    masked_rows = []
    masked_rows.append([f'"{h}"' for h in header])

    for r in rows[1:]:
        masked = []
        for j in range(num_fields):
            if has_class and j == 0:
                # has class column -> keep the class value
                masked.append(f'"{r[j].strip()}"')
            else:
                masked.append("____")
        masked_rows.append(masked)

    masked_csv_text = "\n".join([",".join(row) for row in masked_rows])
    prompt = CSV_INST.format(len(rows), num_fields, masked_csv_text)
    return prompt

def build_csv_quries(data, dataset_dir):
    queries = {}
    for image_name, d in data.items():
        figure_path = os.path.join(dataset_dir, "image", image_name)
        csv_path = os.path.join(
            dataset_dir, "csv", image_name.rsplit(".", 1)[0] + ".csv"
        )
        question = csv_query_helper(csv_path)
        curr_query = {
            "figure_id": image_name,  # figure_name
            "figure_path": figure_path,  # figure_path (dropped later)
            "question": question,  # question content
        }
        queries[image_name] = curr_query
    return queries


if __name__ == "__main__":
    # for testing purposes
    print(csv_query_helper("dataset/csv/00000.csv"))
