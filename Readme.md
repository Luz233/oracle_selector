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

## 源码
### main.py
``` python
from flask import Flask, jsonify, Response, request
import cx_Oracle
import json
import os

# 读取配置文件
with open('config.json') as config_file:
    config = json.load(config_file)

# 设置 Oracle 客户端路径
oracle_client_path = config['oracle']['oracle_client_path']
os.environ['PATH'] = oracle_client_path + ";" + os.environ['PATH']

# 配置 Oracle 连接
oracle_config = config['oracle']

# 根据配置选择使用服务名或 SID
if oracle_config.get('use_service_name'):
    dsn_tns = cx_Oracle.makedsn(oracle_config['ip'], oracle_config['port'], service_name=oracle_config['service_name'])
else:
    dsn_tns = cx_Oracle.makedsn(oracle_config['ip'], oracle_config['port'], sid=oracle_config['instance'])

connection = cx_Oracle.connect(oracle_config['username'], oracle_config['password'], dsn_tns)

app = Flask(__name__)

def execute_query(query, params=None):
    """执行 Oracle 查询并返回结果"""
    cursor = connection.cursor()
    cursor.execute(query, params or {})
    columns = [i[0] for i in cursor.description]
    data = cursor.fetchall()
    cursor.close()
    return columns, data

@app.route('/')
def index():
    return jsonify({"message": "Welcome to the Flask Oracle App!"})

@app.route('/<path:path>', methods=['GET'])
def route(path):
    route_path = '/' + path
    routes = config['routes']
    
    if route_path in routes:
        route_info = routes[route_path]
        query = route_info['sql']
        title = route_info['name']

        # 从 GET 请求中获取参数
        params = request.args.to_dict()
        columns, data = execute_query(query, params)

        html = f"""
        <html>
        <head>
            <title>{title}</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 20px;
                }}
                h1 {{
                    color: #333;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 20px;
                }}
                table, th, td {{
                    border: 1px solid #ddd;
                }}
                th, td {{
                    padding: 15px;
                    text-align: left;
                }}
                th {{
                    background-color: #f2f2f2;
                }}
                tr:nth-child(even) {{
                    background-color: #f9f9f9;
                }}
                tr:hover {{
                    background-color: #f1f1f1;
                }}
            </style>
        </head>
        <body>
            <h1>{title}</h1>
            <table>
                <thead>
                    <tr>{''.join(f'<th>{col}</th>' for col in columns)}</tr>
                </thead>
                <tbody>
                    {''.join(f'<tr>{"".join(f"<td>{cell}</td>" for cell in row)}</tr>' for row in data)}
                </tbody>
            </table>
        </body>
        </html>
        """
        
        return Response(html, mimetype='text/html')
    else:
        return Response("<h1>404 Not Found</h1>", status=404, mimetype='text/html')

if __name__ == '__main__':
    flask_config = config['flask']
    app.run(host='0.0.0.0', port=flask_config['port'])
```

### config.json
``` python 
{
  "oracle": {
    "ip": "127.0.0.1",
    "port": "1529",
    "username": "system",
    "password": "xxxxxxx",
    "instance": "xxxxxx",
	"service_name": "xxxxx",
    "oracle_client_path": "C:\\instantclient-basic-windows.x64-11.2.0.4.0\\instantclient_11_2",
	"use_service_name": true
  },
  "routes": {
    "/route1": {
      "name": "name1",
      "sql": "SELECT count(*) as 查询结果 FROM xxx where ID>:value"
    },
    "/route2": {
      "name": "name2",
      "sql": "SELECT count(*) as 查询结果 FROM xxx"
    }
  },
  "flask": {
    "port": 5001
  }
}

```
