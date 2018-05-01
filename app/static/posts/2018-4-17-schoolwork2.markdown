---
layout: post
title:  "学校任务总结——c#图形化"
date:   2018-04-17 11:49:45 +0200
categories: c#
published: true
---
        对之前做过的c#项目做一个总结。

## 0x00 项目介绍

这是一个用c#写的题库管理系统。这里不对题库管理系统的运行作介绍，仅仅总结图形化的部分。

## 0x01 界面的设计与跳转

一个窗口对应一个`Form`，`Form`之下有各种控件。一般使用`Panel`或者是`GroupBox`作为控件的容器。可以使用一个`GroupBox`作为一个主界面容器，然后点击菜单选项后切换该`GroupBox`的对象来实现界面的切换。代码如下：

```c#
private void create_user(object sender, EventArgs e)
{
        createUser = new createUser();
        createUser.Show();
        groupBox.Controls.Clear();
        groupBox.Controls.Add(createUser);

}
```

效果如下：

![00](http://ofnd3snod.bkt.clouddn.com/blog/schoolwork/qa/00.gif)

## 0x02 动态添加控件

静态的界面设计配合visual studio 的强大功能很容易就能实现了。所以简单介绍一下如何实现动态的控件添加。下面的这个函数是用来给`Panel`动态添加控件的：

```c#
private void showResult(DataTable dt)
{
        panel_result.Controls.Clear();
        int i = 0;
        foreach (DataRow dr in dt.Rows)
        {
        string id = dr["ID"].ToString();

        GroupBox gp = new GroupBox();
        gp.Width = panel_result.Width-100;
        gp.Height = 300;
        gp.Location = new Point(5,i*300+5);
        gp.Text = database.Database.getQusetionTypeById(id)+id+"--"+database.Database.getQuestionEdittedTimeById(id);

        RichTextBox rtb = new RichTextBox();
        rtb.Location = new Point(5,50);
        rtb.Width = gp.Width - 10;
        rtb.Height = 240;
        rtb.ReadOnly = true;
        database.Database.fillRtbById(id,rtb);
        gp.Controls.Add(rtb);

        Button btn_edit = new Button();
        btn_edit.AutoSize = true;
        btn_edit.Text = "编辑此试题";
        btn_edit.Location = new Point(gp.Width-100,17);
        btn_edit.Tag = id;
        btn_edit.Click += new EventHandler(this.btn_edit_Click);
        gp.Controls.Add(btn_edit);

        Button btn_delete = new Button();
        btn_delete.AutoSize = true;
        btn_delete.Text = "删除此试题";
        btn_delete.Location = new Point(btn_edit.Location.X-100,btn_edit.Location.Y);
        btn_delete.Tag = id;
        btn_delete.Click += new EventHandler(this.btn_delete_Click);
        gp.Controls.Add(btn_delete);

        panel_result.Controls.Add(gp);
        i++;
        }
}
```

上面的代码涵盖了如何给控件添加子空间，如何给控件定位，如何设置控件的点击事件的功能。效果如下：

![01](http://ofnd3snod.bkt.clouddn.com/blog/schoolwork/qa/01.gif)

## 0x03 设置DataGridView

定义好`DataTalbe`然后`this.dataGridView_paper.DataSource = dt;`就可以了。

```c#
DataTable dt = new DataTable();
dt.Columns.Add("编号", typeof(Int32));//添加列
dt.Columns.Add("试卷名称", typeof(string));
dt.Columns.Add("修改日期", typeof(string));
using (OleDbCommand cmd = new OleDbCommand { Connection = database.dataHelper.GetSingleInstance().Con, CommandType = CommandType.Text })
{
string sql = $"select id,des,insert_date from tb_math_paper";
cmd.CommandText = sql;
OleDbDataReader reader = cmd.ExecuteReader();
while (reader.Read())
{                        
        DataRow dr = dt.NewRow();
        dr[0] = reader[0];
        dr[1] = reader[1];
        dr[2] = reader[2];
        dt.Rows.Add(dr);   
}
}
this.dataGridView_paper.DataSource = dt;
```

## 0x04 界面美化

由于自带的界面不是很美观，我们考虑使用别人写好的动态链接库封装一下界面。这里使用到的是[Magic library](https://www.codeproject.com/Articles/4193/Magic-Library-Docking-Manager-Designer)。

然后:

```c#
using Crownwood.Magic.Common;
using Crownwood.Magic.Docking;
```

再把之前写的Panel或者是GroupBox装进去就可以了：

```c#
public Search()
{
        InitializeComponent();

        loadPointTree();
        point_tree.ExpandAll();

        _dockingManager = new DockingManager(this, VisualStyle.IDE);

        Content notePad0 = _dockingManager.Contents.Add(this.groupBox1,"搜索选项");
        notePad0.DisplaySize = new Size(groupBox1.Width, groupBox1.Height);
        notePad0.FloatingSize = new Size(groupBox1.Width+50, groupBox1.Height+50);
        Content notePad1 = _dockingManager.Contents.Add(this.panel_result, "搜索结果");
        notePad1.DisplaySize = new Size(panel_result.Width, panel_result.Height);
        notePad1.FloatingSize = new Size(panel_result.Width+50, panel_result.Height+50);

        _dockingManager.ShowAllContents();
}
```

## 0x05 总结

这个c#项目还是相对简单的，也没有用到多线程之类的。有想到什么再加点进来。