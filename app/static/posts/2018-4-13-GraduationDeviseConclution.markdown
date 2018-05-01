---
layout: post
title:  "学校任务总结——python读取excel，图形化与打包"
date:   2018-04-12 11:49:45 +0200
categories: java,android
published: true
---
        毕业设计程序代码后台逻辑部分完成，对此进行一个总结。

## 0x00 项目介绍

是某教务管理系统的android端代码实现。实现的模块包括登录，课程，教师，销售人员，机构，学校，学生，驻校人员的管理。除了教师部分，其他部分的管理基本模式都一样。其他管理部分需要实现对该部分人员数据的查询，更新以及删除；教师部分则增加了查看和添加该教师的调课记录，查看其课程，查看其课表的功能。总结的内容主要是android应用程序的运行原理以及各个项目各个部分的关键代码。

## 0x01 Android APP 运行原理

每个界面就是一个Activity，Activity由View组成，View下是各种控件。当前运行的Activity是主线程，然后可以使用Handler向主线程传输消息实现线程间的信息传递。

## 0x02 网络线程的实现

这个项目关键的难点之一就在于怎样实现网络线程了。代码如下：

```java
public abstract class MyHttpThread extends Thread {
    private final static int timeout = 10000;
    private final static int so_timeout = 20000;
    protected Handler mhandler = null;
    protected String url = null;
    public final static int SUCCESS = 1;
    public final static int TIMEOUT = 2;
    public final static int CONNECTFAIL = 3;
    public final static int FAIL = 4;

    public MyHttpThread() {}

    @Override
    public void run() {
        System.out.println("开始执行网络线程！");
        super.run();
        Message message = mhandler.obtainMessage();
        Bundle responsebundle = new Bundle();
        String result = "";

        System.out.println(url);
        try {

            URL urlloader = new URL(url);
            BufferedReader reader = new BufferedReader
                    (new InputStreamReader(urlloader.openStream()));
            String line;
            while((line = reader.readLine()) != null)
            {
                System.out.println(line);
                result+=line;
            }

            if (result != null && result.startsWith("\ufeff")) {
                result = result.substring(1);
            }
            System.out.println("服务器返回的result" + result);
            responsebundle = parserResponse(result); // 得到解析值

            message.what = SUCCESS;
            message.setData(responsebundle);
            System.out.println("responsebundle==="+responsebundle.toString());
            System.out.println("网络线程执行完毕！");
        } catch (Exception e) {

            Log.e("log_tag", "Error in http connection " + e.toString());
            message.what = FAIL;
        } finally {

            mhandler.sendMessage(message);
            System.out.println("message==="+message.toString());
            Log.e("连接", "结束");
        }

    }

    public abstract Bundle parserResponse(String xml);
}
```

通过URL类访问网页，并获取其文本内容。设置好message，然后传给handler。其中有一个虚类`parserResponse`，这个虚类是继承该类的网络线程类实现的，用来处理获取到的文本信息。

## 0x03 处理接口信息

通过之前的网络线程类，实现了获取网络信息的功能。然后接下来介绍继承该类的处理类如何实现。拿功能较为简单的销售人员管理作为例子。

下面这个类是用来获取所有的销售人员信息的：

```java
public class GetAllSalerThread extends MyHttpThread {
    public GetAllSalerThread(Handler handler){
        super.url = AppUtil.GET_ALL_SALER;
        super.mhandler = handler;
    }
    @Override
    public Bundle parserResponse(String result) {
        Bundle bundle = new Bundle();
        try {
            JSONArray jsonArray = new JSONArray(result);
            ArrayList<String> number = new ArrayList<String>();
            ArrayList<String> name = new ArrayList<String>();
            for(int i=0;i<jsonArray.length();i++) {
                JSONArray tarray = jsonArray.getJSONArray(i);
                number.add(tarray.getString(1));
                name.add(tarray.getString(2));
            }
            bundle.putSerializable("mode","setListView");
            bundle.putStringArrayList("name",name);
            bundle.putStringArrayList("number",number);
        } catch (JSONException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
        return bundle;
    }
}
```

在类的构造函数中，给父类的`url`和`mhandle`变量赋值。前者是URL类访问的网页，后者是需要发送message的handler。然后在`parserResponse`类中对获取到的文本进行处理。由于接口返回的是json数据，所以这里对json数据进行处理。其中`mode`是用来分类信息的，在handler的实现中介绍。它的使用很简单，定义赋值后使用`start()`方法就可以了。例子：

```java
SearchSalersThread searchSalersThread = new SearchSalersThread(handler,name);
searchSalersThread.start();
```

## 0x04 handler的实现

handler的实现在各个activity的部分中，是activity类的一个变量。下面的是handler的一个模板：

```java
    private Handler handler = new Handler(){
        @Override
        public void handleMessage(Message msg){
            switch (msg.what){
                case MyHttpThread.SUCCESS:
                    Bundle bundle = msg.getData();
                    String flag = (String)bundle.getSerializable("mode");
                    if("mode".equals(flag)){
                    }
                    break;
                case MyHttpThread.FAIL:
                    Toast.makeText(getApplicationContext(), "网络连接失败，请检查网络设置！", Toast.LENGTH_SHORT).show();
                    break;
            }
        }
    };
```

