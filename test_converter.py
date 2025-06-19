#!/usr/bin/env python3
"""
Test script for the Python to JavaScript converter.

This script demonstrates how to use the converter programmatically
and provides examples of the expected inputs and outputs.
"""

import asyncio
from converter import PythonToJsConverter, convert_text


def test_convert_text():
    """Test the convert_text function with sample Python code."""
    
    sample_python_code = '''
import json
import requests

def get_user_data(user_id):
    """Fetch user data from API."""
    url = f"https://api.example.com/users/{user_id}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = json.loads(response.text)
        print(f"User name: {data['name']}")
        return data
    else:
        print("Failed to fetch user data")
        return None

# Example usage
if __name__ == "__main__":
    user = get_user_data(123)
    if user is not None:
        print(f"Email: {user['email']}")
    '''
    
    print("Testing convert_text function...")
    print("=" * 50)
    print("INPUT (Python code):")
    print(sample_python_code)
    print("\n" + "=" * 50)
    print("OUTPUT (JavaScript code):")
    
    js_code = convert_text(
        text=sample_python_code,
        lib_name="@azure/ai-agents",
        ref_url="https://docs.microsoft.com/api"
    )
    
    print(js_code)
    print("=" * 50)


async def test_converter_class():
    """Test the PythonToJsConverter class with a mock repository."""
    
    print("\nTesting PythonToJsConverter class...")
    print("=" * 50)
    
    # Example usage (this would normally fetch from a real repository)
    converter = PythonToJsConverter()
    
    # For demonstration, we'll show what the input parameters would be:
    example_inputs = {
        'repo_url': 'https://github.com/Azure-Samples/azure-ai-samples/tree/main/scenarios/agents/python',
        'js_library': '@azure/ai-agents',
        'api_docs_url': 'https://docs.microsoft.com/en-us/javascript/api/@azure/ai-agents/'
    }
    
    print("Example inputs for the converter:")
    for key, value in example_inputs.items():
        print(f"  {key}: {value}")
    
    print("\nTo use the converter with real data, you would call:")
    print("samples = await converter.convert_samples(repo_url, js_library, api_docs_url)")
    print("converter.save_samples_to_zip(samples, 'output.zip')")


def test_cli_examples():
    """Show examples of CLI usage."""
    
    print("\nCLI Usage Examples:")
    print("=" * 50)
    
    examples = [
        "python converter.py https://github.com/user/repo/tree/main/samples",
        "python converter.py https://github.com/user/repo/tree/main/samples --library @azure/ai-agents",
        "python converter.py https://github.com/user/repo/tree/main/samples --library @azure/openai --docs https://docs.microsoft.com/api",
        "python converter.py https://github.com/user/repo/tree/main/samples --output converted_samples.zip",
        "python converter.py https://github.com/user/repo/tree/main/samples --output ./js_samples/ --verbose"
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"{i}. {example}")
    
    print("\nFor help and all options:")
    print("python converter.py --help")


async def main():
    """Run all tests."""
    print("Python to JavaScript Converter - Test Suite")
    print("=" * 60)
    
    # Test the convert_text function
    test_convert_text()
    
    # Test the converter class
    await test_converter_class()
    
    # Show CLI examples
    test_cli_examples()
    
    print("\n" + "=" * 60)
    print("Test completed! Ready to implement actual conversion logic in convert_text()")


if __name__ == '__main__':
    asyncio.run(main())
