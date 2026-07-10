import os
import socket
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

# --- EMON ROOTX: Local Network File Share Tool ---
app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Branding Config
BRAND_NAME = "EMON ROOTX"
TOOL_NAME = "NetShare-RootX"

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', files=files, brand=BRAND_NAME, tool=TOOL_NAME)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' in request.files:
        file = request.files['file']
        if file.filename != '':
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
    return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    local_ip = get_ip()
    print(f"\n[!] EMON ROOTX Server active at: http://{local_ip}:5000\n")
    app.run(host='0.0.0.0', port=5000)