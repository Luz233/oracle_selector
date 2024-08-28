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
