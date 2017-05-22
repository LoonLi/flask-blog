---
layout: post
title:  "用python写一个简单的搜索引擎"
date:   2017-05-19 11:49:45 +0200
categories: python
published: true
---
    这篇文章其实很久之前就该写了，因为东西是学校的一个我早就写完的项目，趁着还记得做个总结。

### 0x00 基本原理

如果把搜索引擎分成最简单的三部分，那就分别是 __爬虫__　，**排序算法** ，**倒排索引** 。后面的部分将对这三部分的编写做简单描述。

### 0x01 爬虫

爬虫是搜索引擎最基础，也是细节最多的部分。写起来绝对比你想象中要苦难得多。需要考虑到网页的编码，数据库的编码，网址是否有效，等等的问题。但相对来说写的思想很简单，就是从指定好的起始网页中获取url，再从这些url中获取url，直到所有的url已经爬过了或者是爬行深度到达了极限。代码大概就是下面的逻辑：

```python
def parse_url():
        soup = BeautifulSoup(html,'html.parser')
        i = 0
        for link in soup.find_all('a'):
                tdomain = None
                string =  link.get('href')
                if string == None or string == '':
                    string = '/'
                string = string.replace('\\','/')
                if string[0] == '#':
                    string = '/'
                if string[0] == '.' or '/' not in string:
                    t = os.path.split(self.url)
                    tdomain = t[0]
                    t = os.path.split(string)
                    string = t[1]
                if 'http' in string:
                    pass
                else:
                    if tdomain:
                        string = tdomain + '/' + string
                    elif string[0]!= '/':
                        string = domain+'/'+string
                    else:
                        string = domain+string
                outdegree.append(string)
                i+=1
                yield string
```

上面的代码并不能直接执行，因为是类中删减过的版本。上面的爬虫是按如下的逻辑执行的：（1）获取页面中所有的url。（2）判断url是直接寻址还是间接寻址。（3）如果是直接寻址就直接返回该url，否则返回加上当前域名的url。

对于如何获得页面的信息就不在讨论范围内了。另外关于页面去重则是另一个比较困难的问题，这篇文章也不做讨论。

补充一点就是对于url的去重使用bloomfilter是个好主意，在github也有现成的实现。

### 0x02 排序算法

对于搜索结果的排序参照的计算因素就非常多了。首先一方面会与肯定与查询词相关，比如查询词是否在标题中，是否被加粗，在文章中是否多次被提到，等等。另一方面与网站本身是否具有公信力也有关。比方说对于查询某个windows的API函数的用法，msdn上的结果肯定比别的网站上更加可信。在这里就简单介绍一下pagerank的使用方法。

pagerank算法是google曾经的三大法宝之一，属于一种链接分析算法，现在大多数的搜索引擎排序算法也是由该种算法改进而来。算法的主要思想是如果某个网站被另一网站链接，那么这个网站的分数就能增加，而增加的分数由链接到该网站的网站的重要性决定。因此我们有必要将一些重要网站的初始分数设置得高一点，比方说，google就将他自己的网站分数设得相当高。

这篇文章就不对pagerank的原理做解释了，网上有解释得很好的文章。然后是pagrank的python实现：

```python
def make_square(html_db,urltag_db):
    tag = 0
    square = {}
    sentence = "SELECT id,url,outdegree_urls FROM html;"
    cursor = html_db.cursor()
    print 'Getting data from database...'
    cursor.execute(sentence)
    result = cursor.fetchall()
    print 'Gotten.'
    print 'Making url-no list.'
    urltag = {}
    for row in result:
        url_id = int(row[0])
        url = row[1]
        urltag[url]=url_id
    print 'Finished Making list.'
    for row in result:
        url_id = int(row[0])
        print url_id
        url = row[1]
        outdegree_urls = eval(row[2])
        outdegree_urls_numbers = []
        for x in outdegree_urls:
            if x in urltag:
                outdegree_urls_numbers.append(urltag[x])
        square[url_id] = outdegree_urls_numbers
    return square
```

首先实现的是初始矩阵的构建。上述代码中使用了了一个字典来代替二维矩阵的存储，一方面可以节省稀疏矩阵的存储空间，另一方面可以避免爬虫爬取时产生的存储标号错误造成的运算异常。对从数据库提取参数做些许说明。`id` 代表爬取到了网站的编号，`url` 是该网站的`url` ，`outdegree_urls` 是该网站所有的出度url的内容。

```python
start_time = time.time()

print "Start to make square......"
square = make_square(html,urltag)
print "Square has been built.Start to calculate PAGERANK."

print "Make original vector."
length = len(square)
origin = 1.0/length
vector = {}
print length
for i in square:
    vector[i]=origin
print "Original vector has benn built.It is",repr(vector)

for i in range(30):
    print "Now the calculate time is ---",i,"---"
    dics = {}
    for x in square:
        dic = {}
        dic["vector_tag"] = vector[x]
        dic["tag_number"] = x
        dic["tag_urls"] = square[x]
        dics.append(dic)
    print "Finished adding."

    #calculate weighted vector
    for i in vector:
        vector[i] = vector[i]*0.3

    for dic in dics:
        tag_urls = dic['tag_urls']
        if not tag_urls:
            tag_value = 0
        else:
            tag_value = float(dic["vector_tag"])/len(tag_urls)
        outdegree_urls = square[dic['tag_number']]
        for x in outdegree_urls:
            vector[x]+=tag_value
    
    print "This turn finished.Vector is :"
    print repr(vector)


for x in vector:
    final_pagerank.set(x,vector[x])

cost_time = time.time()-start_time

print "Now finied."
print 'Cost',cost_time
```

一般对于pagrank的计算30轮左右就能得到收敛的结果。上面的计算步骤分别是：（1）初始化结果向量为为所有网页个数的倒数。（2）进入每轮的循环，获取每个向量对应网站的pagerank值，出度url，url编号。（3）对向量进行加权。（4）计算该轮的pagerank值。（5）若没到循环上限，继续循环。

### 0x03 倒排索引

利用倒排索引我们可以找到词与网页的联系。比方说，我们对于词“教授”，在编号几几的网址中存在。所以构建倒排索引的过程就是对每个网页文本进行分割，获得每个词与网页的联系的过程。关键代码如下：

```python
soup=BeautifulSoup(html,'html.parser')
string=soup.get_text()
seg_list = jieba.cut_for_search(string) #分词
for word in seg_list:
    if word not in dic_words:#这个词在索引中记录过
            dic_words[word] = 1
        else:
            dic_words[word]+=1
```

在数据库中存储方式是这样的：

![pic](http://ofnd3snod.bkt.clouddn.com/blog/python/searchengine/01.png)

图的意义是对于编号为100067号的单词，在key的网页中出现了value次。

### 0x04 分布式

比较推荐的当然是使用现成的分布式工具如hadoop。我在这里自己用redis实现了一个分布式的搜索引擎，原理是利用map-reduce将数据拆分成key-value形式，利用redis作为管道实现同步。代码在我的github上可以看到[https://github.com/LoonLi/Search](https://github.com/LoonLi/Search)，原理也比较简单，就不多说了。