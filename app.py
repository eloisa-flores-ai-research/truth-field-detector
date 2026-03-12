from flask import Flask, request, jsonify, render_template_string
import boto3
import json
import urllib.request
import urllib.parse
import re
import base64

app = Flask(__name__)
client = boto3.client(service_name='bedrock-runtime', region_name='us-east-1')

def fetch_url_text(url):
    """Fetch text content from a URL"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8', errors='ignore')
        # Remove HTML tags
        text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
        text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
        text = re.sub(r'<[^>]+>', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text[:3000]  # First 3000 chars
    except Exception as e:
        return None

PAGE1 = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Truth Field Detector</title>
  <link href="https://fonts.googleapis.com/css2?family=Chewy&display=swap" rel="stylesheet">
  <link href="https://fonts.googleapis.com/css2?family=Roboto&display=swap" rel="stylesheet">
  <link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;700&display=swap" rel="stylesheet">
  <link href="https://fonts.googleapis.com/css2?family=Dancing+Script&display=swap" rel="stylesheet">
  <link href="https://fonts.googleapis.com/css2?family=Share+Tech&display=swap" rel="stylesheet">
  <style>
    :root {
      --yellow: #ffde59;
      --orange: #c52d0e;
      --light-gray: #c5c5c5;
      --gradient-start: #282f4a;
      --gradient-end: #1e273b;
      --white: #ffffff;
    }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      background: radial-gradient(circle at 50% 50%, var(--gradient-start), var(--gradient-end));
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      color: var(--white);
      position: relative;
      font-family: 'Roboto', sans-serif;
    }
    .container {
      max-width: 700px;
      width: 90%;
      text-align: center;
      padding: 2rem;
    }
    .title-container {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 2rem;
      margin-bottom: 1.5rem;
    }
    .truth-field {
      font-family: 'Chewy', sans-serif;
      font-size: 50px;
      color: var(--yellow);
      line-height: 1;
    }
    .detector {
      font-family: 'Chewy', sans-serif;
      font-size: 45px;
      color: var(--yellow);
      line-height: 1;
    }
    .deer-character { width: 110px; }
    .subtitle {
      font-family: 'Barlow Condensed', sans-serif;
      font-size: 17px;
      margin-bottom: 1rem;
      color: var(--white);
    }
    .main-text {
      font-family: 'Barlow Condensed', sans-serif;
      font-size: 20px;
      color: var(--yellow);
      font-weight: 700;
      margin-bottom: 1.5rem;
    }
    .input-container { margin: 1.5rem 0; width: 100%; }
    textarea {
      width: 100%;
      min-height: 100px;
      padding: 1rem;
      border: 2px solid var(--orange);
      border-radius: 12px;
      background-color: var(--light-gray);
      font-family: 'Roboto', sans-serif;
      font-size: 14px;
      resize: vertical;
      margin-bottom: 1rem;
      color: #1e273b;
    }
    textarea::placeholder {
      color: #444;
      font-style: italic;
      font-size: 13px;
    }
    .analyze-btn {
      background-color: var(--orange);
      color: var(--white);
      font-weight: bold;
      padding: 0.75rem 2.5rem;
      font-size: 1.1rem;
      border: none;
      border-radius: 10px;
      cursor: pointer;
      transition: all 0.3s ease;
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
    }
    .analyze-btn:hover { transform: scale(1.05); background-color: #a82509; }
    .footer-note {
      margin-top: 2rem;
      font-family: 'Roboto', sans-serif;
      font-size: 10px;
      font-style: italic;
      color: var(--white);
      opacity: 0.7;
    }
    .signature {
      position: fixed;
      bottom: 1rem;
      left: 1rem;
    }
    .created-by {
      font-family: 'Dancing Script', sans-serif;
      font-size: 13px;
      color: var(--yellow);
    }
    .author {
      font-family: 'Share Tech', sans-serif;
      font-size: 12px;
      color: var(--white);
      display: flex;
      align-items: center;
      gap: 0.4rem;
    }
    .author-photo {
      width: 45px;
      height: 45px;
      border-radius: 50%;
      object-fit: cover;
    }
    #loading {
      display: none;
      margin-top: 1rem;
      color: var(--yellow);
      font-family: 'Barlow Condensed', sans-serif;
      font-size: 18px;
      animation: pulse 1.5s infinite;
    }
    @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.4} }
    #error-msg {
      display: none;
      color: #ff6b6b;
      margin-top: 0.5rem;
      font-size: 13px;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="title-container">
      <div class="title">
        <div class="truth-field">TRUTH FIELD</div>
        <div class="detector">DETECTOR</div>
      </div>
      <img src="/static/logo1venado.png" alt="Venado Detective" class="deer-character">
    </div>
    <p class="subtitle">INFORMATION IS POWER — BUT IT CAN ALSO MANIPULATE YOU</p>
    <p class="main-text">WANT THE TRUTH? PASTE ANY NEWS LINK OR TEXT</p>
    <div class="input-container">
      <textarea id="inputText" placeholder="Paste any news URL or text here and click the button"></textarea>
      <div id="error-msg">⚠️ Could not read that URL. Please paste the text directly.</div>
      <button class="analyze-btn" onclick="analyze()">👍 Analyze Now</button>
    </div>
    <div id="loading">⏳ Analyzing with Amazon Nova...</div>
    <div class="footer-note">* This version supports text and public news URLs. Social media and video analysis coming soon. 👁️</div>
  </div>
  <div class="signature">
    <div class="created-by">Created by</div>
    <div class="author">
      <img src="/static/eloisa_flores_foto.png" alt="Eloisa Flores" class="author-photo">
      Eloisa Flores
    </div>
  </div>
  <script>
    async function analyze() {
      const text = document.getElementById('inputText').value.trim();
      if (!text) { alert('Please enter some text or a URL'); return; }
      document.getElementById('loading').style.display = 'block';
      document.getElementById('error-msg').style.display = 'none';
      try {
        const response = await fetch('/analyze', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({text: text})
        });
        const data = await response.json();
        if (data.error) {
          document.getElementById('error-msg').style.display = 'block';
          document.getElementById('loading').style.display = 'none';
          return;
        }
        // Store result and go to page 2
        sessionStorage.setItem('result', JSON.stringify(data));
        window.location.href = '/results';
      } catch(e) {
        document.getElementById('loading').style.display = 'none';
        alert('Something went wrong. Please try again.');
      }
    }
  </script>
</body>
</html>'''

PAGE2 = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Truth Field Detector - Results</title>
  <link href="https://fonts.googleapis.com/css2?family=Chewy&display=swap" rel="stylesheet">
  <link href="https://fonts.googleapis.com/css2?family=Roboto&display=swap" rel="stylesheet">
  <link href="https://fonts.googleapis.com/css2?family=Dancing+Script&display=swap" rel="stylesheet">
  <link href="https://fonts.googleapis.com/css2?family=Share+Tech&display=swap" rel="stylesheet">
  <style>
    :root {
      --yellow: #ffde59;
      --orange: #c52d0e;
      --light-gray: #c5c5c5;
      --gradient-start: #282f4a;
      --gradient-end: #1e273b;
      --white: #ffffff;
    }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      background: radial-gradient(circle at 50% 50%, var(--gradient-start), var(--gradient-end));
      min-height: 100vh;
      display: flex;
      justify-content: center;
      font-family: 'Roboto', sans-serif;
      padding: 20px;
      color: var(--white);
      position: relative;
    }
    .container { width: 90%; max-width: 800px; position: relative; }
    .header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 1.5rem;
    }
    .risk-center { text-align: center; flex: 1; }
    .risk-label {
      font-family: 'Chewy', sans-serif;
      font-size: 50px;
      color: var(--white);
      text-decoration: underline;
      text-decoration-color: var(--orange);
      text-decoration-thickness: 3px;
      text-underline-offset: 6px;
    }
    .risk-label.HIGH { color: #ff4444; }
    .risk-label.MEDIUM { color: var(--white); }
    .risk-label.LOW { color: #00ff88; }
    .risk-score {
      font-family: 'Chewy', sans-serif;
      font-size: 50px;
      color: var(--yellow);
    }
    .title-right {
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .truth-detector-block { text-align: right; }
    .truth-field {
      font-family: 'Chewy', sans-serif;
      font-size: 30px;
      color: var(--yellow);
    }
    .detector {
      font-family: 'Dancing Script', sans-serif;
      font-size: 25px;
      color: var(--yellow);
    }
    .deer-right { width: 120px; }
    .risk-indicators {
      display: flex;
      flex-direction: column;
      gap: 1rem;
      margin: 1.5rem 0;
    }
    .indicator {
      display: flex;
      align-items: flex-start;
      gap: 0.5rem;
      font-size: 1rem;
      flex-wrap: wrap;
    }
    .indicator-icon { font-size: 1.5rem; }
    .indicator strong {
      font-size: 15px;
      letter-spacing: 1px;
    }
    .tags {
      display: flex;
      gap: 0.5rem;
      margin-left: 2rem;
      flex-wrap: wrap;
      margin-top: 0.3rem;
      width: 100%;
    }
    .tag {
      background-color: var(--orange);
      color: var(--white);
      padding: 0.25rem 0.75rem;
      border-radius: 0.5rem;
      font-size: 0.85rem;
    }
    .explanation {
      background-color: var(--light-gray);
      border-radius: 12px;
      padding: 1.2rem;
      margin: 1.5rem 0;
      font-size: 14px;
      line-height: 1.6;
      color: var(--gradient-end);
      border: 2px solid var(--yellow);
    }
    .back-btn {
      background-color: var(--orange);
      color: var(--white);
      border: none;
      padding: 0.6rem 2rem;
      border-radius: 10px;
      font-size: 1rem;
      cursor: pointer;
      margin-bottom: 1.5rem;
      font-weight: bold;
    }
    .back-btn:hover { background-color: #a82509; }
    .signature {
      position: fixed;
      bottom: 1rem;
      left: 1rem;
    }
    .created-by {
      font-family: 'Dancing Script', sans-serif;
      font-size: 13px;
      color: var(--yellow);
    }
    .author {
      font-family: 'Share Tech', sans-serif;
      font-size: 12px;
      color: var(--white);
      display: flex;
      align-items: center;
      gap: 0.4rem;
    }
    .author-photo {
      width: 45px;
      height: 45px;
      border-radius: 50%;
      object-fit: cover;
    }
  </style>
</head>
<body>
  <div class="container">
    <button class="back-btn" onclick="window.location.href='/'">← Analyze Another</button>
    <div class="header">
      <div class="risk-center">
        <div class="risk-label" id="riskLabel">--</div>
        <div class="risk-score" id="riskScore">--/100</div>
      </div>
      <div class="title-right">
        <div class="truth-detector-block">
          <div class="truth-field">TRUTH FIELD</div>
          <div class="detector">DETECTOR</div>
        </div>
        <img src="/static/logo2venado.png" alt="Venado Detective" class="deer-right">
      </div>
    </div>
    <div class="risk-indicators">
      <div class="indicator">
        <span class="indicator-icon">😱</span>
        <strong>EMOTIONAL LANGUAGE</strong>
        <div class="tags" id="emotionalTags"></div>
      </div>
      <div class="indicator">
        <span class="indicator-icon">⚠️</span>
        <strong>ABSOLUTIST CLAIMS</strong>
        <div class="tags" id="absolutistTags"></div>
      </div>
      <div class="indicator">
        <span class="indicator-icon">🤓</span>
        <strong>MISSING CITATIONS</strong>
        <div class="tags" id="citationsTags"></div>
      </div>
      <div class="indicator">
        <span class="indicator-icon">🔍</span>
        <strong>EXPLANATION</strong>
      </div>
    </div>
    <div class="explanation" id="explanation">Loading...</div>
  </div>
  <div class="signature">
    <div class="created-by">Created by</div>
    <div class="author">
      <img src="/static/eloisa_flores_foto.png" alt="Eloisa Flores" class="author-photo">
      Eloisa Flores
    </div>
  </div>
  <script>
    const data = JSON.parse(sessionStorage.getItem('result') || '{}');
    if (!data.risk_level) { window.location.href = '/'; }

    const label = document.getElementById('riskLabel');
    label.textContent = data.risk_level + ' RISK';
    label.className = 'risk-label ' + data.risk_level;

    document.getElementById('riskScore').textContent = data.score + '/100';
    document.getElementById('explanation').textContent = data.explanation || '';

    function makeTags(items, containerId) {
      const el = document.getElementById(containerId);
      if (!items || items.length === 0) {
        el.innerHTML = '<span style="opacity:0.5;font-size:13px">None detected</span>';
        return;
      }
      el.innerHTML = items.map(i => `<span class="tag">${i}</span>`).join('');
    }

    makeTags(data.emotional_language, 'emotionalTags');
    makeTags(data.absolutist_claims, 'absolutistTags');

    const citEl = document.getElementById('citationsTags');
    citEl.innerHTML = data.missing_citations 
      ? '<span class="tag">Yes — no sources found</span>'
      : '<span class="tag" style="background:#2a7a2a">No — sources present</span>';
  </script>
  <script>
async function speakResults(text) {
    try {
        const response = await fetch('/speak', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({text: text})
        });
        const data = await response.json();
        if (data.audio) {
            const audio = new Audio('data:audio/mp3;base64,' + data.audio);
            audio.play();
        }
    } catch(e) {
        console.log('Audio not available:', e);
    }
}

window.addEventListener('load', function() {
    const score = document.getElementById('riskScore')?.innerText || '';
    const label = document.getElementById('riskLabel')?.innerText || '';
    const explanation = document.querySelector('.explanation-box')?.innerText || '';
    if (score && label) {
        const text = `Analysis complete. ${label} detected. Score ${score}. ${explanation}`;
        speakResults(text);
    }
});
</script>
</body>
</html>'''

@app.route('/')
def home():
    return render_template_string(PAGE1)

@app.route('/results')
def results():
    return render_template_string(PAGE2)

@app.route('/analyze', methods=['POST'])
def analyze():
    input_text = request.json.get('text', '').strip()
    
    # Check if it's a URL
    if input_text.startswith('http://') or input_text.startswith('https://'):
        fetched = fetch_url_text(input_text)
        if fetched:
            text_to_analyze = fetched
        else:
            return jsonify({'error': 'Could not read URL'})
    else:
        text_to_analyze = input_text

    prompt = f"""You are TruthField, a narrative risk analyzer.
