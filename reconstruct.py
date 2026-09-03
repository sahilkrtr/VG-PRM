import os
import glob

chunks = sorted(glob.glob("Dataset.zip.chunk*"))
output_file = "Dataset(5).zip"

print(f"Reconstructing {output_file} from {len(chunks)} chunks...")
with open(output_file, 'wb') as outfile:
    for chunk_file in chunks:
        print(f"  Reading {chunk_file}...")
        with open(chunk_file, 'rb') as infile:
            outfile.write(infile.read())
print("Reconstruction complete!")
