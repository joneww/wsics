import os
import config as cfg
import extraction_feature as exfeat
import hsd_transform as hsd_t
import pixel_classify as pixc
import matplotlib.image as mpimg
import transform
import img_lm_label as lm_lab


def mean_angel_perprocess(hsd_in, he_label,img_mean, img_angle):
    #extract img angle feature from img info
    img_angle_h = img_angle[0]
    img_angle_e = img_angle[1]

    #extract img mean feature from img param
    img_mean_h = img_mean[0]
    img_mean_e = img_mean[1]

    #mean change on img
    mean_chg_hsd_h = transform.mean_change(hsd_in, he_label, img_mean_h, 0)
    mean_chg_hsd_e = transform.mean_change(hsd_in, he_label, img_mean_e, 1)

    #rotate img_angle
    an_chg_hsd_h = transform.angle_change(mean_chg_hsd_h, img_angle_h, 0)
    an_chg_hsd_e = transform.angle_change(mean_chg_hsd_e, img_angle_e, 1)

    return an_chg_hsd_h, an_chg_hsd_e


def main_init():
    if cfg.init() != 0:
        return 1
    return 0

def get_param(hsd_dat, he_label):
    std = exfeat.get_img_st_d(hsd_dat, he_label)
    mean, angle = exfeat.get_feature(hsd_dat, he_label)

    return [mean, angle, std]


def get_tmpl_param():
    path = cfg.config_path()
    tmpl_path = os.path.join(path.top_dir,path.tmpl_name)
    img_dat = mpimg.imread(tmpl_path)
    hsd_dat = hsd_t.rgb2hsd(img_dat)
    he_label = pixc.patch_pixel_cluster(hsd_dat)

    return get_param(hsd_dat,he_label)


def save_hsd_img(hsd,name):
    path = cfg.config_path()
    outs_path = os.path.join(path.top_dir,path.hsd_dir,name)
    img_dat = hsd_t.hsd2rgb(hsd)
    mpimg.imsave(outs_path,img_dat)

    return  0


def main():
    path = cfg.config_path()
    if main_init()!= 0:
        return 1
    tmpl_param = get_tmpl_param()
    #tmpl land_mask computer

    raw_dir = os.path.join(path.top_dir,path.raw_dir)
    list_dir = os.listdir(raw_dir)
    for name in list_dir:
        name_path = os.path.join(path.top_dir,path.raw_dir,name)

        img_dat = mpimg.imread(name_path)
        hsd_dat = hsd_t.rgb2hsd(img_dat)
        he_label = pixc.patch_pixel_cluster(img_dat, 3)

        #ing_info include img_param and img_lm_label
        img_info = get_param(hsd_dat, he_label)
        #change mean and angle
        img_mean = img_info[0]
        img_angle = img_info[1]
        an_chg_hsd_h, an_chg_hsd_e = mean_angel_perprocess(hsd_dat, he_label, img_mean, img_angle)

        #get land mask ,and get img landmask label
        lm = exfeat.get_all_landmask(an_chg_hsd_h, an_chg_hsd_e, he_label)
        lm_label = lm_lab.get_all_lm_label()

        hsd_out = transform.transform_to_tmpl(hsd_dat, he_label, img_info, tmpl_param)
        save_hsd_img(hsd_out,name)
    return 0

if __name__ == "__main__":
    main()


    an_chg_hsd_h , an_chg_hsd_e = mean_angel_perprocess(hsd_dat, he_label, mean, angle)
    lm = exfeat.get_all_landmask(an_chg_hsd_h, an_chg_hsd_e)
    img_lm_label = lm_lab.get_all_lm_label(hsd_dat,hs_labl,img_landmask)
