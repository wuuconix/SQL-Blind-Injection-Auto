# SQL盲注自动化脚本

## 文件说明
`blind_int.py` 为整型注入
`blind_str.py` 为字符型注入
`blind_time_int.py` 为整形时间盲注

## 脚本使用说明
+ 在脚本中有一个变量为`success_flag`，意味查询成功的页面关键字，脚本将根据此变量来判断查询是否成功。这个变量需要你根据实际情况修改。
+ 脚本中的base_url需要你进行更改
+ `blind_str.py`中的request请求都带上了cookie，如果不需要，请自行删除。

## 视频演示
+ [https://www.bilibili.com/video/BV1fL411b7b8/](https://www.bilibili.com/video/BV1fL411b7b8/)