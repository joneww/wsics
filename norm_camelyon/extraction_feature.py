import numpy as np
import config as cfg
import transform


def get_st_d(hsd_in, he_label, he_mode):
    DEF = cfg.config_const()

    if he_mode == 0:
        lab_val = DEF.H_LABEL
    if he_mode == 1:
        lab_val = DEF.E_LABEL
    elif he_mode == 2:
        lab_val = DEF.B_LABEL
    else:
        print("[ERROR]: HE MODE input fail!")
        lab_val = -1
    np_label= np.array(he_label)
    label_mask = (np_label == lab_val)
    dat_cnt = np.sum(label_mask)
    dat_mask = hsd_in[:, :, 2] * label_mask
    val_min = np.min(dat_mask)
    val_min_mask =label_mask * val_min
    dat_mask_off  = dat_mask - val_min_mask
    #dat = ()
    arr_dat = dat_mask_off.reshape(dat_mask_off.shape[0]*dat_mask_off.shape[1])
    sort_val = sorted(arr_dat)
    sort_val.reverse()
    outs_val = np.array(sort_val) + val_min
    std_val = np.std(outs_val[:dat_cnt])

    return std_val


def get_img_st_d(hsd_in, he_label):

    std_h = get_st_d(hsd_in, he_label, 0)
    std_e = get_st_d(hsd_in, he_label, 1)
    std_b = get_st_d(hsd_in, he_label, 2)
    std = [std_h, std_e, std_b]

    return std


def get_feature_mean(hsd_dat,he_label,HE_mode):
    '''
    :param hsd_dat:hsd
    :param he_label: h e
    :param mode:0:H 1:E 2:background
    :return:
    '''
    DEF = cfg.config_const()
    if HE_mode == 0:
        label_val = DEF.H_LABEL
    elif HE_mode == 1:
        label_val = DEF.E_LABEL
    elif HE_mode == 2:
        label_val = DEF.B_LABEL
    else:
        print("[ERROR] the mode input fail!")
        label_val = -1
    np_label= np.array(he_label)
    label_mask = (np_label == label_val)
    dat_cnt = np.sum(label_mask)

    dat_sum_cx = np.sum(hsd_dat[:, :, 0] * label_mask)

    dat_sum_cy = np.sum(hsd_dat[:, :, 1] * label_mask)
    dat_sum_d  = np.sum(hsd_dat[:, :, 2] * label_mask)

    m_cx = dat_sum_cx / dat_cnt
    m_cy = dat_sum_cy / dat_cnt
    m_d = dat_sum_d / dat_cnt

    return [m_cx,m_cy,m_d]


def get_feature_angle(hsd_dat,he_label,he_mode=0):
    '''

    :param hsd_dat:[Cx Cy D]
    :param he_label:
    :param he_mode: h:0 e:1
    :return:
    '''


    return 0

def get_landmask_max_min(dat,cxy_mode,he_label):
    '''

    :param dat: [cx cy d] data
    :param cxy_mode: cx:0 cy 1
    :param he_label: h e background label
    :return:
    '''
    DEF = cfg.config_const()
    lab = ((he_label == DEF.H_LABEL)|(he_label == DEF.E_LABEL))
    dat_cnt = np.sum(lab)
    dat_use = dat[:,:,cxy_mode]
    dat_min = np.min(dat_use)
    dat_off = dat_use - lab * dat_min
    arr_dat = dat_off.reshape((dat_off.shape[0]*dat_off.shape[1]))
    arr_dat_sorted = sorted(arr_dat)
    arr_dat_sorted.reverse()
    arr_dat = np.array(arr_dat_sorted) + dat_min
    lm_max = arr_dat[0]
    lm_min = arr_dat[dat_cnt-1]
    return lm_min,lm_max

#计算landmask时，不计算的类别为0 的问题
def get_landmask(dat,he_label,cxy_mode,he_mode):
    '''

    :param dat:[cx,cy,d]
    :param he_label:  array cx cy d
    :param cxy_mode: cx :0 cy:1
    :param he_mode: h:0 e:1
    :return:
    '''
    DEF= cfg.config_const()

    if he_mode == 0:
        lab_val = DEF.H_LABEL
    elif he_mode == 1:
        lab_val = DEF.E_LABEL
    else:
        print("[ERROR]: HE MODE input fail!")
        lab_val = -1
    np_he_label = np.array(he_label)
    lab = (np_he_label==lab_val)
    dat_cnt = np.sum(lab)
    dat_use = dat[:,:,cxy_mode]*lab
    dat_min = np.min(dat_use)
    dat_off = dat_use - lab*dat_min
    array_dat = dat_off.reshape(dat_off.shape[0]*dat_off.shape[1])
    array_dat.sort(axis=1) ##?
    array_dat = array_dat + dat_min
    lm1 = array_dat[int(dat_cnt*0.99)]
    lm25 = array_dat[int(dat_cnt*0.75)]
    lm50 = array_dat[int(dat_cnt*0.5)]
    lm75 = array_dat[int(dat_cnt*0.25)]
    lm99 = array_dat[int(dat_cnt*0.01)]
    return lm1,lm25,lm50,lm75,lm99

def get_all_landmask(hsd_in_h, hsd_in_e, he_label):
    '''

    :param hsd_data:
    :param he_label:
    :return:
    '''

    lm_x_min,lm_x_max = get_landmask_max_min(hsd_in_h, 0, he_label)

    # H Cx
    lm_h_cx = get_landmask(hsd_in_h, he_label, 0, 0)
    # H Cy
    lm_h_cy = get_landmask(hsd_in_h, he_label, 1, 0)



    lm_y_min, lm_y_max = get_landmask_max_min(hsd_in_e, 1, he_label)

    # E Cx
    lm_e_cx = get_landmask(hsd_in_e, he_label, 0, 1)
    # E Cy
    lm_e_cy = get_landmask(hsd_in_e, he_label, 1, 1)

    lm = np.array([[lm_x_min,lm_h_cx,lm_x_max],[lm_x_min,lm_e_cx,lm_x_max],
                   [lm_y_min,lm_h_cy,lm_y_max],[lm_y_min,lm_e_cy,lm_y_max]])

    return lm

def get_all_mean(hsd_dat,he_label):
    '''

    :param hsd_dat:[cx,cy,d]
    :param he_label:
    :return:
    '''

    h_mean = get_feature_mean(hsd_dat, he_label, 0)
    e_mean = get_feature_mean(hsd_dat, he_label, 1)
    b_mean = get_feature_mean(hsd_dat, he_label, 2)
    return [h_mean,e_mean,b_mean]



def get_all_angle(hsd_dat,he_label):
    h_angle = get_feature_angle(hsd_dat,he_label,0)
    e_angle = get_feature_angle(hsd_dat,he_label,1)
    return [h_angle,e_angle]



def get_feature(hsd_dat,he_label):
    mean = get_all_mean(hsd_dat,he_label)
    angle = get_all_angle(hsd_dat,he_label)

    return mean,angle

