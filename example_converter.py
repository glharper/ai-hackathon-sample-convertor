#!/usr/bin/env python3
"""
Example implementation of convert_text function with more sophisticated conversion logic.

This file shows how the convert_text function could be implemented with
more advanced Python-to-JavaScript conversion patterns.
"""

import re
from typing import Dict, List, Tuple


def convert_text_advanced(text: str, lib_name: str, ref_url: str) -> str:
    """
    Advanced implementation of Python to JavaScript conversion.
    
    This is an example of how the convert_text function could be implemented
    with more sophisticated conversion logic.
    
    Args:
        text: Python source code to convert
        lib_name: JavaScript library name to use
        ref_url: URL to API reference documentation
        
    Returns:
        Converted JavaScript code
    """
    converter = AdvancedPythonToJsConverter(lib_name, ref_url)
    return converter.convert(text)


class AdvancedPythonToJsConverter:
    """Advanced Python to JavaScript converter with sophisticated pattern matching."""
    
    def __init__(self, lib_name: str, ref_url: str):
        self.lib_name = lib_name
        self.ref_url = ref_url
        self.imports_needed = set()
        self.is_async_needed = False
    
    def convert(self, python_code: str) -> str:
        """Convert Python code to JavaScript."""
        # Reset state
        self.imports_needed.clear()
        self.is_async_needed = False
        
        js_code = python_code
        
        # Step 1: Convert basic syntax
        js_code = self._convert_basic_syntax(js_code)
        
        # Step 2: Convert control structures
        js_code = self._convert_control_structures(js_code)
        
        # Step 3: Convert functions and classes
        js_code = self._convert_functions_and_classes(js_code)
        
        # Step 4: Convert library-specific patterns
        js_code = self._convert_library_patterns(js_code)
        
        # Step 5: Add imports and setup
        js_code = self._add_imports_and_setup(js_code)
        
        # Step 6: Format and clean up
        js_code = self._format_and_cleanup(js_code)
        
        return js_code
    
    def _convert_basic_syntax(self, code: str) -> str:
        """Convert basic Python syntax to JavaScript."""
        # Comments
        code = re.sub(r'#(.+)', r'//$1', code)
        
        # Print statements
        code = re.sub(r'\bprint\s*\(', 'console.log(', code)
        
        # Boolean values
        code = re.sub(r'\bTrue\b', 'true', code)
        code = re.sub(r'\bFalse\b', 'false', code)
        code = re.sub(r'\bNone\b', 'null', code)
        
        # Logical operators
        code = re.sub(r'\band\b', '&&', code)
        code = re.sub(r'\bor\b', '||', code)
        code = re.sub(r'\bnot\b', '!', code)
        
        # String formatting (f-strings)
        code = re.sub(r'f"([^"]*\{[^}]*\}[^"]*)"', self._convert_fstring, code)
        code = re.sub(r"f'([^']*\{[^}]*\}[^']*)'", self._convert_fstring, code)
        
        # Dictionary/object syntax
        code = re.sub(r"'(\w+)':", r'"\1":', code)  # Convert single quotes to double in object keys
        
        # List/array methods
        code = re.sub(r'\.append\(', '.push(', code)
        code = re.sub(r'\.extend\(', '.push(...', code)
        
        # String methods
        code = re.sub(r'\.strip\(\)', '.trim()', code)
        code = re.sub(r'\.lower\(\)', '.toLowerCase()', code)
        code = re.sub(r'\.upper\(\)', '.toUpperCase()', code)
        
        # Length function
        code = re.sub(r'\blen\(([^)]+)\)', r'\1.length', code)
        
        return code
    
    def _convert_fstring(self, match) -> str:
        """Convert f-string to template literal."""
        content = match.group(1)
        # Convert {variable} to ${variable}
        js_template = re.sub(r'\{([^}]+)\}', r'${\1}', content)
        return f'`{js_template}`'
    
    def _convert_control_structures(self, code: str) -> str:
        """Convert control structures (if, for, while, try/catch)."""
        lines = code.split('\n')
        converted_lines = []
        indent_stack = []
        
        for line in lines:
            stripped = line.strip()
            indent = len(line) - len(line.lstrip())
            
            # Handle closing braces for decreased indentation
            while indent_stack and indent < indent_stack[-1]:
                indent_stack.pop()
                converted_lines.append(' ' * (len(indent_stack) * 2) + '}')
            
            if not stripped:
                converted_lines.append(line)
                continue
            
            # Convert control structures
            if stripped.startswith('if ') and stripped.endswith(':'):
                condition = stripped[3:-1].strip()
                converted_lines.append(' ' * indent + f'if ({condition}) {{')
                indent_stack.append(indent)
                
            elif stripped.startswith('elif ') and stripped.endswith(':'):
                condition = stripped[5:-1].strip()
                converted_lines.append(' ' * indent + f'}} else if ({condition}) {{')
                
            elif stripped == 'else:':
                converted_lines.append(' ' * indent + '} else {')
                
            elif stripped.startswith('for ') and ' in ' in stripped and stripped.endswith(':'):
                # Parse for loop
                for_part = stripped[4:-1].strip()
                if ' in range(' in for_part:
                    # for i in range(n) -> for (let i = 0; i < n; i++)
                    var_match = re.match(r'(\w+)\s+in\s+range\(([^)]+)\)', for_part)
                    if var_match:
                        var_name, range_expr = var_match.groups()
                        converted_lines.append(f'{" " * indent}for (let {var_name} = 0; {var_name} < {range_expr}; {var_name}++) {{')
                        indent_stack.append(indent)
                else:
                    # for item in iterable -> for (const item of iterable)
                    parts = for_part.split(' in ', 1)
                    if len(parts) == 2:
                        var_name, iterable = parts
                        converted_lines.append(f'{" " * indent}for (const {var_name.strip()} of {iterable.strip()}) {{')
                        indent_stack.append(indent)
                        
            elif stripped.startswith('while ') and stripped.endswith(':'):
                condition = stripped[6:-1].strip()
                converted_lines.append(' ' * indent + f'while ({condition}) {{')
                indent_stack.append(indent)
                
            elif stripped.startswith('try:'):
                converted_lines.append(' ' * indent + 'try {')
                indent_stack.append(indent)
                
            elif stripped.startswith('except'):
                if ':' in stripped:
                    exception_part = stripped[6:stripped.find(':')].strip()
                    if exception_part:
                        converted_lines.append(' ' * indent + f'}} catch ({exception_part.split()[0].lower()}) {{')
                    else:
                        converted_lines.append(' ' * indent + '} catch (error) {')
                        
            elif stripped == 'finally:':
                converted_lines.append(' ' * indent + '} finally {')
                
            else:
                converted_lines.append(line)
        
        # Close any remaining braces
        while indent_stack:
            indent_stack.pop()
            converted_lines.append(' ' * (len(indent_stack) * 2) + '}')
        
        return '\n'.join(converted_lines)
    
    def _convert_functions_and_classes(self, code: str) -> str:
        """Convert function and class definitions."""
        # Function definitions
        code = re.sub(
            r'def\s+(\w+)\s*\(([^)]*)\)\s*:',
            self._convert_function_def,
            code
        )
        
        # Class definitions
        code = re.sub(
            r'class\s+(\w+)(?:\([^)]*\))?\s*:',
            r'class \1 {',
            code
        )
        
        # Method definitions (within classes)
        code = re.sub(
            r'(\s+)def\s+(\w+)\s*\(self(?:,\s*([^)]*))?\)\s*:',
            r'\1\2(\3) {',
            code
        )
        
        # Constructor
        code = re.sub(
            r'(\s+)def\s+__init__\s*\(self(?:,\s*([^)]*))?\)\s*:',
            r'\1constructor(\2) {',
            code
        )
        
        return code
    
    def _convert_function_def(self, match) -> str:
        """Convert function definition."""
        func_name = match.group(1)
        params = match.group(2)
        
        # Clean up parameters (remove default values for simplicity)
        js_params = []
        if params:
            for param in params.split(','):
                param = param.strip()
                if '=' in param:
                    param = param.split('=')[0].strip()
                js_params.append(param)
        
        params_str = ', '.join(js_params)
        
        # Check if function might need to be async
        if 'requests.' in match.string or 'async' in match.string:
            self.is_async_needed = True
            return f'async function {func_name}({params_str}) {{'
        else:
            return f'function {func_name}({params_str}) {{'
    
    def _convert_library_patterns(self, code: str) -> str:
        """Convert library-specific patterns."""
        if 'requests.' in code:
            self.imports_needed.add('axios')
            self.is_async_needed = True
            
            # Convert requests calls
            code = re.sub(r'requests\.get\(([^)]+)\)', r'await axios.get(\1)', code)
            code = re.sub(r'requests\.post\(([^)]+)\)', r'await axios.post(\1)', code)
            code = re.sub(r'\.status_code', '.status', code)
            code = re.sub(r'\.text', '.data', code)
        
        if 'json.' in code:
            code = re.sub(r'json\.loads\(([^)]+)\)', r'JSON.parse(\1)', code)
            code = re.sub(r'json\.dumps\(([^)]+)\)', r'JSON.stringify(\1)', code)
        
        # Azure SDK specific patterns
        if self.lib_name.startswith('@azure/'):
            self.imports_needed.add(self.lib_name)
            self.imports_needed.add('@azure/identity')
            
            # Add client creation patterns
            if 'client' not in code and any(pattern in code for pattern in ['get', 'post', 'create', 'list']):
                code = f"const client = new {self._get_client_class()}(endpoint, credential);\n\n" + code
        
        return code
    
    def _get_client_class(self) -> str:
        """Get the appropriate client class name for the library."""
        client_mappings = {
            '@azure/ai-agents': 'AgentsClient',
            '@azure/openai': 'OpenAIClient',
            '@azure/storage-blob': 'BlobServiceClient',
            '@azure/cosmos': 'CosmosClient'
        }
        return client_mappings.get(self.lib_name, 'Client')
    
    def _add_imports_and_setup(self, code: str) -> str:
        """Add necessary imports and setup code."""
        imports = []
        
        # Add library imports
        if self.lib_name in self.imports_needed:
            client_class = self._get_client_class()
            imports.append(f"const {{ {client_class} }} = require('{self.lib_name}');")
        
        if '@azure/identity' in self.imports_needed:
            imports.append("const { DefaultAzureCredential } = require('@azure/identity');")
        
        if 'axios' in self.imports_needed:
            imports.append("const axios = require('axios');")
        
        # Add common Node.js imports if needed
        if 'fs.' in code or 'file' in code.lower():
            imports.append("const fs = require('fs');")
        
        if 'path.' in code or 'os.path' in code:
            imports.append("const path = require('path');")
        
        if imports:
            import_section = '\n'.join(imports) + '\n\n'
            
            # Add credential setup for Azure
            if '@azure/identity' in self.imports_needed:
                import_section += "const credential = new DefaultAzureCredential();\n"
                import_section += "const endpoint = process.env.AZURE_ENDPOINT || 'https://your-resource.azure.com';\n\n"
            
            code = import_section + code
        
        return code
    
    def _format_and_cleanup(self, code: str) -> str:
        """Format and clean up the generated JavaScript code."""
        # Add header comment
        header = f"""// Converted from Python to JavaScript
// Target library: {self.lib_name}
// API Reference: {self.ref_url}
// Generated on: {self._get_timestamp()}

"""
        
        # Clean up extra whitespace
        code = re.sub(r'\n\s*\n\s*\n', '\n\n', code)
        code = code.strip()
        
        # Wrap in main function if needed and not already wrapped
        if not re.search(r'function\s+\w+|class\s+\w+|module\.exports', code):
            if self.is_async_needed:
                code = f"async function main() {{\n{self._indent_code(code, 2)}\n}}\n\nmain().catch(console.error);"
            else:
                code = f"function main() {{\n{self._indent_code(code, 2)}\n}}\n\nmain();"
        
        return header + code
    
    def _indent_code(self, code: str, spaces: int) -> str:
        """Indent code by specified number of spaces."""
        lines = code.split('\n')
        indented_lines = []
        for line in lines:
            if line.strip():  # Don't indent empty lines
                indented_lines.append(' ' * spaces + line)
            else:
                indented_lines.append(line)
        return '\n'.join(indented_lines)
    
    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# Example usage
if __name__ == '__main__':
    sample_python = '''
import json
import requests

def fetch_user_data(user_id):
    """Fetch user data from API."""
    url = f"https://api.example.com/users/{user_id}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = json.loads(response.text)
        print(f"User: {data['name']}")
        return data
    else:
        print("Failed to fetch user")
        return None

# Main execution
if __name__ == "__main__":
    for i in range(3):
        user = fetch_user_data(i + 1)
        if user is not None:
            print(f"Email: {user['email']}")
    '''
    
    print("Advanced Python to JavaScript Conversion Example")
    print("=" * 60)
    print("INPUT:")
    print(sample_python)
    print("\n" + "=" * 60)
    print("OUTPUT:")
    
    result = convert_text_advanced(
        sample_python,
        "@azure/ai-agents",
        "https://docs.microsoft.com/api"
    )
    
    print(result)
