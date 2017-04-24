import config as cfg
import numpy as np

def angle_change(hsd_in, angle, he_mode):
    '''

    :param hsd_in:
    :param he_lable:
    :param tmpl_angle:
    :param he_mode:
    :return:
    '''
    DEF = cfg.config_const()
    if he_mode == 0:
        lab_val = DEF.H_LABEL
    elif he_mode == 1:
        lab_val = DEF.E_LABEL
    else:
        print("[ERROR]: HE MODE input fail!")
        lab_val = -1

    hsd_dat = hsd_in
    hsd_out = hsd_dat * angle[lab_val]

    return hsd_out

def landmask_change(hsd_in, he_label, lm_label, img_landmask, tmpl_landmask, cxy_mode):
    '''

    :param hsd_in:
    :param he_label:
    :param lm_label:
    :param img_landmask:
    :param tmpl_landmask:
    :param cxy_mode:
    :return:
    '''
    DEF = cfg.config_const()

    hsd_dat = hsd_in[:, :, cxy_mode] * ((he_label == DEF.H_LABEL) | (he_label == DEF.E_LABEL))
    img_scaled = np.zeros(hsd_dat.shape)

    for i in range(0, 5):
        img_scaled = (img_scaled) + (hsd_dat * (lm_label == i) * (img_landmask[i] / tmpl_landmask[i]))

    return img_scaled

def lm_linear_scaling(hsd_in, he_label, img_info, tmpl_param, he_mode):
    '''

    :param hsd_in:
    :param he_label:
    :param img_info: [param, lm_label]
    :param tmpl_landmsk: [[lm_x_min,lm_h_cx,lm_x_max],[lm_x_min,lm_e_cx,lm_x_max],
                         [lm_y_min,lm_h_cy,lm_y_max],[lm_y_min,lm_e_cy,lm_y_max]]
    :param he_mode:0:h,1:e
    :return:
    '''
    #lm_label = ([[lm_label_Cx_h], [lm_label_Cx_e], [lm_label_Cy_h], [lm_label_Cy_e]])
    lm_label = img_info[1]
    img_parm = img_info[0]
    img_landmask = img_parm[2]
    tmpl_landmask = tmpl_param[2]
    if(he_mode == 0):
        #Cx_h
        img_scaled_Cx = landmask_change(hsd_in, he_label, lm_label[0], img_landmask[0], tmpl_landmask[0], 0)
        #Cy_h
        img_scaled_Cy = landmask_change(hsd_in, he_label, lm_label[2], img_landmask[2], tmpl_landmask[2], 1)
    elif(he_mode == 1):
        #Cx_e
        img_scaled_Cx = landmask_change(hsd_in, he_label, lm_label[1], img_landmask[1], tmpl_landmask[1], 0)
        #Cy_e
        img_scaled_Cy = landmask_change(hsd_in, he_label, lm_label[3], img_landmask[3], tmpl_landmask[3], 1)

    img_scaled = [[img_scaled_Cx], [img_scaled_Cy]]

    return img_scaled

def mean_change(hsd_in, he_label, he_mean, he_mode):
    '''

    :param hsd_in:
    :param he_label:
    :param img_info:
    :param he_mode:
    :return:
    '''
    DEF = cfg.config_const()
    if he_mode == 0:
        lab_val = DEF.H_LABEL
    elif he_mode == 1:
        lab_val = DEF.E_LABEL
    else:
        print("[ERROR]: HE MODE input fail!")
        lab_val = -1

    hsd_dat = hsd_in * (he_label == DEF.H_LABEL | he_label == DEF.E_LABEL)

    mean = he_mean[lab_val]#h_mean or e_mean
    hsd_dat_out = hsd_dat - mean

    return hsd_dat_out


def density_transfer_he(hsd_in, he_label, img_info, tmpl_param, img_st_d, tmpl_st_d, he_mode):
    '''

    :param hsd_in:
    :param he_label:
    :param img_info:
    :param tmpl_param:
    :param he_mode:
    :return:
    '''
    DEF = cfg.config_const()
    if he_mode == 0:
        lab_val = DEF.H_LABEL
    elif he_mode == 1:
        lab_val = DEF.E_LABEL
    else:
        print("[ERROR]: HE MODE input fail!")
        lab_val = -1

    hsd_dat = hsd_in * (he_label == lab_val)
    hsd_dat_d = hsd_dat[:, :, 2]

    tmpl_mean = tmpl_param[0]
    tmpl_u = tmpl_mean[lab_val]

    img_mean = img_info[0][0]
    img_u = img_mean[lab_val]

    hsd_dat_d_out = (hsd_dat_d - img_u) /img_st_d * tmpl_st_d + tmpl_u

