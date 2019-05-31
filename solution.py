#!/usr/bin/env python
# coding: utf-8

import numpy as np
from PIL import Image
import argparse
import os

# Pass directory path
parser = argparse.ArgumentParser(description='First test task on images similarity.')
parser.add_argument('--path', help='folder with images', type=str,required=True)
parsed_args = parser.parse_args()

path = parsed_args.path

# Create list of all files in the directory
all_imgs_names = os.listdir(path)

# Load all files in the directory
all_imgs= []
for i in all_imgs_names:
    img = Image.open(path+"\\"+i)
    all_imgs.append(img)

# The approach consists of 2 parts: if imgs have same size and diff of their vectors==0 => they are duplicate
# If images are not dupicate we transform them and compare their histograms. The higher the intersection, the higher is their similarity

def return_intersection(hist_1, hist_2):
    minima = np.minimum(hist_1, hist_2)
    intersection = np.true_divide(np.sum(minima), np.sum(hist_2))
    return intersection

# Let's assume that all imges with intersection higher that 0.85 are similar to each other (or modified).
inters_threshold = 0.85

for i in range(0, len(all_imgs)):
    for j in range(i+1, len(all_imgs)):
        i_shape = np.asarray(all_imgs[i]).shape
        j_shape = np.asarray(all_imgs[j]).shape

        if i_shape == j_shape:
            im_diff = np.sum(np.asarray(all_imgs[i]) - np.asarray(all_imgs[j]))
            if im_diff==0:
                dupl_pair = str(all_imgs_names [i])+" "+ str(all_imgs_names [j])
                print(dupl_pair)
            else:
                a = all_imgs[i].resize(all_imgs[i].size, resample=Image.BICUBIC)
                b = all_imgs[j].resize(all_imgs[i].size, resample=Image.BICUBIC)

                hist_1,_ = np.histogram(a, bins=100)
                hist_2,_ = np.histogram(b, bins=100)        

                inters_coef = return_intersection(hist_1, hist_2)

                if inters_coef > inters_threshold:
                    similar_pair =  str(all_imgs_names [i])+" "+ str(all_imgs_names [j])
                    print(str(all_imgs_names[i])+" "+ str(all_imgs_names[j]))

        else:
            a = all_imgs[i].resize(all_imgs[i].size, resample=Image.BICUBIC)
            b = all_imgs[j].resize(all_imgs[i].size, resample=Image.BICUBIC)

            hist_1,_ = np.histogram(a, bins=100)
            hist_2,_ = np.histogram(b, bins=100)        

            inters_coef = return_intersection(hist_1, hist_2)

            if inters_coef > inters_threshold:
                similar_pair =  str(all_imgs_names [i])+" "+ str(all_imgs_names [j])
                print(str(all_imgs_names[i])+" "+ str(all_imgs_names[j]))
