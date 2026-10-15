from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def index():
    return """
    <h1>Hello Railway</h1>
    <p>✅ 项目部署成功</p>
    <p>当前服务运行正常</p>
    """

@app.route('/api/info')
def info():
    return {
        "status": "ok",
        "message": "Railway flask api demo"
    }

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
