from flask import Flask, request, jsonify
import io
import base64
import os

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

@app.route('/api/ai-enhance', methods=['POST'])
def ai_enhance():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image'}), 400

        file = request.files['image']
        img_bytes = file.read()

        from rembg import remove
        from PIL import Image

        input_image = Image.open(io.BytesIO(img_bytes))
        output_image = remove(input_image)

        output_bytes = io.BytesIO()
        output_image.save(output_bytes, format='PNG')
        output_bytes.seek(0)

        encoded = base64.b64encode(
            output_bytes.read()).decode('utf-8')

        return jsonify({
            'status': 'ok',
            'final_image_url': 
                f'data:image/png;base64,{encoded}'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
