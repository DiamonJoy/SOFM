# -*- coding: utf-8 -*-

from random import *
from math import *
from PIL import Image
from time import *

#----------- SOM节点 -------------  
class Node:

    # 初始化
    def __init__(self, X=0, Y=0):
        
        self.R=randint(0,255)  # R值
        self.G=randint(0,255)  # G值
        self.B=randint(0,255)  # B值
        self.X=X               # X坐标
        self.Y=Y               # Y坐标

#----------- SOM结构 -------------  
class SOM:

    # 初始化
    def __init__(self, height=500, width=500):
        
        self.height=height                      # 高度
        self.width=width                        # 宽度 
        self.radius=height/2+width/2            # 半径
        self.total=self.height*self.width       # 总数
        
        self.nodes=[[0 for x in range(self.height)] for y in range(self.width)] # 节点结构

        # 初始化节点结构
        for i in range(self.width):
            for j in range(self.height):
                self.nodes[i][j]=Node(i,j)
    
    # 计算像素距离
    def W_distance(self, r_sample, node):
        return sqrt((r_sample[0]-node.R)**2+(r_sample[1]-node.G)**2+(r_sample[2]-node.B)**2)
    
    # 计算位置距离
    def distance(self, node1, node2):
        return sqrt((node1.X-node2.X)**2+(node1.Y-node2.Y)**2)

    # 获取最优竞争者 
    def get_bmu(self,r_sample):

        # 竞争匹配数目
        match_amt=0
        # 最大距离
        max_dist=1000000.0
        # 匹配列表
        match_list=[]
        # 遍历节点
        for i in range(self.width):
            for j in range(self.height):
                t_dist=self.W_distance(r_sample,self.nodes[i][j])
                # 更新新距离
                if t_dist<max_dist:
                    max_dist=t_dist
                    match_list=[]
                    match_list.append(self.nodes[i][j])
                    match_amt=1
                # 添加节点
                elif t_dist==max_dist:
                    match_list.append(self.nodes[i][j])
                    match_amt+=1
    
        # 返回优胜节点
        return match_list[randint(0,match_amt-1)]
    
    # 更新领域值
    def scale_neighbors(self, bmu_loc, r_sample, times):

        # 计算领域范围半径
        R2=(int)(((float)(self.radius)*(1.0-times)/2.0))+1
        # 计算节点距离
        outer=Node(R2,R2)
        center=Node(0,0)
        d_normalize=self.distance(center,outer)
        print u"radius:",R2,u"d_normalize:",d_normalize
        for i in range(-R2,R2+1):
            for j in range(-R2,R2+1):
                # 半径范围内的节点
                if j+bmu_loc.Y >= 0 and j+bmu_loc.Y < self.height and i+bmu_loc.X >= 0 and i+bmu_loc.X < self.width:
                    # 计算到中心点的距离并归一化
                    outer=Node(i,j)
                    distance=self.distance(center,outer)
                    distance/= d_normalize
                    # 度量学习率
                    t=(float)(exp(-1.0*distance**2/0.15))
                    # 计算随迭代次数减少的程度
                    t/=(times*4.0+1.0)
                    # 更新值
                    self.nodes[i+bmu_loc.X][j+bmu_loc.Y].R = int(self.nodes[i+bmu_loc.X][j+bmu_loc.Y].R*(1-t) + r_sample[0]*t)
                    self.nodes[i+bmu_loc.X][j+bmu_loc.Y].G = int(self.nodes[i+bmu_loc.X][j+bmu_loc.Y].G*(1-t) + r_sample[1]*t)
                    self.nodes[i+bmu_loc.X][j+bmu_loc.Y].B = int(self.nodes[i+bmu_loc.X][j+bmu_loc.Y].B*(1-t) + r_sample[2]*t)

        # 输出图像
        # self.save_image(str((int)(100*times)))
        self.save_image("result_2")
        sleep(1)
    # 保存图像
    def save_image(self, imagename):
        newImage = Image.new ("RGBA", (self.width,self.height), (0,0,0))
        newpix = newImage.load()
        for i in range(self.width):
            for j in range(self.height):
                newpix[i,j] = (self.nodes[i][j].R,self.nodes[i][j].G,self.nodes[i][j].B,255)
        newImage.save("data\\result_image\\"+imagename+".jpg")

#----------- 程序的入口处 -----------
    
if __name__ == "__main__":
    
    print u""" 
--------------------------------------------------------
    程序：SOM图片生成程序 
    作者：DiamonJoy 
    日期：2015-11-24
    语言：Python 2.7 
-------------------------------------------------------- 
    """    
    print u'请按下回车开始程序'
    raw_input(' ')
    
    print u"1.读入测试图片中..."
    # 测试图片
    myimage = Image.open('data\\source_image\\2.jpg')
    # 图片尺寸
    myimage_with = myimage.size[0]
    myimage_height = myimage.size[1]
    print u"image_with:",myimage_with,u"image_height:",myimage_height
    print u""
    # 读入图片像素值
    mypix = myimage.load()
    print u"2.训练中..."
    # Som训练
    mySom = SOM(myimage_with,myimage_height)
    # 当前迭代次数，对于邻域和学习率有影响
    times=0.0
    # 最大迭代次数
    MAX_ITER=100
    # 次数增加幅度
    T_INC=1.0/(float)(MAX_ITER)
    # print T_INC
    # 循环迭代
    while(True):
        
        if times<1.0:

            # 获取随机样本
            random_x=randint(0,myimage_with-1)
            random_y=randint(0,myimage_height-1)
            r_sample=mypix[random_x,random_y]
            # 获取最优竞争者
            bmu_loc=mySom.get_bmu(r_sample)
            print u"-----------"+str(int(100*times))+u"%"+u"-----------"
            print u"sample.x:",random_x,u"sample.y:",random_y,u"sample.R:",r_sample[0],u"sample.G:",r_sample[1],u"sample.B:",r_sample[2]
            print u"bmu.x:",bmu_loc.X,u"bmu.y:",bmu_loc.Y,u"bmu.R:",bmu_loc.R,u"bmu.G:",bmu_loc.G,u"bmu.B:",bmu_loc.B
            # 更新领域值
            mySom.scale_neighbors(bmu_loc,r_sample,times)
            print u""
            # 更新当前迭代次数
            times+=T_INC
            
        else:
            print u"-----------"u"100%"+u"-----------"
            print u"程序结束"
            break

