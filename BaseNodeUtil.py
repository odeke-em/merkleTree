#!/usr/bin/env python3
# Author: Emmanuel Odeke <odeke@ualberta.ca>

import sys
import random
import hashlib

isCallableAttr = lambda obj, attrName: hasattr(getattr(obj, attrName, None), '__call__')
encodingArgs = {}
pyVersion = sys.hexversion//(1<<24)
if pyVersion >= 3:
    encodingArgs = {'encoding': 'utf-8'}

class CheckNode:
    def __init__(self, checkSum, chunkSize, index=-1):
        self.__index = index
        self.__checkSum = checkSum
        self.__chunkSize = chunkSize

    def setIndex(self, index):
        self.__index = index

    def getIndex(self):
        return self.__index

    def getCheckSum(self):
        return self.__checkSum

    def getChunkSize(self):
        return self.__chunkSize

    def setCheckSum(self, ckSum):
        self.__checkSum = ckSum

    def setChunkSize(self, ckSize):
        self.__chunkSize = ckSize

    def __str__(self):
        return '[%s:%s:%s]'%(self.__index, self.__checkSum, self.__chunkSize)

class LevelNode:
    def __init__(self, hashAlgoName='md5'):
        self.__left = None
        self.__right = None
        self.__hashAlgoName = hashAlgoName

    def setLeftChunk(self, ckSum, ckSize, index):
        self.__left = CheckNode(checkSum=ckSum, chunkSize=ckSize, index=index)

    def setRightChunk(self, ckSum, ckSize, index):
        self.__right = CheckNode(checkSum=ckSum, chunkSize=ckSize, index=index)

    def getRightChunk(self):
        return self.__right

    def getLeftChunk(self):
        return self.__left

    def getNodeCheckSum(self, n):
        if not isCallableAttr(n, 'getCheckSum'):
            return 'NULL'

        return n.getCheckSum()

    def getCheckSum(self):
        joinedCkSum = '%s%s'%(
            self.getNodeCheckSum(self.__left), self.getNodeCheckSum(self.__right)
        )
        hashFunc = getattr(hashlib, self.__hashAlgoName, hashlib.md5)
        return hashFunc(bytes(joinedCkSum, **encodingArgs)).hexdigest()

def initialLevelize(chunkList):
    ckListLen = len(chunkList)
   
    i = 0 
    levelNodeList = []
    
    while True:
        if i >= ckListLen:
            break

        levelNode = LevelNode()
        levelNodeList.append(levelNode)

        l = chunkList[i]
        levelNode.setLeftChunk(index=i, **l)

        i += 1
        if i >= ckListLen:
            break

        r = chunkList[i]
        levelNode.setRightChunk(index=i, **r)
        i += 1

    return levelNodeList
