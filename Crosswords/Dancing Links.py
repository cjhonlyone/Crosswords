# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 22:02:04 2017

@author: caojiahui
"""

#Dancing Links
import Crosswords
import numpy
import time
numpy.set_printoptions(threshold=numpy.nan)
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
                
tCrosswords1 = [[0,0,0,7,5,0,0,0,0],
                [0,3,0,0,4,8,0,2,0],
                [1,0,0,0,0,0,0,0,6],
                [0,4,0,0,0,0,0,0,8],
                [7,9,0,0,0,0,0,3,1],
                [2,0,0,0,0,0,0,7,0],
                [5,0,0,0,0,0,0,0,7],
                [0,8,0,3,2,0,0,4,0],
                [0,0,0,0,6,9,0,0,0]]

tCrosswords2 = [[0,1,8,0,0,0,7,0,0],
                [0,0,0,3,0,0,2,0,0],
                [0,7,0,0,0,0,0,0,0],
                [0,0,0,0,7,1,0,0,0],
                [6,0,0,0,0,0,0,4,0],
                [3,0,0,0,0,0,0,0,0],
                [4,0,0,5,0,0,0,0,3],
                [0,2,0,0,8,0,0,0,0],
                [0,0,0,0,0,0,0,6,0]]       


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
    for i in range(rows):
        temp = []
        for j in range(cols):
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
                    if ((cnt == th1) | (cnt == th2) | (cnt == th3) | (cnt == th4)):
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
                        if ((cnt == th1) | (cnt == th2) | (cnt == th3) | (cnt == th4)):
                            temp.append(1)
                        else:
                            temp.append(0)                    
                    matrix.append(temp)
    return matrix
                
            

def dance(dlinks,k):
    RIGHT = dlinks[0].right
    if RIGHT == 0:
        return True  
    if isnosolution(dlinks):
        return False    
    remove(dlinks[RIGHT].col+1, dlinks)
    down = dlinks[RIGHT].down
    while(down != RIGHT):
        ans.append(dlinks[down].row)
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
            
                
if __name__ == '__main__':
    start = time.time()
#    逻辑求解
    [tCrosswords,count,GRID] = Crosswords.solve(tCrosswords2)
#    dancinglinks 求解
    matrix = gm(tCrosswords, GRID)
    print(len(matrix),len(matrix[0]))
    [dlinks, cols] = gdl(matrix)
    ans = []
    dance(dlinks, 0)
    end = time.time()
#    根据矩阵逆向求数独解
    for cnt in ans:
        count = 0
        temp = []
        for item in matrix[cnt-1]:
            if item == 1:
                temp.append(count)
            count = count + 1
        temp[3] = temp[3] - 243
        temp[2] = temp[2] - 162
        temp[1] = temp[1] - 81
        i = int((temp[0] - temp[1] + 9*temp[3])/90)
        j = int((temp[1] - temp[0] + temp[3])/10)
        num = int((9*temp[0] + temp[1] - 9*temp[3])/10 + 1)
        tCrosswords[i][j] = num
    print(numpy.array(tCrosswords))
    print('用时%s'%(end - start))
        
