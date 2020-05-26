"""
@author: liukun
@date: 2020-05-26
@desc: 性能测试
"""

import time 
import random
from lru import LRU

def get_random_int(beg,end,limit=50000):
    random_data=[]
    i=0
    while i<limit:
        value=random.randint(beg, end)
        random_data.append(value)
        i=i+1
    return random_data
    

def random_wirte(lru_len=100,times=20000):
    """
    [测试随机写操作]

    Keyword Arguments:
        times {int} -- [本轮测试次数] (default: {20000})
    """
    key_list=get_random_int(0,1500,times)
    lru_obj=LRU(lru_len) 
    beg_time=time.time()
    for key in key_list:
        lru_obj.put(key,key)
    end_time=time.time()
    print("测试随机写操作{}次,lru_len长度为{},情况下耗时{} ".format(times,lru_len,end_time-beg_time))
    time.time()

def random_read(lru_len=100,times=20000):
    key_list=get_random_int(0,1500,times)
    lru_obj=LRU(lru_len) 
    for key in key_list:
        lru_obj.put(key,key)
    beg_time=time.time()
    for key in key_list:
        lru_obj.get(key)
    end_time=time.time()
    print("测试随机读操作{}次,lru_len长度为{},情况下耗时{} ".format(times,lru_len,end_time-beg_time))
    time.time()
 

def random_read_write(lru_len=100,times=20000):
    """
    随机读写
    """
    key_list=get_random_int(0,1500,times)
    lru_obj=LRU(lru_len) 

    beg_time=time.time()
    for index,key in  enumerate(key_list):
        if index%2==0:
            lru_obj.put(key,key)
        else:
            lru_obj.get(key)
    end_time=time.time()
    print("测试随机读写操作{}次,lru_len长度为{},情况下耗时{} ".format(times,lru_len,end_time-beg_time))
    time.time()

if __name__ == "__main__":
    hello=get_random_int(0,1500,limit=200)
    #print(hello)
    lru_len=500
    times=2000000
    random_wirte(lru_len,times)
    random_read(lru_len,times)
    random_read_write(lru_len,times)