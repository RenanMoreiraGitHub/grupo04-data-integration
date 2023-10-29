import cv2
import boto3
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

def read_data_s3(bucket_path:str) -> str:
    date = datetime.now().strftime("%Y%m%d")
    s3 = boto3.resource('s3')
    s3.download_file(bucket_path, f'MERGE_CPTEC_{date}.jpeg', f'data_raw\MERGE_CPTEC_{date}.jpeg')
    return f'data_raw\MERGE_CPTEC_{date}.jpeg'

def main(img_path:str) -> float:
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
    
    kernel = np.ones((3,3),np.uint8)
    opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 3)

    sure_bg = cv2.dilate(opening,kernel,iterations=4)
    percentage = (np.count_nonzero(sure_bg == 0) * 100)/(sure_bg.shape[0] * sure_bg.shape[1])
    return round(percentage, 2)

def slice(path_img:str) -> str:
    path_save = path_save.replace('data_raw','data')
    img = plt.imread(path_img)[58:-55, 192:-98]
    plt.imsave(path_save, img)
    return path_save

if __name__ =='__main__':
    BUCKET = 'test-img-grupo04/img/'
    img = read_data_s3(BUCKET)
    file = slice(img)
    percentage = main(file)
    
    #TO DO: SAVE IN SOME PLACE PLEASE
    print(percentage)
