"""
@author: liukun
@date: 2020-05-26
@desc: 单元测试
"""
from lru import LRU

def test_adddata_01():
    lru_obj=LRU(2)
    lru_obj.put(1, 2)
    assert lru_obj.get(1)==2

def test_updatedata_02():
    lru_obj=LRU(2)
    lru_obj.put(1, 2)
    assert lru_obj.get(1)==2
    lru_obj.put(1, 3)
    assert lru_obj.get(1)==3
def test_limit_03():
    lru_obj=LRU(2)
    lru_obj.put(1, 2)
    lru_obj.put(2, 3)
    lru_obj.put(3, 4)
    assert lru_obj.get(3)==4

def test_len0_04():
    lru_obj=LRU(2)
    assert lru_obj.get(4)=='-1'

def test_missdata_05():
    lru_obj=LRU(2)
    lru_obj.put(1, 2)
    lru_obj.put(2, 3)
    lru_obj.put(3, 4)
    assert lru_obj.get(1)=='-1'

def test_missdata_06():
    lru_obj=LRU(2)
    lru_obj.put(1, 2)
    lru_obj.put(2, 3)
    lru_obj.put(3, 4)
    assert lru_obj.get(7)=='-1'

def test_put_path_01():
    lru_obj=LRU(2)
    lru_obj.put(1, 2)
    lru_obj.put(2, 4)
    assert lru_obj.data_list.head.next.value==4

def test_put_path_02():
    lru_obj=LRU(2)
    lru_obj.put(1, 2)
    lru_obj.put(2, 4)
    lru_obj.put(3, 5)
    assert lru_obj.data_list.head.next.value==5
    assert lru_obj.data_list.head.next.next.value==4 # 第二个元素
    assert lru_obj.data_list.head.next.next.next== lru_obj.data_list.end # 之后就是最后一个结束节点了.
    assert (1 in lru_obj.cache_dict)==False # 数据也从字典中删除了.

def test_put_path_03():
    """
    见readme.md
    """
    lru_obj=LRU(2)
    lru_obj.put(1, 2)
    assert lru_obj.data_list.head.next.value==2
    lru_obj.put(2, 4)
    assert lru_obj.data_list.head.next.value==4

def test_get_path_01():
    lru_obj=LRU(2)
    lru_obj.put(1, 2)
    assert lru_obj.get(1)==2

def test_get_path_02():
    lru_obj=LRU(2)
    lru_obj.put(1, 2)
    assert lru_obj.get(2)=='-1'


def test_other_except_07():
    """
    测试LRU的长度不正确时,系统的表现
    """
    import pytest
    lru_obj=LRU(-1)
    with pytest.raises(AttributeError) as e:
        "E               AttributeError: 'NoneType' object has no attribute 'key'"
        lru_obj.put(1, 2)
    print()


