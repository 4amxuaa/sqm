from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# 内存存储（重启丢失数据，演示使用）
visit_count = 0
msg_list = []

HTML_INDEX = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Railway Flask 项目完整部署教程</title>
    <style>
        *{box-sizing:border-box;margin:0;padding:0}
        body{font-family:system-ui,sans-serif;max-width:900px;margin:20px auto;padding:0 16px;line-height:1.6}
        h1,h2,h3{margin:18px 0 10px}
        .card{border:1px solid #e5e7eb;border-radius:10px;padding:18px;margin:16px 0;background:#fff}
        pre{background:#111;color:#00ff99;padding:12px;overflow-x:auto;border-radius:6px;font-size:14px}
        .msg-item{padding:6px 0;border-bottom:1px solid #eee}
        form{margin:12px 0}
        input{padding:8px;width:75%;max-width:400px}
        button{padding:8px 14px;cursor:pointer}
        .tip{background:#eef7ff;padding:10px;border-left:4px solid #2563eb}
    </style>
</head>
<body>
    <div class="card">
        <h1>✅ Railway + Flask 完整部署教程</h1>
        <p>当前页面访问次数：<strong>{{ count }}</strong></p>
    </div>

    <div class="card">
        <h2>📋 项目介绍</h2>
        <p>单文件Flask项目，仅 app.py + requirements.txt + Procfile + .gitignore，可一键部署到 Railway。</p>
        <p class="tip">⚠️ 当前数据保存在内存，服务重启后留言、访问计数会清空；如需持久化可以接入SQLite。</p>
    </div>

    <div class="card">
        <h2>🔧 前置准备（Termux环境）</h2>
<pre>
# 1. 配置Git全局账号
git config --global user.name "4amxuaa"
git config --global user.email "1556646563@qq.com"

# 2. 配置SSH密钥（github/gitee/gitcode多平台）
# 生成独立密钥，~/.ssh/config区分host，测试连通
ssh -T git@github.com
</pre>
    </div>

    <div class="card">
        <h2>📁 本地创建项目</h2>
<pre>
# 新建项目文件夹
mkdir sqm
cd sqm

# 初始化git仓库
git init

# Github网页新建仓库（不要勾选readme）
# 关联远程仓库
git remote add origin git@github.com:4amxuaa/sqm.git
</pre>
    </div>

    <div class="card">
        <h2>📄 项目必须的4个文件</h2>
<p><b>1. app.py</b>：主程序，web服务代码（当前这个文件）</p>
<p><b>2. requirements.txt</b>：Python依赖</p>
<pre>Flask==2.3.3</pre>
<p><b>3. Procfile（无后缀！）</b>：Railway启动命令</p>
<pre>web: python app.py</pre>
<p><b>4. .gitignore</b>：忽略不需要提交的缓存文件</p>
<pre>
__pycache__/
*.pyc
*.pyo
*.pyd
.env
.venv
venv/
</pre>
    </div>

    <div class="card">
        <h2>🧪 本地测试</h2>
<pre>
pip install flask
python app.py
# 本地访问：127.0.0.1:5000
# Ctrl + C 停止服务
</pre>
    </div>

    <div class="card">
        <h2>📤 Git提交并推送到Github</h2>
<pre>
git add .
git commit -m "备注本次修改内容"
git push
</pre>
<p>推送完成，刷新Github仓库页面查看代码。</p>
    </div>

    <div class="card">
        <h2>🚀 Railway部署步骤</h2>
<ol>
<li>打开 railway.app，使用Github账号登录</li>
<li>New Project → Import from GitHub repo</li>
<li>选择仓库 4amxuaa/sqm</li>
<li>点击Deploy，自动拉代码、安装依赖、启动服务</li>
<li>部署完成 → Settings → Domains 获取访问域名</li>
</ol>
<p class="tip">后续修改代码，git push到Github后，Railway会<strong>自动重新部署</strong>！</p>
    </div>

    <div class="card">
        <h2>🧩 功能演示区</h2>
        <h3>留言板</h3>
        <form action="/add_msg" method="post">
            <input type="text" name="msg" placeholder="输入留言" required>
            <button type="submit">提交留言</button>
        </form>
        <div style="margin-top:12px">
            {% for m in messages %}
                <div class="msg-item">• {{ m }}</div>
            {% endfor %}
        </div>
        <h3 style="margin-top:16px">API接口</h3>
        <p>GET <a href="/api/count">/api/count</a> 获取访问统计和留言列表</p>
        <p>POST /api/addmsg JSON提交留言</p>
<pre>
# curl测试示例
curl -X POST -H "Content-Type:application/json" -d '{"msg":"测试留言"}' https://你的域名/api/addmsg
</pre>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    global visit_count
    visit_count += 1
    return render_template_string(HTML_INDEX, count=visit_count, messages=msg_list)

# 网页表单提交留言
@app.route('/add_msg', methods=["POST"])
def add_msg():
    content = request.form.get("msg", "").strip()
    if content:
        msg_list.append(content)
    return "<script>location.href='/'</script>"

# API 获取访问次数、留言
@app.route('/api/count')
def api_count():
    return jsonify({
        "code": 200,
        "visit_count": visit_count,
        "msg_list": msg_list
    })

# API POST添加留言（JSON）
@app.route('/api/addmsg', methods=["POST"])
def api_addmsg():
    data = request.get_json()
    if not data or "msg" not in data:
        return jsonify({"code":400,"msg":"缺少msg参数"})
    content = data["msg"].strip()
    if content:
        msg_list.append(content)
        return jsonify({"code":200,"msg":"留言成功"})
    return jsonify({"code":400,"msg":"内容不能为空"})

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
