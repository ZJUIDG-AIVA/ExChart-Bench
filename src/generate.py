import os
import json
import argparse
from csv_utils import build_csv_quries

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # input/output
    parser.add_argument(
        "--data_dir",
        type=str,
        required=False,
        default="./dataset"
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        required=False,
        default="./results",
        help="Directory to save the output json files",
    )
    parser.add_argument("--model_name", type=str, required=True)
    parser.add_argument("--model_path", type=str, required=True)
    parser.add_argument("--model_api", type=str, required=False, default=None)
    args = parser.parse_args()

    metadata = os.path.join(args.data_dir, "metadata.json")
    print(f"Reading {metadata}...")
    with open(metadata) as f:
        metadata = json.load(f)
        
    os.makedirs(args.output_dir, exist_ok=True)
    output_file = os.path.join(
        args.output_dir, f"gen-{args.model_name}.json"
    )
    
    queries = build_csv_quries(metadata, args.data_dir)

    print("Number of charts to extract:", len(queries))
    print("Output file:", output_file)

    from qwen2_5 import generate_response
    generate_response(queries, args.model_path)

    for k in queries:
        queries[k].pop("figure_path", None)
        queries[k].pop("question", None)

    try:
        print(f"Saving results to {output_file}...")
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, "w+") as f:
            json.dump(queries, f, indent=4)
        print(f"Results saved.")
    except Exception as e:
        print(e)
        print(f"Error in saving {output_file}")
