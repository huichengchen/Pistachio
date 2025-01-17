﻿# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 12:18:04 2019
@author: icheng
"""
import argparse
from PIL import Image
import numpy as np
import random
import time
import os

def setSize(path,savepath,x,y): 
    """
    重新设置图片大小  最终输出为保存图片为x*y像素
    path :资源图片路径   savepath:输出图片保存路径
    """
    print(path)
    image = Image.open(path)
    width, height = image.size
    if(width > height):
        left = (width - height) // 2
        box=(left,0,left + height,height)
        image = image.crop(box)
    elif(width < height):
        top = (height - width) // 2
        box=(0,top,width,top + width)
        image = image.crop(box)
    image = image.resize((x,y),Image.ANTIALIAS)  #此处可更改输出图片大小
    image = image.convert('RGB')
    image.save(savepath)


 
def getColor(path): 
    """
    获取图片的大致色彩 保存为RGB
    """   
    image = Image.open(path)
    data = list(image.getdata())
    b = np.array([0,0,0])
    for i in data:
        a = np.array(i)
        b = np.add(a,b)
    b = list(b)
    b = [i // 10000 for i in b]
    b = tuple(b)
    c = np.array([0,0,0])
    count = 0
    for i in data:
        a = np.array(i)
        temp = list(np.subtract(a,b))
        temp = abs(temp[0]) + abs(temp[1]) + abs(temp[2])
        if(temp > 200):
            continue
        count += 1
        c = np.add(a,c)
    c = list(c)
    c = [i // count for i in c]
    c = tuple(c)
    return c           #此处可选择  b  OR  c


def write(data):
    path = 'colorlist.txt'
    f = open(path,'w')
    for i in data:
        f.write(str(i)+'\n')
    f.close()
    
def read():
    path = 'colorlist.txt'
    data = []
    f = open(path,'r')
    for line in f:
        temp = line[1:-2].split(',')
        temp = [int(i.strip()) for i in temp]
        data.append(temp)
    f.close()
    return data

def imageToColor(num):  #将批量图片转化为颜色 
    data = []
    for i in range(num):
        path = 'source\image_{}.jpg'.format(i)
        color = getColor(path)
        data.append(color)
    write(data)

def findSimilerImage(data,pixel,similer):
    """
    查找与 像素 最相近的点
    """
    index = []
    for i in range(len(data)):
        temp = abs(data[i][0]-pixel[0]) + abs(data[i][1]-pixel[1]) + abs(data[i][2]-pixel[2])
        if(temp < similer):
            index.append(i)
    if(len(index) == 0):
        index = findSimilerImage(data,pixel,2*similer)
    return index
    
def dealImage(path,edge):  
    """
    处理图片  输出 像素填充图
    """
    data = read()
    inImage = Image.open(path)
    x = inImage.size[0]
    y = inImage.size[1]
    outImage = Image.new('RGB',(x*edge,y*edge))
    for i in range(x):
        for j in range(y):
            pixel = inImage.getpixel((i,j))
            indexlist = findSimilerImage(data,pixel,100)
            index = random.randint(0,len(indexlist)-1)
            sourcePath = 'source\image_{}.jpg'.format(indexlist[index])
            sourceImage = Image.open(sourcePath)
            outImage.paste(sourceImage,(i*edge,j*edge))
    outImage.save('ouput.jpg')
     
        
        
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str, default='', help='imgs path must')
    parser.add_argument('--resize', type=int, default='100', help='imgs resize')
    parser.add_argument('--img', type=str, default='', help='source img must')
    parser.add_argument('--size', type=int, default='100', help='img size')
    opt = parser.parse_args()

    if(opt.path != ""):
        path=opt.path
        resize=opt.resize
        imgs = os.listdir(path)
        i=0
        for img in imgs:
            if(img.endswith(".jpg") or img.endswith(".png")):
                imgpath = os.path.join(path,img)
                savepath = os.path.join("source","image_{}.jpg".format(i))
                setSize(imgpath,savepath,resize,resize)   
        
    if(opt.img != ""):
        imgs = os.listdir("source")
        if(len(imgs) > 0):
            print('Processing...')
            imageToColor(len(imgs))
            imgpath = opt.img
            dealImage(imgpath,len(imgs))
            print('successfully')
        else:
            print("please using: python pixelImage.py --path [imgs_path] --resize [size]")
    print('Exit after 3 seconds')
    time.sleep(3)
    
