## 功能
将oracle数据库的sql运行执行结果可视化，使用html的形式展示，便于数据监控。
## 运行环境
Win10 64位及以上
### 运行条件：
- 可以与数据库服务器正常联通
- Instantclient版本与目标数据库版本相匹配
- Sql语句编写正确，且每个路由中只有一个sql

## 基本使用
1. 解压instantclient-basic-windows.x64-11.2.0.4.0.zip，将解压后的文件夹放到不带中文路径的地方，如C:\\instantclient-basic-windows.x64-11.2.0.4.0\\instantclient_11_2，记住此路径

2. 修改config.json
![](https://www.hyluz.cn/zb_users/upload/2024/08/202408281632404945429.png)
（sql语句后面不需要分号）
3. 运行main.exe
如果出现端口监听则运行成功
![](https://www.hyluz.cn/zb_users/upload/2024/08/202408281632519835823.png)

4. 网页访问http://ip:端口/路由  测试数据
![](https://www.hyluz.cn/zb_users/upload/2024/08/202408281632575089144.png)
## 进阶使用
### 查询参数传递
部分sql语句需要经常更换参数，如时间、id等，参数若写在配置文件中不便于调整。可以在配置文件中预留参数位置，使用网页传参的方式进行查询，如：
配置文件中的sql：
SELECT count(*) as 查询结果 FROM dvsys.code$ where ID#>:value
:value 为临时使用的参数变量值，变量名可任取，但前面必须加英文冒号
此时网页访问URL示例为：
http://127.0.0.1:5001/route1?value=200

![](https://www.hyluz.cn/zb_users/upload/2024/08/202408281633118657729.png)
若存在多个参数变量，使用&隔开，即：
http://ip:端口/路由?变量名1=变量值&变量名2=变量值&变量名3=变量值……