def density_transfer_all(hsd_in, he_label, img_info, tmpl_param, img_st_d,tmpl_st_d):

    hsd_d_h = density_transfer_he(hsd_in, he_label, img_info, tmpl_param, img_st_d, tmpl_st_d, 0)
    hsd_d_e = density_transfer_he(hsd_in, he_label, img_info, tmpl_param, img_st_d, tmpl_st_d, 1)

    return [hsd_d_h, hsd_d_e]


def background_transfer(hsd_in, he_label,img_info, tmpl_param):
    '''

    :param hsd_in: hsd_dat[b][:,:,0:2] Cx Cy D of b kinds of pixels
    :param he_label:
    :param img_info:
    :param tmpl_param:
    :return: hsd_dat[b][:,:,0:2] Cx Cy D of b kinds of pixels after transform
    '''
    DEF = cfg.config_const()

    img_mean = img_info[0][0]
    img_u_b = img_mean[2]

    tmpl_mean = tmpl_param[0]
    tmpl_u_b = tmpl_mean[2]

    hsd_dat = hsd_in * (he_label == DEF.B_LABEL)

    hsd_dat_out = hsd_dat - img_u_b + tmpl_u_b

    return hsd_dat_out


def gen_hsd_with_weight():
    return 0

def transform_to_tmpl(hsd_in, he_label, img_info, tmpl_param):
    '''

    :param hsd_in:he kinds of pixels transfered to orig
    :param he_lable:
    :param img_info:[param, lm_label]
    :param tmpl_param:[mean, angle, lm]
    :param tmpl_param:[mean, angle, lm]
    :param he_mode:
    :return:
    '''
    hsd_out = 0
    img_shape = np.shape(hsd_in)

    # #extract img angle feature from img info
    # img_angle = img_info[0][1]
    # img_angle_h = img_angle[0]
    # img_angle_e = img_angle[1]
    #
    # #extract img mean feature from img param
    # img_mean = img_info[0][0]
    # img_mean_h = img_mean[0]
    # img_mean_e = img_mean[1]

    #extract tmpl angle feature from tmpl param
    tmpl_angle = tmpl_param[1]
    tmpl_angle_h = tmpl_angle[0]
    tmpl_angle_e = tmpl_angle[1]

    #extract tmpl mean feature from tmpl param
    tmpl_mean = tmpl_param[0]
    tmpl_mean_h = tmpl_mean[0]
    tmpl_mean_e = tmpl_mean[1]

    #extract img std feature from img param
    img_st_d = img_info[0][3]

    #extract img std feature from img param
    tmpl_st_d = tmpl_param[3]

    #Piece-wise linear scaling
    img_scaled_h_xy = lm_linear_scaling(hsd_in, he_label, img_info, tmpl_param, 0)
    img_scaled_e_xy = lm_linear_scaling(hsd_in, he_label, img_info, tmpl_param, 1)

    #combine img_scaled Cx and Cy
    img_scaled_h = np.zeros(img_shape)
    img_scaled_e = np.zeros(img_shape)

    img_scaled_h[:, :, 0] = img_scaled_h_xy[0]
    img_scaled_h[:, :, 1] = img_scaled_h_xy[1]
    img_scaled_e[:, :, 0] = img_scaled_e_xy[0]
    img_scaled_e[:, :, 1] = img_scaled_e_xy[1]

    #rotate tmpl_angle
    T_hsd_h = angle_change(img_scaled_h, tmpl_angle_h, 0)
    T_hsd_e = angle_change(img_scaled_e, tmpl_angle_e, 1)

    #mean change on tmpl
    T_hsdout_h = mean_change(T_hsd_h, he_label, tmpl_mean_h, 0)
    T_hsdout_e = mean_change(T_hsd_e, he_label, tmpl_mean_e, 1)

    #density transfer
    T_d_out = density_transfer_all(hsd_in, he_label,img_info, tmpl_param,img_st_d,tmpl_st_d)

    #background transfer
    T_b_out = background_transfer(hsd_in, he_label,img_info,tmpl_param)

    #combine T_hsdout_h , T_hsdout_e, T_d_out, T_b_out with weight



    return hsd_out

