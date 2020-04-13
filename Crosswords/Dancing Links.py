# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 22:02:04 2017

@author: caojiahui
"""

#Dancing Links
import Crosswords
import numpy
import time
from itertools import permutations
# numpy.set_printoptions(threshold=numpy.nan)
#tCrosswords =  [[2 ,1 ,0 ,7 ,6 ,9 ,8 ,3 ,0],
#                [0 ,9 ,0 ,2 ,8 ,3 ,1 ,0 ,7],
#                [8 ,7 ,3 ,5 ,4 ,1 ,6 ,9 ,2],
#                [5 ,6 ,9 ,3 ,7 ,0 ,0 ,8 ,1],
#                [1 ,8 ,7 ,0 ,9 ,0 ,3 ,0 ,0],
#                [3 ,0 ,0 ,1 ,5 ,8 ,9 ,7 ,6],
#                [9 ,0 ,1 ,8 ,2 ,0 ,7 ,0 ,3],
#                [7 ,0 ,0 ,9 ,3 ,0 ,0 ,1 ,8],
#                [0 ,3 ,8 ,0 ,1 ,7 ,0 ,0 ,9]]
tCrosswords =  [[2,0,0,7,0,0,8,3,0],
                [0,9,0,0,8,0,0,0,0],
                [8,0,0,0,0,0,6,0,2],
                [0,6,9,3,7,0,0,0,1],
                [0,0,0,0,9,0,0,0,0],
                [3,0,0,0,5,8,9,7,0],
                [9,0,1,0,0,0,0,0,3],
                [0,0,0,0,3,0,0,1,0],
                [0,3,8,0,0,7,0,0,9]] 
#                
#tCrosswords1 = [[0,0,0,7,5,0,0,0,0],
#                [0,3,0,0,4,8,0,2,0],
#                [1,0,0,0,0,0,0,0,6],
#                [0,4,0,0,0,0,0,0,8],
#                [7,9,0,0,0,0,0,3,1],
#                [2,0,0,0,0,0,0,7,0],
#                [5,0,0,0,0,0,0,0,7],
#                [0,8,0,3,2,0,0,4,0],
#                [0,0,0,0,6,9,0,0,0]]
#
#tCrosswords2 = [[0,1,8,0,0,0,7,0,0],
#                [0,0,0,3,0,0,2,0,0],
#                [0,7,0,0,0,0,0,0,0],
#                [0,0,0,0,7,1,0,0,0],
#                [6,0,0,0,0,0,0,4,0],
#                [3,0,0,0,0,0,0,0,0],
#                [4,0,0,5,0,0,0,0,3],
#                [0,2,0,0,8,0,0,0,0],
#                [0,0,0,0,0,0,0,6,0]]       

class grid(object):
#类初始化    
    def __init__(self, row, column):
        self.__row = row
        self.__column = column
        self.__alter = set([1,2,3,4,5,6,7,8,9])
#遍历行        
    def traverserow(self, Crosswords):        
        return set(Crosswords[self.__row - 1])
#遍历列          
    def traversecolumn(self, Crosswords):     
        return set(list(map(lambda x: Crosswords[x][self.__column - 1], range(0,9))))
#遍历宫
    def traversebiggrid(self, Crosswords):
        i = int((self.__row-1)/3) * 3
        j = int((self.__column-1)/3) * 3
        x=[]
        for cnt in range(i, i+3):
            x = x + list(Crosswords[cnt][j:j+3]) 
        return set(x)
#根据遍历结果更新备选元素并返回集合长度        
    def updatealter(self, Crosswords):
        newalter = self.traversebiggrid(Crosswords) | self.traversecolumn(Crosswords) | self.traverserow(Crosswords)
        newalter.remove(0)
        self.__alter = self.__alter - newalter
        return len(self.__alter)
#返回所有备选元素                                                       
    def getallalter(self):
        return self.__alter
#返回首个备选元素        
    def getalter(self):
        for items in self.__alter:
            item = items
        return item

class node():
    def __init__(self, up, down, left, right, row, col, cnt):
        
        self.up = up
        self.down = down
        self.left = left        
        self.right = right
        
        self.row = row
        self.col = col
        
        self.cnt = cnt
        
        
#generate dancing links      
def gdl(matrix):
    rows = len(matrix)  
    cols = len(matrix[0])
    head = node(0,0,cols,1,0,0,0)
    dlinks = [head]
    for j in range(cols):
        if j != (cols - 1):
            dlinks.append(node(0,0,j,j+2,0,j,j+1))
        else:
            dlinks.append(node(0,0,j,0,0,j,j+1))
    count = cols 
    for i in range(rows):
        for j in range(cols):
            if matrix[i][j] == 0:
                continue
            count = count + 1
            dlinks.append(node(count,count,count,count,i+1,j,count))
    '''horizontal links'''        
    count = cols 
    for i in range(rows): #行
        temp = []
        for j in range(cols): #列
            if matrix[i][j] == 0:
                continue
            count = count + 1 
            temp.append([i,j,count])
        dlinks[temp[0][2]].left = temp[-1][2]
        dlinks[temp[-1][2]].right = temp[0][2]
        length = len(temp)
        for num in range(0,length):            
            if num != 0:
                dlinks[temp[num][2]].left = temp[num-1][2]
            if num != (length - 1):
                dlinks[temp[num][2]].right = temp[num+1][2]
    '''vertical links'''
    temp = []
    count = cols
    for i in range(rows):        
        for j in range(cols):
            if i == 0:  
                temp.append([])
            if matrix[i][j] == 0:
                continue
            count = count + 1
            temp[j].append([i,j,count])
    for j in range(cols): 
        if temp[j] == []:
            print('no')
            return
        dlinks[j+1].up = temp[j][-1][2]
        dlinks[j+1].down = temp[j][0][2]
        dlinks[temp[j][0][2]].up = j+1
        dlinks[temp[j][-1][2]].down = j+1
        length = len(temp[j])
        for num in range(0,length):
            if num != 0:
                dlinks[temp[j][num][2]].up = temp[j][num-1][2]
            if num != (length - 1):
                dlinks[temp[j][num][2]].down = temp[j][num+1][2] 
    return [dlinks, cols]

    
#generate matrix    
def gm(tCrosswords, GRID): 
    matrix = []      
    rows = len(tCrosswords)  
    cols = len(tCrosswords[0])    
    for i in range(rows):
        for j in range(cols):
            i0 = int(i/3)
            j0 = int(j/3)            
            if tCrosswords[i][j] != 0:
                temp = []
                th1 = 9*i + tCrosswords[i][j] - 1
                th2 = 9*j + tCrosswords[i][j] - 1 + 81
                th3 = 9*(3*i0 + j0) + tCrosswords[i][j] - 1 + 162
                th4 = 9*i + j + 243
                for cnt in range(324):
                    if ((cnt == th1) or (cnt == th2) or (cnt == th3) or (cnt == th4)):
                        temp.append(1)
                    else:
                        temp.append(0)
                matrix.append(temp)
            else:
                for num1 in GRID[i][j].getallalter():
                    num = num1 - 1
                    temp = []
                    th1 = 9*i + num
                    th2 = 9*j + num + 81
                    th3 = 9*(3*i0 + j0) + num + 162
                    th4 = 9*i + j + 243
                    for cnt in range(324):
                        if ((cnt == th1) or (cnt == th2) or (cnt == th3) or (cnt == th4)):
                            temp.append(1)
                        else:
                            temp.append(0)                    
                    matrix.append(temp)
    return matrix
                
            
result = []
ans = []
def dance(dlinks,k):
    RIGHT = dlinks[0].right
    if RIGHT == 0:
        result.append(list(ans))
        return False  
    if isnosolution(dlinks):
        return False    
    remove(dlinks[RIGHT].col+1, dlinks)
    down = dlinks[RIGHT].down
    while(down != RIGHT):
        ans.append(dlinks[down].row)
#        print(ans)
        right = dlinks[down].right
        while(right != down):  
            remove(dlinks[right].col+1, dlinks)
            right = dlinks[right].right
        if dance(dlinks, k+1):
            return True
        left = dlinks[down].left
        while(left != down):  
            resume(dlinks[left].col+1, dlinks)
            left = dlinks[left].left
        ans.pop()
        down = dlinks[down].down        
    resume(dlinks[RIGHT].col+1, dlinks)
    return False
            
            
def remove(col, dlinks):
    dlinks[dlinks[col].left].right = dlinks[col].right
    dlinks[dlinks[col].right].left = dlinks[col].left
    down = dlinks[col].down
    while(down != col):
        right = dlinks[down].right
        while(right != down):
            dlinks[dlinks[right].down].up = dlinks[right].up
            dlinks[dlinks[right].up].down = dlinks[right].down
            right = dlinks[right].right
        down = dlinks[down].down
    
    
def resume(col, dlinks):
    dlinks[dlinks[col].left].right = col
    dlinks[dlinks[col].right].left = col
    up = dlinks[col].up
    while(up != col):
        left = dlinks[up].left
        while(left != up):
            dlinks[dlinks[left].down].up = left
            dlinks[dlinks[left].up].down = left
            left = dlinks[left].left
        up = dlinks[up].up    
        
        
def sum_d(dlinks):
    count = 0
    count_cols = 0
    right = dlinks[0].right 
    while(True):
        down = right
        while(True):
            count = count + 1
            if dlinks[down].down != right:
                down = dlinks[down].down
            else:
                break
        count_cols = count_cols + 1
        if dlinks[right].right != 0:
            right = dlinks[right].right
        else:
            break
    return [count, count_cols]

    
def isnosolution(dlinks):
    right = dlinks[0].right 
    while(True):
        if dlinks[right].down == right:
            return True
        right = dlinks[right].right
        if right == 0:
            return False
            
  
def print_dlinks(dlinks):
#    firstnode = dlinks[0].right
    node_ = dlinks[0].right
    while True:
        if (node_+1) != dlinks[node_].right:
            print('0 ',end='')
        else:
            print('1 ',end='')
        if node_ == dlinks[node_].right:
            break
        else:
            node_ = dlinks[node_].right
        
        
    
            
list1 = []
def SumOfkNumber(sumN, n, list_, k, c1):
    #递归出口
    if ((n <= 0) or (sumN <= 0)):
        return
    #输出找到的结果
    if (sumN == n) and (len(list1) == (k-1)):
        if (n == 1 and c1 == True) or (n != 1 and c1 == False):
            list1.append(n)
            list_.append(list(list1))
    #        for i in range(len(list1)):
    #            print(list1[i],end='')
    #            if (i != (len(list1)-1)):
    #                print(',',end='')
    #        print('\n',end='')
            list1.pop()
    list1.append(n)      #典型的01背包问题
    SumOfkNumber(sumN - n, n - 1, list_, k, c1)  #“放”n，前n-1个数“填满”sum-n
    list1.pop()
    SumOfkNumber(sumN, n - 1, list_, k, c1)    #不“放”n，n-1个数“填满”sum

#SumOfkNumber(5,4)
def delet_listrol(list_, k):
    if (list_ == []):
        return
    for kk in k:
        list_array = numpy.array(list_)
        [m, n] = numpy.where(list_array == kk)
        m = m.tolist()
        m.reverse()
        for mm in m: 
            list_.pop(mm)
        
if __name__ == '__main__':
#    start = time.time()
#    逻辑求解
#    [tCrosswords,count,GRID] = Crosswords.solve(tCrosswords)
#    tCrosswords = tCrosswords1;
#    GRID = []
#    for i in range(1, 10):
#        row = []
#        for j in range(1, 10):
#            row = row + [grid(i,j)]
#        GRID.append(row)    

#    dancinglinks 求解
#    matrix = gm(tCrosswords, GRID)
#    matrix = [[0,1,0,1],[1,0,0,1],[1,0,1,0],[1,0,0,0],[0,0,1,0]]
#    print(len(matrix),len(matrix[0]))
#    [dlinks, cols] = gdl(matrix)
#    ans = []
#    dance(dlinks, 0)
#    end = time.time()
##    根据矩阵逆向求数独解
#    for cnt in ans:
#        count = 0
#        temp = []
#        for item in matrix[cnt-1]:
#            if item == 1:
#                temp.append(count)
#            count = count + 1
#        temp[3] = temp[3] - 243
#        temp[2] = temp[2] - 162
#        temp[1] = temp[1] - 81
#        i = int((temp[0] - temp[1] + 9*temp[3])/90)
#        j = int((temp[1] - temp[0] + temp[3])/10)
#        num = int((9*temp[0] + temp[1] - 9*temp[3])/10 + 1)
#        tCrosswords[i][j] = num
#    print(numpy.array(tCrosswords))
#    print('用时%s'%(end - start))
    
    list25_3 = []
    list_7 = []
    SumOfkNumber(25,23, list25_3, 3, False)
    SumOfkNumber(51,23, list_7, 7, True)
    delet_listrol(list25_3,[5])
    delet_listrol(list_7,[5])


    list25_3_permutations = []
    cnt = 0
    for list_mm in list25_3:
        for list_tt in list(permutations(list_mm)):
            list25_3_permutations.append(list(list_tt))
    for list_tt in list25_3_permutations:
        list_3_1 = []
        list_2_1 = []
        list_2_2 = []
        list_2_3 = []
        list_3_2 = []
        SumOfkNumber(51-5,23, list_3_1, 3, False)
        SumOfkNumber(51-5-list_tt[0],23, list_2_1, 2, False)
        SumOfkNumber(51-list_tt[0]-list_tt[1],23, list_2_2, 2, False)
        SumOfkNumber(51-list_tt[1]-list_tt[2],23, list_2_3, 2, False)
        SumOfkNumber(51-list_tt[2],23, list_3_2, 3, False)
        deletelement = list(list_tt)
        deletelement.append(5)
        delet_listrol(list_3_1,deletelement)
        delet_listrol(list_2_1,deletelement)
        delet_listrol(list_2_2,deletelement)
        delet_listrol(list_2_3,deletelement)
        delet_listrol(list_3_2,deletelement)
        if ((list_2_1==[]) or (list_2_2==[]) 
            or (list_2_3==[]) or (list_3_2==[]) or (list_3_1==[])):
            continue
        else:
            dmat = []
            for list_tmp in list_3_1:
                tmp = numpy.zeros([29],dtype = 'int8').tolist()
                tmp[list_tmp[0]-1] = 1
                tmp[list_tmp[1]-1] = 1
                tmp[list_tmp[2]-1] = 1
                tmp[23] = 1
                dmat.append(tmp)
            for list_tmp in list_2_1:
                tmp = numpy.zeros([29],dtype = 'int8').tolist()
                tmp[list_tmp[0]-1] = 1
                tmp[list_tmp[1]-1] = 1
                tmp[24] = 1
                dmat.append(tmp)          
            for list_tmp in list_2_2:
                tmp = numpy.zeros([29],dtype = 'int8').tolist()
                tmp[list_tmp[0]-1] = 1
                tmp[list_tmp[1]-1] = 1
                tmp[25] = 1
                dmat.append(tmp)   
            for list_tmp in list_2_3:
                tmp = numpy.zeros([29],dtype = 'int8').tolist()
                tmp[list_tmp[0]-1] = 1
                tmp[list_tmp[1]-1] = 1
                tmp[26] = 1
                dmat.append(tmp)   
            for list_tmp in list_3_2:
                tmp = numpy.zeros([29],dtype = 'int8').tolist()
                tmp[list_tmp[0]-1] = 1
                tmp[list_tmp[1]-1] = 1
                tmp[list_tmp[2]-1] = 1
                tmp[27] = 1
                dmat.append(tmp)         
            for list_tmp in list_7:
                tmp = numpy.zeros([29],dtype = 'int8').tolist()
                tmp[list_tmp[0]-1] = 1
                tmp[list_tmp[1]-1] = 1
                tmp[list_tmp[2]-1] = 1
                tmp[list_tmp[3]-1] = 1
                tmp[list_tmp[4]-1] = 1
                tmp[list_tmp[5]-1] = 1
                tmp[list_tmp[6]-1] = 1
                tmp[28] = 1
                dmat.append(tmp)
            tmp = numpy.zeros([29],dtype = 'int8').tolist()
            tmp[deletelement[0]-1] = 1
            tmp[deletelement[1]-1] = 1
            tmp[deletelement[2]-1] = 1
            tmp[deletelement[3]-1] = 1
            dmat.append(tmp)
            
            [dlinks, cols] = gdl(dmat)
            result = []
            ans = []
            dance(dlinks, 0)
            
            dmat = numpy.array(dmat,dtype='int8')
            for anss in result:
                print(cnt,'.',end='')
                print(deletelement)
                print('dmat',end='')
                print(dmat.shape)
                print(anss)
                for ss in anss:
                    m = numpy.where(dmat[ss-1][:] == 1)[0] + 1
                    if (m[-1] == 29):
                        list_7_show = m[0:-1].tolist()
                    elif (m[-1] == 28):
                        list_3_2_show = m[0:-1].tolist()
                    elif (m[-1] == 27):
                        list_2_3_show = m[0:-1].tolist()
                    elif (m[-1] == 26):
                        list_2_2_show = m[0:-1].tolist()
                    elif (m[-1] == 25):
                        list_2_1_show = m[0:-1].tolist()
                    elif (m[-1] == 24):
                        list_3_1_show = m[0:-1].tolist()
                    
                list_show = numpy.zeros([7,7],dtype = 'int8')
                list_show[0,1:4] = list_3_1_show
                list_show[0,0] = 5
                list_show[1:3,0] = list_2_1_show
                list_show[3,0] = deletelement[0]
                list_show[3,1:3] = list_2_2_show
                list_show[3,3] = deletelement[1]
                list_show[4:6,3] = list_2_3_show
                list_show[6,3] = deletelement[2]
                list_show[6,0:3] = list_3_2_show
                list_show[:,6] = list_7_show
                #check
                if ((sum(list_show[0,0:4]) == 51) and (sum(list_show[0:4,0]) == 51) 
                    and (sum(list_show[3,0:4]) == 51) and (sum(list_show[3:7,3]) == 51)
                    and (sum(list_show[6,0:4]) == 51) and (sum(list_show[:,6]) == 51)):
                    print(list_show)
                else:
                    print('bug')
                cnt = cnt + 1
#            break
            
#    print('有%d个'%(cnt))
    
    
    
    
    
