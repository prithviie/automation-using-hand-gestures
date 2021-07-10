import os

# creates sub-directories into the Dataset directory

dirs = []
dataset_dir = 'Dataset'
gestures_file = 'gestures.txt'
all_dataset_dirs_file = 'all_dataset_dirs.txt'

if not os.path.isdir(dataset_dir):
    os.mkdir(dataset_dir)


with open(f'./{os.path.dirname(__file__)}/{gestures_file}', 'r') as f:
    for line in f:
        line = line.strip()

        imagesf = f'{dataset_dir}/{line}'

        if not os.path.isdir(imagesf):
            os.mkdir(imagesf)

        dirs.append(imagesf)


# write the created sub-directories into a text file
count = 0
with open(f'./{os.path.dirname(__file__)}/{all_dataset_dirs_file}', 'w+') as f:
    for d in dirs:
        f.write(f"{d}\n")
