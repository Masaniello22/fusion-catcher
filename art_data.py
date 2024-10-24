import os
import subprocess
import sys

def run_art_illumina(fasta_filename, fusim_fasta_dir_path, art_output_path):
    result = subprocess.run([
        'art_illumina',
        '-i', os.path.join(fusim_fasta_dir_path, fasta_filename),
        '-l', '150',
        '-f', '10',
        '-p',
        '-m', '400',
        '-s', '10',
        '-o', os.path.join(art_output_path, fasta_filename)
    ])

    if result.returncode != 0:
        print(f"Error processing {fasta_filename}: {result.stderr}", file=sys.stderr)


if __name__ == '__main__':
    data_path = "data"
    fusim_output_path = os.path.join(data_path, "fusim_output")
    fusim_fasta_dir_path = os.path.join(fusim_output_path, "fusim_fasta_dir")
    art_output_path = os.path.join(data_path, "art_output")

    os.makedirs(art_output_path, exist_ok=True)

    if not os.path.exists(fusim_fasta_dir_path) or not os.listdir(fusim_fasta_dir_path):
        print(f"No FASTA files found in {fusim_fasta_dir_path}", file=sys.stderr)
    else:
        fasta_files = os.listdir(fusim_fasta_dir_path)
        for fasta_filename in fasta_files:
            print(f"Processing {fasta_filename}...")
            run_art_illumina(fasta_filename, fusim_fasta_dir_path, art_output_path)