定义了`Handler`类后，重写`handlerMessage`方法，获取message信息，通过之前定义好的mode信息分类执行代码。

## 0x05 ListView相关

### 一，ListView内容填充

需要首先定义好一个layout文件，然后再定义adapter。例子：

```java
ArrayList<String> name = bundle.getStringArrayList("name");
ArrayList<String> number = bundle.getStringArrayList("number");
List<Map<String,Object>> listitem = new ArrayList<Map<String,Object>>();
for(int i=0;i<name.size();i++)
{
    Map<String,Object> showitem = new HashMap<String,Object>();
    showitem.put("name",name.get(i));
    showitem.put("number",number.get(i));
    listitem.add(showitem);
}
SimpleAdapter myAdapter = new SimpleAdapter(getApplicationContext(),listitem,R.layout.course_list_item,new String[]{"name","number"},new int[]{R.id.tv_course_name,R.id.tv_course_number});
list_info.setAdapter(myAdapter);
```

### 二，ListView设置点击事件

例子如下：

```java
list_info = (ListView)findViewById(R.id.list_saler_info);
list_info.setOnItemClickListener(new AdapterView.OnItemClickListener() {
    @Override
    public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
        HashMap<String,String> map = (HashMap<String, String>) list_info.getItemAtPosition(position);
        String number = map.get("number");
        Intent intent = new Intent(SalerActivity.this,SalerInfoActivity.class);
        intent.putExtra("number",number);
        startActivity(intent);
    }
});
```

然而这样只能设置对整个ListItem的点击，不能设置对其中某一个控件的点击。这时需要重写一下`getView`方法。比如我在Item中定义了一个Button，那么我需要：

```java
private class MyAdapter extends SimpleAdapter implements View.OnClickListener{
        public MyAdapter(Context context, List<? extends Map<String, ?>> data, int resource, String[] from, int[] to){
            super(context,data,resource,from,to);
        }
        public View getView(int position, View convertView, ViewGroup parent) {
            convertView = super.getView(position,convertView,parent);
            Button btnButton = (Button) convertView.findViewById(R.id.btn_charschool_item);
            btnButton.setOnClickListener(this);
            return convertView;
        }
        @Override
        public void onClick(View v) {
            View now_v =  (View)v.getParent().getParent();
            TextView tv_name = (TextView)now_v.findViewById(R.id.tv_charschool_item);
            String seleted_name = tv_name.getText().toString();
            int sid = getSchoolID(seleted_name);
            String schools_id = "";
            String schools_name = "";
            int[] new_school_list = new int[now_shool_list.length-1];
            int j=0;
            for(int i=0;i<now_shool_list.length;i++){
                if(sid!=now_shool_list[i]){
                    new_school_list[j] = now_shool_list[i];
                    j++;
                }
            }
            for(int i=0;i<new_school_list.length;i++){
                if(i!=0){
                    schools_id += ",";
                    schools_name += "<br/>";
                }
                schools_id+=Integer.toString(new_school_list[i]);
                schools_name+=getSchoolName(new_school_list[i]);
            }
            if(TextUtils.isEmpty(schools_id)){
                schools_id = " ";
            }
            UpdateTeacherSchoolThread updateTeacherSchoolThread = new UpdateTeacherSchoolThread(handler,id,schools_id,schools_name);
            updateTeacherSchoolThread.start();
        }
    }
```

顺带一提，上面的onClick代码中实现了通过view的父控件来寻找其他view的代码。

## 0x06 Activity相关

在android程序中，一个界面就是一个Activity，所以通过Activity的创建于关闭来实现界面的切换。下面总结些许Activity界面操作的关键点。

Activity除了入口以外，其他的通常使用`Intent`类来启动。例如：

```java
Intent intent = new Intent(TeacherCourseActivity.this,TeacherCourseInfoActivity.class);
intent.putExtra("cid",cid);
intent.putExtra("tid",tid);
startActivity(intent);
```

然后可以通过`Intent.putExtra(String key,Object value)`方法向新创建的Intent传递变量。传递好的参数以key-value的方式存储，在新的Activtiy中，可以使用`getIntent().getStringExtra(String key)`等方法得到。

关闭Activity的方法也很简单，在希望关闭的活动中使用`finish()`方法即可。

## 0x07 更改style样式

首先在`colors.xml`中定义好想用的颜色：

```xml
<resources>
    <color name="material_blue_500">#009688</color>
    <color name="material_blue_700">#00796B</color>
    <color name="material_green_A200">#FD87A9</color>
</resources>
```

然后在`style.xml`中，更改style标签:

```xml
<style name="AppTheme" parent="Theme.AppCompat.Light.DarkActionBar">
    <!-- Customize your theme here. -->
    <item name="colorPrimary">@color/material_blue_500</item>
    <item name="colorPrimaryDark">@color/material_blue_700</item>
    <item name="colorAccent">@color/material_green_A200</item>
</style>
```