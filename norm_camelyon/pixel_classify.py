import numpy as np
from sklearn.cluster import KMeans
from sklearn.utils import shuffle
import config as cfg
import hsd_transform as hsl


#cluster three kinds of pixels
def pixels_classify(img, sort_label, labels, w, h):
    label_idx = 0
    img_shape = img.shape
    heb_label = np.zeros((img_shape[0], img_shape[1]))

    DEF= cfg.config_const()

    for i in range(w):
        for j in range(h):
            if (labels[label_idx] == sort_label[0]):
                heb_label[i][j] = DEF.H_LABEL
            if (labels[label_idx] == sort_label[1]):
                heb_label[i][j] = DEF.E_LABEL
            if (labels[label_idx] == sort_label[2]):
            #if a pixel is b classes in k-mean,and its density is lower than 0.2, classify this pixel to background
                if(hsl.pixel_rgb2hsd(img[i][j])[2] < 0.2):
                    heb_label[i][j] = DEF.B_LABEL
            # if a pixel is b classes in k-mean,but its density is higher than 0.2, classify this pixel to cytoplasm
            # and then change its orig label
                else:
                    heb_label[i][j] = DEF.E_LABEL
            label_idx += 1

    return heb_label


##input patch color label
##sort label of color by optical density of the hsd color model
##output cell nucleus,cytoplasm and background label
def label_sort(patch_label):
    pixel_hsd = []
    hsd_d = []
    nu_id = 0
    cyt_id = 0
    b_id = 0

    for pixel_rgb in patch_label:
        hsd = hsl.pixel_rgb2hsd(pixel_rgb)
        pixel_hsd.append(hsd)
        hsd_d.append(hsd[2])
    pixel_hsd = np.array(pixel_hsd)
    #sort by density
    for i in hsd_d:
        if (i == max(hsd_d)):
            nu_id = hsd_d.index(i)
        elif (i == min(hsd_d)):
            b_id = hsd_d.index(i)
        else:
            cyt_id = hsd_d.index(i)

    sort_label = nu_id, cyt_id, b_id
    return sort_label

def patch_pixel_cluster(rgb_dat, n_colors):
    heb_label = [0]

    orig_img_rgb = rgb_dat
    orig_img = np.array(orig_img_rgb, dtype=np.float64) / 255

    # Load Image and transform to a 2D numpy array.
    w, h, d = original_shape = tuple(orig_img.shape)
    assert d == 3
    image_array = np.reshape(orig_img, (w * h, d))

    image_array_sample = shuffle(image_array, random_state=0)[:1000]
    kmeans = KMeans(n_clusters=n_colors, random_state=0).fit(image_array_sample)

    # Get labels for all points
    print("Predicting color indices on the full image (k-means)")
    labels = kmeans.predict(image_array)

    #sort patch_label,the first is nucleus,the second is cytoplasm,the last is background
    sort_label = label_sort(kmeans.cluster_centers_)

    #cluster the three kinds of pixels in the orig img
    heb_label = pixels_classify(orig_img_rgb,sort_label,labels, w, h)

    return  heb_label



