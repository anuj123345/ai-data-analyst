"""
Quick test script to verify Together AI API key
Usage: python test_together_api.py
"""

from together import Together

def test_api_key():
    # Paste your Together AI API key here
    api_key = input("Enter your Together AI API key: ").strip()
    
    if not api_key:
        print("❌ No API key provided!")
        return
    
    try:
        print("\n🔄 Testing API key...")
        client = Together(api_key=api_key)
        
        # Simple test call
        response = client.chat.completions.create(
            model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
            messages=[{"role": "user", "content": "Say 'Hello World' in one word"}],
            max_tokens=10
        )
        
        result = response.choices[0].message.content
        print(f"\n✅ API Key works! Response: {result}")
        print("\n✨ Your API key is valid and working correctly!")
        
    except Exception as e:
        print(f"\n❌ API Key test failed!")
        print(f"Error: {str(e)}")
        
        if "401" in str(e) or "Invalid API key" in str(e):
            print("\n💡 Solutions:")
            print("1. Double-check your API key at https://api.together.ai/settings/api-keys")
            print("2. Make sure you copied the entire key")
            print("3. Try creating a new API key")
            print("4. Ensure your account has credits/quota available")
        elif "403" in str(e):
            print("\n💡 Your account might not have access to this model")
        else:
            print("\n💡 Check your internet connection and try again")

if __name__ == "__main__":
    print("=" * 60)
    print("Together AI API Key Tester")
    print("=" * 60)
    test_api_key()
