import os

# CREATES 2 (TEST AND TRAIN) SUB-DIRECTORIES INTO THE DATASET DIRECTORY FOR EACH GESTURE

dirs = []
dataset_dir = 'Dataset'
gestures_file = 'gestures.txt'
all_dataset_dirs_file = 'all_dataset_dirs.txt'

if not os.path.isdir(dataset_dir):
    os.mkdir(dataset_dir)
    

with open(f'./{os.path.dirname(__file__)}/{gestures_file}', 'r') as f:
    for line in f:
        line = line.strip()

        imagesf = f'{dataset_dir}/{line}_train_images'
        testf = f'{dataset_dir}/{line}_test_images'

        if not os.path.isdir(imagesf):
            os.mkdir(imagesf)
            os.mkdir(testf)

        dirs.append(imagesf)
        dirs.append(testf)


# WRITE THE CREATED SUB-DIRECTORIES INTO TEXT FILE
count = 0
with open(f'./{os.path.dirname(__file__)}/{all_dataset_dirs_file}', 'w+') as f:
    for d in dirs:
        f.write(f"'{d}/{os.path.basename(d).lower()[:-1]}_'\n")
        count += 1
        if count >= 2:
            count = 0
            f.write('\n')
