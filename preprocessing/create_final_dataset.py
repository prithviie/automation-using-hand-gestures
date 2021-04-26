import os
import shutil

all_dataset_dirs_file = 'preprocessing/all_dataset_dirs.txt'

final_dataset_dir = 'Dataset'
train_dir = "Training"
test_dir = "Testing"

if not os.path.isdir(final_dataset_dir):
    os.mkdir(final_dataset_dir)
    os.mkdir(f"{final_dataset_dir}/{train_dir}")
    os.mkdir(f"{final_dataset_dir}/{test_dir}")


folders_to_copy_from = []

with open(all_dataset_dirs_file, 'r') as f:
    for line in f:
        line = line.strip()
        if len(line) > 10:
            idx = line.index('/', 14)
            line = line[1:idx]
            folders_to_copy_from.append(line)


for loc in folders_to_copy_from:
    for f in os.listdir(loc):
        if 'train' in f:
            shutil.copy(f"{loc}/{f}", f"{final_dataset_dir}/{train_dir}/")
        else:
            shutil.copy(f"{loc}/{f}", f"{final_dataset_dir}/{test_dir}/")