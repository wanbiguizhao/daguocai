
"""
@author: liukun
@date: 2020-05-26
@desc: 简单的LRU缓存

"""
from typing import List

class Node:
    key : int 
    value : int 
    next  = None
    prev  = None 
    def __init__(self,k,v):
        self.key=k
        self.value=v 
    
    def __repr__(self):
        return "key->{} value->{} ".format(self.key,self.value)

class DoubleList:
    head:Node 
    end:Node 
    LEN: int 
    def __init__(self):
        head = Node(-1,-1)
        end = Node(-1,-1)
        head.next = end
        head.prev = None
        end.prev = head
        end.next = None
        self.head = head
        self.end = end
        self.LEN=0

    def addNode(self, x:Node):
        x.next = self.head.next 
        self.head.next.prev = x
        x.prev = self.head 
        self.head.next = x
        self.LEN = self.LEN+1 

    def removeNode(self):
        if self.LEN>0:
            del_node=self.end.prev
            self.end.prev=del_node.prev
            del_node.prev.next = self.end
            self.LEN = self.LEN - 1
            return del_node

    def hitNode(self, x : Node):
        pre_node= x.prev
        next_node=x.next
        pre_node.next = next_node
        next_node.prev = pre_node
        # 放到头结点上
        x.next = self.head.next 
        self.head.next.prev = x
        x.prev = self.head 
        self.head.next = x

class LRU:
    data_list:DoubleList 
    cache_dict:dict

    def __init__(self,max_len=5):
        self.data_list=DoubleList()
        self.cache_dict={}
        if max_len<1:
            print("max_len 必须大于等于1, 将max_len=1")
            # max_len=1
        self.MAX_LEN = max_len # 最大长度
        

    def put(self,key,value):
        if key in self.cache_dict:
            node=self.cache_dict[key] # 索引
            node.value=value
            self.data_list.hitNode(node)# 写操作,缓存放在第一位.
        else:
            # 删除node
            while len(self.cache_dict)>= self.MAX_LEN :
                node=self.data_list.removeNode()
                del self.cache_dict[node.key] # 删除节点
                del node # 释放node
            new_node=Node(key,value)
            self.cache_dict[key]=new_node
            self.data_list.addNode(new_node)

    def get(self,key):
        if key in self.cache_dict:
            node=self.cache_dict[key]
            self.data_list.hitNode(node)
            return node.value
        return "-1"


if __name__ == "__main__":
    node1=Node(1,2)
    print(node1)
    node2=Node(3,4)
    print(node2)
    dnl=DoubleList()
    dnl.addNode(node1)
    dnl.addNode(node2)
    lr=LRU(max_len=2)
    lr.put(1,4)
    lr.put(2,5)
    print(lr.cache_dict)
    lr.put(3,4)
    
    print(lr.cache_dict)
    print(lr.get(3))
    print(lr.get(10))

