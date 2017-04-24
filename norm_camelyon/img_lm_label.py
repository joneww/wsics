import config as cfg

###像素点分段时，b类像素点为0的问题

def get_lm_label_min_max(hsd_in, img_landmask,cxy_mode):
    '''

    :param hsd_in:
    :param img_landmask:
    :param cxy_mode:
    :return:
    '''
    #input include background
    hsd_dat = hsd_in[:,:,cxy_mode]

    lm_label = ((hsd_dat >= img_landmask[0]) & (hsd_dat < img_landmask[1])) * 0  # min-1
    lm_label += ((hsd_dat >= img_landmask[5]) & (hsd_dat <= img_landmask[6])) * 5  # 99-max


def get_lm_label(hsd_in, img_landmask, cxy_mode):
    '''

    :param hsd_in:
    :param img_landmask:
    :param cxy_mode:
    :return:
    '''
    hsd_dat = hsd_in[:, :, cxy_mode]

    lm_label = ((hsd_dat >= img_landmask[1]) & (hsd_dat < img_landmask[2])) * 1  #1-25
    lm_label += ((hsd_dat >= img_landmask[2]) & (hsd_dat < img_landmask[3])) * 2 #25-50
    lm_label += ((hsd_dat >= img_landmask[3]) & (hsd_dat < img_landmask[4])) * 3 #50-75
    lm_label += ((hsd_dat >= img_landmask[4]) & ( hsd_dat < img_landmask[5])) * 4 #75-99

    return lm_label

def get_all_lm_label(hsd_in_h, hsd_in_e, he_label, img_landmask):
    '''

    :param hsd_in:
    :param he_label:
    :param img_landmask:
    :return:
    '''
    img_landmask_h_Cx = img_landmask[0]
    img_landmask_e_Cx = img_landmask[1]
    img_landmask_h_Cy = img_landmask[2]
    img_landmask_e_Cy = img_landmask[3]

    #computer h major lm label
    lm_label_Cx = get_lm_label_min_max(hsd_in_h, img_landmask_h_Cx, 0)
    lm_label_Cy = get_lm_label_min_max(hsd_in_h, img_landmask_h_Cy, 1)

    lm_label_Cx_h = lm_label_Cx + get_lm_label(hsd_in_h, img_landmask_h_Cx, 0)
    lm_label_Cy_h = lm_label_Cy + get_lm_label(hsd_in_h, img_landmask_h_Cy, 1)

    # computer e major lm label
    lm_label_Cx = get_lm_label_min_max(hsd_in_e, he_label, img_landmask_e_Cx, 0)
    lm_label_Cy = get_lm_label_min_max(hsd_in_e, he_label, img_landmask_e_Cy, 1)

    lm_label_Cx_e = lm_label_Cx + get_lm_label(hsd_in_e, img_landmask_e_Cx, 0)
    lm_label_Cy_e = lm_label_Cy + get_lm_label(hsd_in_e, img_landmask_e_Cy, 1)

    lm_label = np.array([[lm_label_Cx_h], [lm_label_Cx_e],
                        [lm_label_Cy_h], [lm_label_Cy_e]])
    return lm_label
