# main.py

import argparse
import os
from src.services import export_all_annotations
from src.logger_setup import setup_logging

def parse_args():
    parser = argparse.ArgumentParser(description="Export iBooksX annotations to markdown files.")
    parser.add_argument("-o", "--output", help="Output directory for markdown files", default=".")
    parser.add_argument("--vault", help="Vault base directory", default=None)
    parser.add_argument("--folder", help="Folder name inside the vault directory", default=None)
    return parser.parse_args()

def main():
    setup_logging()
    args = parse_args()
    file_path = args.output
    if args.vault and args.folder:
        file_path = os.path.join(args.vault, args.folder)
    annotation_type_map = {1: "HIGH-IMPORTANCE", 3: "MID-IMPORTANCE"}
    export_all_annotations(file_path, annotation_type_map)

if __name__ == "__main__":
    main()