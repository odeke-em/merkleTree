#!/usr/bin/env python3
# Author: Emmanuel Odeke <odeke@ualberta.ca>

import random, hashlib

import BaseNodeUtil

getParent = lambda i: (i-1)>>1

hashCompile = lambda *args: hashlib.md5(*args).hexdigest()

def conjoinHash(itemIter, hashFunc=hashCompile):
    return hashFunc(bytes(''.join(itemIter), **BaseNodeUtil.encodingArgs))

class ObjHit:
    def __init__(self, maxHits=2, onThresholdOverflow=conjoinHash):
        self.__maxHits = maxHits or 2
        assert(self.__maxHits >= 1)

        self.__result = ''
        self.__itemTuple = ()

        self.__onThresholdOverflow = onThresholdOverflow

    def addItem(self, item):
        self.__itemTuple += (item,)
        if len(self.__itemTuple) >= self.__maxHits:
            self.compileResult()

    def compileResult(self):
        self.__result = self.__onThresholdOverflow(self.__itemTuple)
        self.__itemTuple = (self.__result,)
        return self.__result

    def getResult(self):
        return self.__result

def levelized(levelList):
    lLen = len(levelList)
    if lLen < 1:
        return [None]
    elif lLen == 1:
        return [levelList[0].getCheckSum()]
    
    objHitDict = {}
    maxParent = 0
    for i in range(lLen-1, 0, -1): # Not including '0' since it is always the root
        parent = getParent(i)
        if parent >= maxParent:
            maxParent = parent

        pItem = levelList[parent]
        objHitDict.setdefault(parent, ObjHit(maxHits=2)).addItem(pItem.getCheckSum())

    # Ordering contains consecutive indices
    ordering = []

    for i in range(maxParent + 1):
        objHit = objHitDict[i]
        retrHash = objHit.getResult()
        if not retrHash:
            retrHash = objHit.compileResult()

        ordering.append(retrHash)

    return ordering

def main():
    minCkSize, maxCkSize = 0, 1035872739

    chunks = []
    chunkCount = random.randint(0, 229)

    for i in range(chunkCount):
        ckSize = random.randint(minCkSize, maxCkSize)
        chunks.append(dict(
            ckSize=ckSize, ckSum=hashlib.md5(
                bytes('%s%s%s'%(i, ckSize, chunkCount), **BaseNodeUtil.encodingArgs)
            ).hexdigest()
        ))

    levelNList = BaseNodeUtil.initialLevelize(chunks)

    print(levelized(levelNList))

if __name__ == '__main__':
    main()