Analyze this text and return ONLY a valid JSON object with these exact fields:
- risk_level: exactly "LOW", "MEDIUM", or "HIGH"
- score: integer from 0 to 100
- emotional_language: array of strings (emotional words found, max 5)
- absolutist_claims: array of strings (absolute statements found, max 3)
- missing_citations: boolean true or false
- explanation: one clear sentence summarizing the risk

Text to analyze:
{text_to_analyze[:2000]}

Respond ONLY with valid JSON. No markdown. No backticks. No explanation."""

    try:
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
        clean = text_response.strip().replace('```json','').replace('```','').strip()
        data = json.loads(clean)
        return jsonify(data)
    except Exception as e:
        return jsonify({
            "risk_level": "MEDIUM",
            "score": 50,
            "emotional_language": [],
            "absolutist_claims": [],
            "missing_citations": True,
            "explanation": "Analysis completed with limited data."
        })
@app.route('/speak', methods=['POST'])
def speak():
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        import boto3
        bedrock = boto3.client(
            service_name='bedrock-runtime',
            region_name='us-east-1'
        )
        
        body = json.dumps({
            "voice": "tiffany",
            "text": text,
            "responseFormat": "mp3"
        })
        
        response = bedrock.invoke_model(
            modelId='amazon.nova-sonic-v1:0',
            body=body,
            contentType='application/json',
            accept='audio/mpeg'
        )
        
        audio_bytes = response['body'].read()
        audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
        
        return jsonify({"audio": audio_base64})
    
    except Exception as e:
        print(f"SPEAK ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)






