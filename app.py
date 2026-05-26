from flask import Flask, request, jsonify
from rembg import remove
from PIL import Image
import io
import base64
import os

app = Flask(__name__)

@app.route('/api/ai-enhance', methods=['POST'])
def ai_enhance():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image'}), 400

        file = request.files['image']
        img_bytes = file.read()

        # Убираем фон через REMBG
        input_image = Image.open(io.BytesIO(img_bytes))
        output_image = remove(input_image)

        # Конвертируем результат в bytes
        output_bytes = io.BytesIO()
        output_image.save(output_bytes, format='PNG')
        output_bytes.seek(0)

        # Кодируем в base64
        encoded = base64.b64encode(
            output_bytes.read()).decode('utf-8')

        return jsonify({
            'status': 'ok',
            'final_image_url': f'data:image/png;base64,{encoded}'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
