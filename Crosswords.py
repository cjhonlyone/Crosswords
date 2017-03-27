# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 15:59:49 2017

@author: caojiahui
"""
#import numpy
#numpy.set_printoptions(threshold=numpy.nan)


#solve Sudoku Crosswords
#tCrosswords =  [[2,0,0,7,0,0,8,3,0],
#                [0,9,0,0,8,0,0,0,0],
#                [8,0,0,0,0,0,6,0,2],
#                [0,6,9,3,7,0,0,0,1],
#                [0,0,0,0,9,0,0,0,0],
#                [3,0,0,0,5,8,9,7,0],
#                [9,0,1,0,0,0,0,0,3],
#                [0,0,0,0,3,0,0,1,0],
#                [0,3,8,0,0,7,0,0,9]]
                
#tCrosswords =  [[2 ,0 ,0 ,7 ,0 ,9 ,8 ,3 ,0],
#                [0 ,9 ,0 ,0 ,8 ,0 ,1 ,0 ,7],
#                [8 ,0 ,0 ,0 ,0 ,0 ,6 ,9 ,2],
#                [0 ,6 ,9 ,3 ,7 ,0 ,0 ,8 ,1],
#                [0 ,8 ,0 ,0 ,9 ,0 ,3 ,0 ,0],
#                [3 ,0 ,0 ,0 ,5 ,8 ,9 ,7 ,0],
#                [9 ,0 ,1 ,8 ,0 ,0 ,0 ,0 ,3],
#                [0 ,0 ,0 ,9 ,3 ,0 ,0 ,1 ,8],
#                [0 ,3 ,8 ,0 ,0 ,7 ,0 ,0 ,9]]

#tCrosswords =  [[2 ,1 ,0 ,7 ,6 ,9 ,8 ,3 ,0],
#                [0 ,9 ,0 ,2 ,8 ,3 ,1 ,0 ,7],
#                [8 ,7 ,3 ,5 ,4 ,1 ,6 ,9 ,2],
#                [5 ,6 ,9 ,3 ,7 ,0 ,0 ,8 ,1],
#                [1 ,8 ,7 ,0 ,9 ,0 ,3 ,0 ,0],
#                [3 ,0 ,0 ,1 ,5 ,8 ,9 ,7 ,6],
#                [9 ,0 ,1 ,8 ,2 ,0 ,7 ,0 ,3],
#                [7 ,0 ,0 ,9 ,3 ,0 ,0 ,1 ,8],
#                [0 ,3 ,8 ,0 ,1 ,7 ,0 ,0 ,9]]
#[[2 1 5 7 6 9 8 3 4]
# [4 9 6 2 8 3 1 5 7]
# [8 7 3 5 4 1 6 9 2]
# [5 6 9 3 7 4 2 8 1]
# [1 8 7 6 9 2 3 4 5]
# [3 2 4 1 5 8 9 7 6]
# [9 4 1 8 2 5 7 6 3]
# [7 5 2 9 3 6 4 1 8]
# [6 3 8 4 1 7 5 2 9]]

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
        
        
def solve(Crosswords):
    '''init'''
    count = 0
    GRID = []
    for i in range(1, 10):
        row = []
        for j in range(1, 10):
            row = row + [grid(i,j)]
        GRID.append(row)    
    for item in Crosswords:
        count = count + item.count(0)                           
    '''solve'''
    cnt = 0
    lastcount = 0
    while(True):
        if count == 0:
            break;          
        for i in range(0, 9):
            for j in range(0, 9):  
                if Crosswords[i][j] != 0:
                    continue               
                '''a'''
                lenset = GRID[i][j].updatealter(Crosswords)
                if lenset == 1:
                    Crosswords[i][j] = GRID[i][j].getalter()
                    count = count - 1   
                    continue
                '''b'''    
                if cnt != 0:   
                    i0 = int(i/3) * 3
                    j0 = int(j/3) * 3
                    com = set([1,2,3,4,5,6,7,8,9])
                    for ix in range(i0,i0+3):
                        for jx in range(j0,j0+3):
                            if (Crosswords[ix][jx] != 0) | ((ix == i) & (jx == j)):
                                continue
                            com =  com & (GRID[i][j].getallalter() - GRID[ix][jx].getallalter())        
                    if len(com) == 1:
                        for item in com:
                            Crosswords[i][j] = item
                            count = count - 1  
                        continue
         
                    com = set([1,2,3,4,5,6,7,8,9])        
                    for jx in range(0,9):
                        if (Crosswords[i][jx] != 0) | (jx == j):
                            continue
                        com =  com & (GRID[i][j].getallalter() - GRID[i][jx].getallalter())
                    if len(com) == 1:
                        for item in com:
                            Crosswords[i][j] = item
                            count = count - 1   
                        continue 
             
                    com = set([1,2,3,4,5,6,7,8,9])        
                    for ix in range(0,9):
                        if (Crosswords[ix][j] != 0) | (ix == i):
                            continue
                        com =  com & (GRID[i][j].getallalter() - GRID[ix][j].getallalter())
                    if len(com) == 1:
                        for item in com:
                            Crosswords[i][j] = item
                            count = count - 1   
                        continue 
                    
        if cnt != 0:                                           
            if count == lastcount:
                break
            lastcount = count
        cnt = cnt + 1                                                                                     
    return [Crosswords, count]            
#        for i0 in range(3):
#            for j0 in range(3):
#                i = i0 * 3
#                j = j0 * 3
#                temp = set()
#                allcom = set()
#                rowcom = []
#                columncom = [set(), set(), set()]
#                             
#                for ix in range(i,i+3):
#                    ccount = 0
#                    for jx in range(j,j+3):
#                        ccount = ccount + 1 
#                        if (Crosswords[ix][jx] != 0):
#                            continue
#                        allcom =  allcom | GRID[ix][jx].getallalter()
#                        temp = temp | GRID[ix][jx].getallalter()
#                        columncom[ccount-1] = columncom[ccount-1] | GRID[ix][jx].getallalter()
#                    rowcom.append(temp)
#                    temp = set()
##                print(allcom)    
##                print(rowcom)
##                print(columncom)
##                print("######")
#                for item in allcom: 
#                    if ((item in rowcom[0]) & (item not in rowcom[1]) & (item not in rowcom[2])):
#                        for jx in (index-set(list(range(j,j+3)))):
#                            if (Crosswords[i][jx] != 0):
#                                continue 
#                            GRID[i][jx].alter = GRID[i][jx].alter - set([item])
#                    elif ((item not in rowcom[0]) & (item in rowcom[1]) & (item not in rowcom[2])):
#                        for jx in (index-set(list(range(j,j+3)))):
#                            if (Crosswords[i+1][jx] != 0):
#                                continue 
#                            GRID[i+1][jx].alter = GRID[i+1][jx].alter - set([item])                    
#                    elif ((item not in rowcom[0]) & (item not in rowcom[1]) & (item in rowcom[2])):
#                        for jx in (index-set(list(range(j,j+3)))):
#                            if (Crosswords[i+2][jx] != 0):
#                                continue 
#                            GRID[i+2][jx].alter = GRID[i+2][jx].alter - set([item])     
#                            
#                    if ((item in columncom[0]) & (item not in columncom[1]) & (item not in columncom[2])):
#                        for ix in (index-set(list(range(i,i+3)))):
#                            if (Crosswords[ix][j] != 0):
#                                continue 
#                            GRID[ix][j].alter = GRID[ix][j].alter - set([item])   
#                    elif ((item not in columncom[0]) & (item in columncom[1]) & (item not in columncom[2])):
#                        for ix in (index-set(list(range(i,i+3)))):
#                            if (Crosswords[ix][j+1] != 0):
#                                continue 
#                            GRID[ix][j+1].alter = GRID[ix][j+1].alter - set([item])                            
#                    elif ((item not in columncom[0]) & (item not in columncom[1]) & (item in columncom[2])):
#                        for ix in (index-set(list(range(i,i+3)))):
#                            if (Crosswords[ix][j+2] != 0):
#                                continue 
#                            GRID[ix][j+2].alter = GRID[ix][j+2].alter - set([item])      
                            
        
    
     
if __name__ == '__main__':  
    ans = solve(tCrosswords)
    print(numpy.array(ans[0]))
    print('%d grids left' %ans[1])
    

