import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder
import os
os.system('clear')

gestures_file = 'gestures.txt'
gestures_labelled_file = 'gestures_labelled.txt'
separator = '\t'

gestures = []
with open(f'./{os.path.dirname(__file__)}/{gestures_file}', 'r') as f:
    for line in f:
        line = line.strip()
        gestures.append(line)

gestures.sort()
gestures = np.array([gestures[i] for i in range(len(gestures))])
# print(gestures)

integer_encoded = LabelEncoder().fit_transform(gestures)
# print(integer_encoded)

integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
onehot_encoded = OneHotEncoder(sparse=False).fit_transform(integer_encoded)
# print(onehot_encoded)

with open(f'./{os.path.dirname(__file__)}/{gestures_labelled_file}', 'w+') as f:
    for i in range(len(gestures)):
        f.write(f"{gestures[i]}{separator}{integer_encoded[i]}{separator}{str(onehot_encoded[i]).replace('.', ',')[:-2]}]\n")
