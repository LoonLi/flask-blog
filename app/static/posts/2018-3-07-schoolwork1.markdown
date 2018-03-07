---
layout: post
title:  "学校任务总结——python读取excel，图形化与打包"
date:   2018-03-07 11:49:45 +0200
categories: python
published: true
---
        这篇博客是对python读取excel，图形化与打包的一个小总结。

## 0x00 程序介绍

程序的代码在[这里](https://github.com/LoonLi/flask-blog)。程序本身并不复杂，功能就是先读取excel内容，然后根据ecxel内容对图片改名。其余就是做了一个图形化界面还有这里没有的打包操作。

## 0x01 操作excel

python操作excel我用到的是`xlrd`库。这个库的文档内容相当丰富，应该是能够实现很多复杂的excel操作的。但之前我用excel作为爬虫记录存储数据的时候出现了存储错误的问题，具体的原因还不清楚，猜测是内容过大excel的一个sheet可能存贮不了。不过这次的操作只涉及到了读取excel所以不需要考虑写入的问题。

```python
try:
    data = xlrd.open_workbook(excel_path)
    table = data.sheet_by_name('reportofstudent')
    #生成学生学号与身份证号对应字典
    first_row = table.row_values(0)
    c_student_number = first_row.index('学号')
    c_id_number = first_row.index('身份证号')
    list_student_number = table.col_values(c_student_number)
    list_id_number = table.col_values(c_id_number)
    dict_sn_idn = {}
    for c in range(1,len(list_id_number)-1):
        dict_sn_idn[list_student_number[c]] = list_id_number[c]
except :
    print("发生excel读取错误！")
    messagebox.showerror("错误","发生excel读取错误！错误内容为%s。" % (traceback.format_exc()))
```

首先利用`xlrd.open_workbook()`函数打开excel文件。根据xlrd文档，这里返回的是一个`book`对象，然后利用`index()`方法找到学号与身份证的对应列，再利用`book`对象的`col_values()`方法找到对应列。现在得到了学号与身份证的对应数据，然后就可以建立学号对应身份证字典开始改名操作。

另外一点，这里利用`traceback`库输出了错误信息。

## 0x02 改名操作

改名操作可以利用`os`库完成。

```python
#修改所有图片的名称
path = work_path
list_error = []
for f in os.listdir(path):
    if os.path.isfile(os.path.join(path,f))==True:
        if f.find('.jpg') > 0:
            if dict_sn_idn.get(f[:f.find('.jpg')],False):
                try:
                    os.rename(os.path.join(path,f),os.path.join(path,dict_sn_idn[f[:f.find('.jpg')]]+".jpg"))
                except:
                    list_error.append(f)
            else:
                list_error.append(f)
print('共有'+str(len(list_error))+'个学号未能找到对应身份证号。\n')
messagebox.showinfo("成功","改名已完成，有%s个学号未能找到对应身份证号或身份证信息有误。"%(str(len(list_error))))
```

## 0x03 图形化

python图形化的库有很多，这里使用了python3安装时同时安装的`tkinter`库。基础的图形化界面设计由下面的代码实现：

```python
window = tk.Tk()
window.title('修改学号为身份证')
window.geometry('500x150')

lable_excel_path = tk.Label(window,text="excel路径：")
lable_excel_path.place(x=10,y=20)
text_excel_path = tk.Text(window,width=50,height=1)
text_excel_path.place(x=80,y=25)
btn_excel_path = tk.Button(window,text="选择",height=1,command=on_click_btn_excel_path)
btn_excel_path.place(x=450,y=18)

lable_main_path = tk.Label(window,text="图片路径：")
lable_main_path.place(x=10,y=60)
text_main_path = tk.Text(window,width=50,height=1)
text_main_path.place(x=80,y=65)
btn_main_path = tk.Button(window,text="选择",height=1,command=on_click_btn_main_path)
btn_main_path.place(x=450,y=58)

btn_change = tk.Button(window,text='开始',height=1,command=on_click_btn_change)
btn_change.place(x=250,y=100)

window.mainloop()
```

这些代码都很直观，一看就能明白。这个`tkinter`库有一个很奇葩的地方在于他对于文本框的操作很与众不同。拿点击获取excel路径的操作作为例子：

```python
def on_click_btn_excel_path():
    filename = tkinter.filedialog.askopenfilename()
    if filename != '':
        text_excel_path.delete('1.0',END)
        text_excel_path.insert(INSERT,filename)
```

首先利用`tkinter.filedialog.askopenfilename()`函数获取到文件路径，然后删除文本框内容，再插入新内容。其中`delete（）`有两个参数，表示删除的区域，而`tkinter`库内替你定义好了删除到结尾的宏定义，所以我们使用`END`。然后是`insert()`方法，同样是两个参数，第一个表示插入的位置，第二个是插入的字符串。`INSERT`同样是定义好的宏定义，具体是什么意义也不是特别清楚，总之拿来用了。

另外还有消息框的使用，也很简单：

```python
from tkinter import messagebox
#...
messagebox.showerror("错误","发生excel读取错误！错误内容为%s。" % (traceback.format_exc()))
#...
messagebox.showinfo("成功","改名已完成，有%s个学号未能找到对应身份证号或身份证信息有误。"%(str(len(list_error))))
```

## 0x04 打包成exe文件

详细的可以参照[这个网站](http://blog.csdn.net/zengxiantao1994/article/details/76578421)。讲得很清楚。这里就简单记录一下操作。

首先安装好`PyInstaller`,然后执行命令`pyinstaller -F path\\mycode.py --noconsole`就可以打包出没有cmd运行框的exe啦。如果不加`--noconsole`就会有cmd的运行框。

最后还有点小插曲，如果加了`--nonconsole`在我电脑上会被腾讯电脑管家识别为木马，很有意思。

## 0x05 总结

没有很么很难的代码跟操作，在这里简单地记录一下。