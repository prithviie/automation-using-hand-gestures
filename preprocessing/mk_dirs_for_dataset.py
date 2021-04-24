import os

dirs = []
dataset_dir = 'TestDataset'
gestures_file = 'gestures.txt'
all_dataset_dirs_file = 'all_dataset_dirs.txt'


with open(f'./{os.path.dirname(__file__)}/{gestures_file}', 'r') as f:
    for line in f:
        line = line.strip()

        imagesf = f'./{dataset_dir}/{line}_images'
        testf = f'./{dataset_dir}/{line}_test_images'

        if not os.path.isdir(imagesf):
            os.mkdir(imagesf)
            os.mkdir(testf)

        dirs.append(imagesf)
        dirs.append(testf)


count = 0
with open(f'./{os.path.dirname(__file__)}/{all_dataset_dirs_file}', 'w+') as f:
    for d in dirs:
        f.write(f"'{d}/{os.path.basename(d).lower()[:-1]}_'\n")
        count += 1
        if count >= 2:
            count = 0
            f.write('\n')
