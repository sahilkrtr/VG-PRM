import os
import glob

# Find all existing large parts
large_files = sorted(glob.glob("Dataset(5).zip.part*"))

if not large_files:
    print("No large files found to split.")
    exit()

CHUNK_SIZE = 90 * 1024 * 1024 # 90MB to be safely under GitHub's 100MB limit
out_idx = 1

# We will concatenate conceptually and split into 90MB chunks
# To avoid requiring 2.5GB of extra disk space, we will read and write, then delete the original
# Or just keep them if disk space is enough. Let's delete them after successful read.

for large_file in large_files:
    print(f"Processing {large_file}...")
    with open(large_file, 'rb') as infile:
        while True:
            chunk = infile.read(CHUNK_SIZE)
            if not chunk:
                break
            out_name = f"Dataset.zip.chunk{out_idx:03d}"
            print(f"  Writing {out_name} ({len(chunk)} bytes)...")
            with open(out_name, 'wb') as outfile:
                outfile.write(chunk)
            out_idx += 1
    # Delete the large file after we have fully split it
    print(f"Removing {large_file}...")
    os.remove(large_file)

print("Finished splitting all files.")

# Write a reconstruction script for the user
reconstruct_script = """import os
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
"""

with open("reconstruct.py", "w") as f:
    f.write(reconstruct_script)
print("Created reconstruct.py")
