import boto3
import json

client = boto3.client(service_name='bedrock-runtime', region_name='us-east-1')

def analyze_text(text):
    prompt = f"""You are TruthField, a narrative risk analyzer.
Analyze this text and return a JSON with:
- risk_level: LOW, MEDIUM, or HIGH
- score: number from 0 to 100
- emotional_language: list of emotional words found
- absolutist_claims: list of absolute statements found
- missing_citations: true or false
- explanation: one sentence summary

Text to analyze: {text}

Respond ONLY with valid JSON, nothing else."""

    response = client.invoke_model(
        modelId='amazon.nova-lite-v1:0',
        body=json.dumps({
            "messages": [
                {"role": "user", "content": [{"text": prompt}]}
            ]
        })
    )
    
    result = json.loads(response['body'].read())
    return result['output']['message']['content'][0]['text']

# Test
text = "All scientists agree this is the biggest crisis humanity has ever faced!"
print("Analyzing...")
print(analyze_text(text))
