import cv2
import numpy as np
import matplotlib.pyplot as plt


def main(img_path:str) -> float:
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
    
    kernel = np.ones((3,3),np.uint8)
    opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 3)

    sure_bg = cv2.dilate(opening,kernel,iterations=4)
    percentage = (np.count_nonzero(sure_bg == 0) * 100)/(sure_bg.shape[0] * sure_bg.shape[1])
    return round(percentage, 2)

def slice(path_img:str, path_save:str) -> None:
    img = plt.imread(path_img)[58:-55, 192:-98]
    plt.imsave(path_save, img)


if __name__ =='__main__':
    img = "data_raw\MERGE_CPTEC_20231016.jpeg"
    file = "data\MERGE_CPTEC_20231016.png"
    slice(img, file)
    p = main(file)
    print(p)
