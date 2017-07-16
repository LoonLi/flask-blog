---
layout: post
title:  "Python numpy 教程"
date:   2017-07-16 11:49:45 +0200
categories: python
published: true
---
    就是对于http://cs231n.github.io/python-numpy-tutorial/的一个翻译总结。

### 0x00 Numpy

Numpy是python中的一个核心科学计算库，它提供了多维数组的多种计算方式，常是是其他各种库的依赖。据说与MATLAB的语法很像。那么开始使用Numpy只要在 `pip install numpy` ,之后在python源文件中：

```python
import numpy as np
```

### 0x01 array初始化

在numpy中，array是一组相同类型的数，并且以一个不可迭代的整形元组作为目录。我们可以用Python的list来初始化一个array。

```python
>>> a = np.array([1,2,3])
>>> a
array([1, 2, 3])
```

通过类的\_\_getitem()\_\_方法来获取元素，通过shape属性获得行列数。

```python
>>> a[0]
1
>>> a.shape
(3,)
```

numpy还提供了一些初始化array的函数：

```python
>>> a = np.zeros((3,4))
>>> a
array([[ 0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.]])
>>> b = np.ones((3,4))
>>> b
array([[ 1.,  1.,  1.,  1.],
       [ 1.,  1.,  1.,  1.],
       [ 1.,  1.,  1.,  1.]])
>>> c = np.full((3,4),7)
>>> c
array([[7, 7, 7, 7],
       [7, 7, 7, 7],
       [7, 7, 7, 7]])
>>> d = np.eye(3)
>>> d
array([[ 1.,  0.,  0.],
       [ 0.,  1.,  0.],
       [ 0.,  0.,  1.]])
>>> e = np.random.random((3,4))
>>> e
array([[ 0.25516012,  0.00591205,  0.62652757,  0.34553351],
       [ 0.26652228,  0.36970886,  0.00590201,  0.47514231],
       [ 0.17561344,  0.93916743,  0.58160846,  0.43681136]])
```

### 0x01 array indexing

即数组索引。数组索引有多种方式，大概是下面几种：

#### 切片

numpy的切片与python自带的list切片功能是基本相同的，需要注意的点是numpy提供了在多个维度切片的功能，比如：

```python
>>> a
array([[ 1,  2,  3,  4],
       [ 5,  6,  7,  8],
       [ 9, 10, 11, 12]])
>>> a[:2,1:3]
array([[2, 3],
       [6, 7]])
```

需要注意的是切片操作会改变array的shape，需要考虑到计算时的异常情况。

#### 整形数组索引

numpy还允许使用多个数组作为索引。比如说对于 `array[[1,2,3],[4,5,6]]` ,就相当于选取到了 `[array[1,4],array[2,5],array[3,6]` 。

```python
>>> a = np.array([[1,2], [3, 4], [5, 6]])
>>> a
array([[1, 2],
       [3, 4],
       [5, 6]])
>>> a[[0, 1, 2], [0, 1, 0]]
array([1, 4, 5])
```

#### 布尔型数组索引

如果想要选取满足某个布尔表达式的元素，那么用布尔型数组索引就对了。比方说，我想要选取数组中所有大于2的元素：

```python
>>> a = np.array([[1,2], [3, 4], [5, 6]])
>>> a
array([[1, 2],
       [3, 4],
       [5, 6]])
>>> a>2
array([[False, False],
       [ True,  True],
       [ True,  True]], dtype=bool)
>>> a[a>2]
array([3, 4, 5, 6])
```

需要注意的是布尔索引本身也是一个numpy数组。

### 0x02 数据类型

每个numpy数组中，数据类型都是唯一的，当然也是可以查看和改变的。

```python
>>> x = np.array([1, 2])
>>> x
array([1, 2])
>>> x.dtype
dtype('int32')
>>> x = np.array([1.0, 2.0])
>>> x.dtype
dtype('float64')
>>> x = np.array(x, dtype=np.int64)
>>> x.dtype
dtype('int64')
```

### 0x03 数学运算

使用numpy完成基础的矩阵运算非常简单。

```python
>>> x = np.array([[1,2],[3,4]], dtype=np.float64)
>>> y = np.array([[5,6],[7,8]], dtype=np.float64)
>>> x+y
array([[  6.,   8.],
       [ 10.,  12.]])
>>> x-y
array([[-4., -4.],
       [-4., -4.]])
>>> x*y
array([[  5.,  12.],
       [ 21.,  32.]])
>>> x/y
array([[ 0.2       ,  0.33333333],
       [ 0.42857143,  0.5       ]])
>>> np.sqrt(x)
array([[ 1.        ,  1.41421356],
       [ 1.73205081,  2.        ]])
```

需要注意的是在numpy中， `*` 并不代表矩阵相乘，而是矩阵中每个元素逐个相乘，如果需要使用矩阵相乘需要使用别的操作。

```python
>>> x
array([[ 1.,  2.],
       [ 3.,  4.]])
>>> y
array([[ 5.,  6.],
       [ 7.,  8.]])
>>> x.dot(y)
array([[ 19.,  22.],
       [ 43.,  50.]])
>>> np.dot(x,y)
array([[ 19.,  22.],
       [ 43.,  50.]])
```

numpy还提供了很多便利的计算函数。比方说可以使用 `sum()` 函数来计算矩阵所有元素，行或者列的和。其中 `axis=0` 表示计算列的和， `axis=1` 表示计算行的和。

```python
>>> x = np.array([[1,2],[3,4]])
>>> np.sum(x)
10
>>> np.sum(x,axis=0)
array([4, 6])
>>> np.sum(x,axis=1)
array([3, 7])
```

或者是使用 `T` 属性获得矩阵的转置。

```python
>>> x = np.array([[1,2], [3,4]])
>>> x
array([[1, 2],
       [3, 4]])
>>> x.T
array([[1, 3],
       [2, 4]])
```

需要注意的是对于rank为1的数组 `T` 不会做任何操作。