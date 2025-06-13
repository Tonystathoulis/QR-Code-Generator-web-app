from flask import Flask, request, render_template_string
import qrcode
import base64
from io import BytesIO

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QR GUM</title>
    <style>
        body {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
        background-color: #205ad6;
        font-family: Arial, sans-serif;
        margin: 0;
        position: relative; 
        overflow: hidden; 
    }
        h1 {
            color: #ff69b4;
            font-size: 5em;
            text-align: center;  
            animation: bounce 1s infinite; 
            display: flex;
            align-items: center;
        }
        .bubble {
            display: inline-block;
            width: 7px;
            height: 7px;
            background-color: #ff85c2; 
            border-radius: 50%; 
            margin: 0 10px; 
            position: relative;
            animation: float 2s infinite; 
        }
        @keyframes bounce {
            0%, 20%, 50%, 80%, 100% {
                transform: translateY(0);
            }
            40% {
                transform: translateY(-10px); 
            }
            60% {
                transform: translateY(-5px);
            }
        }
        @keyframes float {
            0%, 100% {
                transform: translateY(0);
            }
            50% {
                transform: translateY(-5px); 
            }
        }
        form {
            display: flex; 
            flex-direction: column;
            align-items: center; 
            margin-bottom: 20px;
        }
        input[type="url"] {
            width: 150%;
            padding: 0.5em;
            border: 2px solid #ff69b4;
            border-radius: 10px;  
            outline: none;
            margin-bottom: 10px; 
        }
        button {
            background-color: #ff69b4;
            color: white;
            border: none;
            padding: 0.7em 1.5em;
            font-size: 1em;
            border-radius: 10px;  
            cursor: pointer;
        }
        button:hover {
            background-color: #ff85c2;
        }
        .qr-result {
            display: flex; 
            justify-content: center; 
            margin-top: 20px;
        }
        .qr-result img {
            width: 150px;  
            height: 150px; 
        }
        footer {
            animation: slideIn 1s ease-in-out;
            margin-top: 20px;
            text-align: center;
            color: #ff69b4;
            font-size: 1.2em;
        }
        @keyframes slideIn {
            from {
                transform: translateY(100px);
                opacity: 0;
            }
            to {
                transform: translateY(0);
                opacity: 1;
            }
        }
        .pink-rectangle {
            position: absolute;
            bottom: 4;
            left: 846px;
            width: 40em; 
            height: 60em; 
            background-color: rgba(255, 105, 180, 0.10); 
            z-index: -1; 
            transform: rotate(-10deg); 
            transform-origin: bottom right; 
        }
    </style>
    <script>
        async function generateQRCode(event) {
            event.preventDefault();
            const url = document.getElementById('urlInput').value;
            const response = await fetch(`/generate_qr?url=${encodeURIComponent(url)}`);
            const data = await response.json();
            document.getElementById('qrImage').src = data.qr_code;
            document.getElementById('qrImage').style.display = 'block';
            
            const button = document.getElementById('generateButton');
            button.textContent = 'Generate Again';
            button.setAttribute('onclick', 'location.reload();');
        }
    </script>
</head>
<body>
    <h1>
        <span class="bubble"></span>
        QR GUM
        <span class="bubble"></span>
    </h1>

    <form onsubmit="generateQRCode(event)">
        <input type="url" id="urlInput" placeholder="Enter your link here..." required>
        <button id="generateButton" type="submit">Generate QR Code</button>
    </form>
    <div class="qr-result">
        <img id="qrImage" src="" alt="QR Code" style="display:none;">
    </div>
    <footer>
         <size style="font-size: 0.8em;">Paste any link and generate a QR code for it! <br>&copy; 2024 QR GUM Scan and have fun!
    </footer>
    
    <div class="pink-rectangle"></div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/generate_qr', methods=['GET'])
def generate_qr():
    url = request.args.get('url')
    if not url:
        return {"error": "No URL provided"}, 400

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=6,  
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="#ff69b4", back_color="#fff3f7")
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)

    img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
    img_src = f"data:image/png;base64,{img_base64}"

    return {"qr_code": img_src}

if __name__ == '__main__':
    app.run(debug=True)
