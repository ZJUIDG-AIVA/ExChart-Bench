import argparse, json
from tqdm import tqdm
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_name', type=str, required=True)
    parser.add_argument("--data_dir", type=str, required=False, default="./dataset")
    args = parser.parse_args()

    args.resp_file = f"results/gen-{args.model_name}.json"
    args.output_file = args.resp_file.replace("gen-", "scores-")
    print(f"Output file: {args.output_file}")

    gt_csv_dir = os.path.join(args.data_dir, "csv")
    from csv_utils import compare_csv_with_ground_truth
    
    metadata = json.load(open(os.path.join(args.data_dir, "metadata.json")))
    results = compare_csv_with_ground_truth(metadata, args.resp_file, gt_csv_dir)

    # output the scores
    with open(args.output_file, "w") as f:
        json.dump(results, f, indent=4)
