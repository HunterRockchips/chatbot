from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)

# DeepSeek API configuration
DEEPSEEK_API_KEY = "your_API_KEY"  # Replace with your actual API key
DEEPSEEK_API_URL = "https://api.deepseek.com/chat/completions"  # Replace with actual API endpoint

@app.route('/')
def home():
    return render_template('chat.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    
    # Prepare the request to DeepSeek API
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "deepseek-chat",  # Replace with actual model name
        "messages": [
            {"role": "user", "content": user_message}
        ]
    }
    
    try:
        # 禁用代理设置
        proxies = {
            'http': None,
            'https': None
        }
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data, proxies=proxies, verify=False)
        response.raise_for_status()
        bot_response = response.json()['choices'][0]['message']['content']
        return jsonify({"response": bot_response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
