import requests
import sys

def test_openai(api_key):
    """Test if API key is from OpenAI"""
    try:
        headers = {"Authorization": f"Bearer {api_key}"}
        response = requests.get("https://api.openai.com/v1/models", headers=headers, timeout=5)
        if response.status_code == 200:
            models = [model['id'] for model in response.json().get('data', [])]
            return True, "OpenAI", models
        return False, None, []
    except:
        return False, None, []

def test_anthropic(api_key):
    """Test if API key is from Anthropic (Claude)"""
    try:
        headers = {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        data = {"model": "claude-3-haiku-20240307", "max_tokens": 1, "messages": [{"role": "user", "content": "Hi"}]}
        response = requests.post("https://api.anthropic.com/v1/messages", headers=headers, json=data, timeout=5)
        if response.status_code in [200, 400]:
            # Anthropic doesn't have a models endpoint, return known models
            models = ["claude-3-5-sonnet-20241022", "claude-3-5-haiku-20241022", "claude-3-opus-20240229", 
                     "claude-3-sonnet-20240229", "claude-3-haiku-20240307"]
            return True, "Anthropic (Claude)", models
        return False, None, []
    except:
        return False, None, []

def test_google_ai(api_key):
    """Test if API key is from Google AI (Gemini)"""
    try:
        url = f"https://generativelanguage.googleapis.com/v1/models?key={api_key}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            models = [model['name'].replace('models/', '') for model in response.json().get('models', [])]
            return True, "Google AI (Gemini)", models
        return False, None, []
    except:
        return False, None, []

def test_huggingface(api_key):
    """Test if API key is from HuggingFace"""
    try:
        headers = {"Authorization": f"Bearer {api_key}"}
        response = requests.get("https://huggingface.co/api/whoami", headers=headers, timeout=5)
        if response.status_code == 200:
            models = ["Access to all HuggingFace models via Inference API"]
            return True, "HuggingFace", models
        return False, None, []
    except:
        return False, None, []

def test_cohere(api_key):
    """Test if API key is from Cohere"""
    try:
        headers = {"Authorization": f"Bearer {api_key}"}
        response = requests.get("https://api.cohere.ai/v1/check-api-key", headers=headers, timeout=5)
        if response.status_code == 200:
            models = ["command-r-plus", "command-r", "command", "command-light", "embed-english-v3.0", "embed-multilingual-v3.0"]
            return True, "Cohere", models
        return False, None, []
    except:
        return False, None, []

def test_replicate(api_key):
    """Test if API key is from Replicate"""
    try:
        headers = {"Authorization": f"Token {api_key}"}
        response = requests.get("https://api.replicate.com/v1/account", headers=headers, timeout=5)
        if response.status_code == 200:
            models = ["Access to all Replicate models (meta/llama-2, stability-ai/sdxl, etc.)"]
            return True, "Replicate", models
        return False, None, []
    except:
        return False, None, []

def test_stability_ai(api_key):
    """Test if API key is from Stability AI"""
    try:
        headers = {"Authorization": f"Bearer {api_key}"}
        response = requests.get("https://api.stability.ai/v1/user/account", headers=headers, timeout=5)
        if response.status_code == 200:
            models = ["stable-diffusion-xl-1024-v1-0", "stable-diffusion-v1-6", "stable-diffusion-xl-beta-v2-2-2"]
            return True, "Stability AI", models
        return False, None, []
    except:
        return False, None, []

def identify_api_key(api_key):
    """Test API key against multiple services"""
    print(f"Testing API key: {api_key[:8]}...{api_key[-4:]}")
    print("-" * 50)
    
    tests = [
        test_openai,
        test_anthropic,
        test_google_ai,
        test_huggingface,
        test_cohere,
        test_replicate,
        test_stability_ai
    ]
    
    for test_func in tests:
        service_name = test_func.__doc__.split("from ")[-1].strip("\"")
        print(f"Testing {service_name}...", end=" ")
        is_valid, provider, models = test_func(api_key)
        if is_valid:
            print(f"✓ MATCH!")
            return provider, models
        print("✗")
    
    print("\nNo matching service found.")
    return None, []

if __name__ == "__main__":
    if len(sys.argv) > 1:
        api_key = sys.argv[1]
    else:
        api_key = input("Enter your API key: ").strip()
    
    if not api_key:
        print("Error: No API key provided")
        sys.exit(1)
    
    result, models = identify_api_key(api_key)
    
    if result:
        print(f"\n🎉 Your API key is from: {result}")
        print(f"\n📋 Available models ({len(models)}):")
        for i, model in enumerate(models[:20], 1):  # Show first 20 models
            print(f"  {i}. {model}")
        if len(models) > 20:
            print(f"  ... and {len(models) - 20} more models")
    else:
        print("\n❌ Could not identify the API key provider.")
        print("It might be from a service not tested, or the key might be invalid.")
