from flask import Flask, request, jsonify, render_template_string
import boto3
import json

app = Flask(__name__)
client = boto3.client(service_name='bedrock-runtime', region_name='us-east-1')

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Truth Field Detector</title>
    <style>
        body { font-family: Arial; max-width: 800px; margin: 50px auto; background: #0a0a0a; color: white; padding: 20px; }
        h1 { color: #00ff88; text-align: center; }
        textarea { width: 100%; height: 120px; padding: 10px; font-size: 16px; border-radius: 8px; background: #1a1a1a; color: white; border: 1px solid #333; }
        button { width: 100%; padding: 15px; background: #00ff88; color: black; font-size: 18px; font-weight: bold; border: none; border-radius: 8px; cursor: pointer; margin-top: 10px; }
        #result { margin-top: 30px; padding: 20px; border-radius: 10px; display: none; }
        .HIGH { background: #3a0000; border: 2px solid #ff4444; }
        .MEDIUM { background: #3a3000; border: 2px solid #ffaa00; }
        .LOW { background: #003a00; border: 2px solid #00ff88; }
        .score { font-size: 48px; font-weight: bold; text-align: center; }
        .HIGH .score { color: #ff4444; }
        .MEDIUM .score { color: #ffaa00; }
        .LOW .score { color: #00ff88; }
        .label { text-align: center; font-size: 24px; margin-bottom: 20px; }
        .section { margin-top: 15px; }
        .section h3 { color: #aaa; }
        .tag { display: inline-block; padding: 5px 10px; border-radius: 20px; margin: 3px; background: #333; font-size: 14px; }
        #loading { text-align: center; display: none; color: #00ff88; font-size: 20px; margin-top: 20px; }
    </style>
</head>
<body>
    <h1>🛰️ Truth Field Detector</h1>
    <p style="text-align:center; color:#aaa;">Paste any text to analyze its narrative risk</p>
    <textarea id="text" placeholder="Paste news, tweets, speeches or any text here..."></textarea>
    <button onclick="analyze()">🔍 Analyze Now</button>
    <div id="loading">⏳ Analyzing with Amazon Nova...</div>
    <div id="result"></div>

    <script>
    async function analyze() {
        const text = document.getElementById('text').value;
        if (!text) return alert('Please enter some text');
        document.getElementById('loading').style.display = 'block';
        document.getElementById('result').style.display = 'none';
        
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({text: text})
        });
        const data = await response.json();
        document.getElementById('loading').style.display = 'none';
        
        const r = document.getElementById('result');
        r.className = data.risk_level;
        r.style.display = 'block';
        r.innerHTML = `
            <div class="label">${data.risk_level} RISK</div>
            <div class="score">${data.score}/100</div>
            <div class="section"><h3>📢 Emotional Language</h3>${data.emotional_language.map(w => `<span class="tag">${w}</span>`).join('')}</div>
            <div class="section"><h3>⚠️ Absolutist Claims</h3>${data.absolutist_claims.map(w => `<span class="tag">${w}</span>`).join('')}</div>
            <div class="section"><h3>📚 Missing Citations</h3>${data.missing_citations ? '❌ Yes' : '✅ No'}</div>
            <div class="section"><h3>💬 Explanation</h3><p>${data.explanation}</p></div>
        `;
    }
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/analyze', methods=['POST'])
def analyze():
    text = request.json['text']
    prompt = f"""You are TruthField, a narrative risk analyzer.
Analyze this text and return ONLY a JSON object with:
- risk_level: LOW, MEDIUM, or HIGH
- score: number from 0 to 100
- emotional_language: list of emotional words found
- absolutist_claims: list of absolute statements found
- missing_citations: true or false
- explanation: one sentence summary

Text: {text}

Respond ONLY with valid JSON, no markdown, no backticks."""

    response = client.invoke_model(
        modelId='amazon.nova-lite-v1:0',
        body=json.dumps({
            "messages": [
                {"role": "user", "content": [{"text": prompt}]}
            ]
        })
    )
    
    result = json.loads(response['body'].read())
    text_response = result['output']['message']['content'][0]['text']
    
    try:
        clean = text_response.strip().replace('```json','').replace('```','')
        data = json.loads(clean)
    except:
        data = {"risk_level": "MEDIUM", "score": 50, "emotional_language": [], "absolutist_claims": [], "missing_citations": True, "explanation": "Could not parse response"}
    
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
