
import google.generativeai as genai
import argparse
import os

try:
    parser = argparse.ArgumentParser(description='List available Gemini models.')
    parser.add_argument('--api_key', help='Your Gemini API Key', required=True)
    args = parser.parse_args()

    genai.configure(api_key=args.api_key)

    print("Finding available models that support 'generateContent':")
    for m in genai.list_models():
      if 'generateContent' in m.supported_generation_methods:
        print(f"- {m.name}")
except Exception as e:
    print(f"An error occurred: {e}")
