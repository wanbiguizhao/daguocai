
"""
@author: liukun
@date: 2020-05-26
@desc: 简单的LRU缓存,增加日志版本

"""
from typing import List
from sys import stdout
from eliot import start_action,log_call, to_file
to_file(stdout)
to_file(open("eliot.log", "ab"))

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

    def jsonify(self):
        return {
            "key":self.key,
            "value": self.value,
        }
    
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
        with start_action(action_type=u"addNode", add_node=x.jsonify()):
            x.next = self.head.next 
            self.head.next.prev = x
            x.prev = self.head 
            self.head.next = x
            self.LEN = self.LEN+1

    def removeNode(self):
        with start_action(action_type=u"removeNode") as action:
            if self.LEN>0:
                del_node=self.end.prev
                self.end.prev=del_node.prev
                del_node.prev.next = self.end
                self.LEN = self.LEN - 1
                action.log(message_type="del_node_info",node=del_node.jsonify())
                return del_node
    #@log_call(action_type="hitNode"  , include_args=["x"])
    def hitNode(self, x : Node):
        with start_action(action_type=u"hitNode", add_node=x.jsonify()):
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
        
    @log_call(action_type="put" , include_args=["key","value"] )
    def put(self,key,value):
        if key in self.cache_dict:
            node=self.cache_dict[key] # 索引
            with start_action(action_type=u"updateNode", old_node=node.jsonify()):
                node.value=value
                self.data_list.hitNode(node)# 写操作,缓存放在第一位.
        else:
            # 删除node
            while len(self.cache_dict)>= self.MAX_LEN :
                node=self.data_list.removeNode()
                with start_action(action_type=u"delNode", old_node=node.jsonify()):
                    del self.cache_dict[node.key] # 删除节点
                    del node # 释放node
            new_node=Node(key,value)
            self.cache_dict[key]=new_node
            self.data_list.addNode(new_node)
    @log_call(action_type="get" , include_args=["key"] )
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
    lr=LRU(max_len=5)
    lr.put(1,4)
    lr.put(2,5)
    lr.put(1,5)
    lr.put(3,5)
    lr.get(1)
    print(lr.cache_dict)
    lr.put(3,4)
    print(lr.cache_dict)
    print(lr.get(3))
    print(lr.get(10))
    batch_num=20
    with start_action(action_type="batch_insert_data",batch_num=batch_num):
        for i in range(batch_num):
            lr.put(i%6, i)