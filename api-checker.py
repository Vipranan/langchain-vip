import os

try:
    import google.generativeai as genai
except ImportError:
    print("⚠️  Missing dependency: google-generative-ai")
    print("Install with: pip install google-generative-ai")
    import sys
    sys.exit(1)

# Configure with your API key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("⚠️  Environment variable GOOGLE_API_KEY is not set.")
    print("Set it with: export GOOGLE_API_KEY='your-key-here'")
    import sys
    sys.exit(1)

genai.configure(api_key=api_key)

# List available models
print("Fetching available models...")
try:
    models = genai.list_models()
    model_count = 0
    for model in models:
        # Filter models that support text generation
        methods = getattr(model, "supported_generation_methods", None)
        if methods and "generateContent" in methods:
            name = getattr(model, "name", "<unknown>")
            print(f"  ✓ {name}")
            model_count += 1
    print(f"\nFound {model_count} text generation models.")
except Exception as e:
    print(f"✗ Error listing models: {e}")
    import sys
    sys.exit(1)