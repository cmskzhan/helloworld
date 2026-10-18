import sys
from google import genai
import getpass

def list_models():
    print("--- Gemini Model Discovery Tool ---")
    api_key = getpass.getpass("Enter your Gemini API Key: ")
    if not api_key:
        print("Error: API Key is required.")
        return

    try:
        client = genai.Client(api_key=api_key)
        print("\nFetching available models...\n")
        models = client.models.list()
        
        print(f"{'Model Name':<40} | {'Supported Methods'}")
        print("-" * 70)
        
        found_any = False
        for m in models:
            methods = ", ".join(m.supported_generation_methods)
            print(f"{m.name:<40} | {methods}")
            found_any = True
            
        if not found_any:
            print("No models found for this API key.")
            
    except Exception as e:
        print(f"\nError: {e}")
        print("\nCommon fixes:")
        print("1. Check if your API key is correct.")
        print("2. Ensure the 'google-genai' package is up to date.")
        print("3. Check your internet connection.")

if __name__ == "__main__":
    list_models()
