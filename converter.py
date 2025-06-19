#!/usr/bin/env python3
"""
Python to JavaScript Sample Converter

A command-line tool that converts Python code samples to JavaScript,
designed for porting repository samples to use JavaScript libraries.
"""

import argparse
import asyncio
import aiohttp
import json
import os
import sys
import zipfile
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from urllib.parse import urlparse
import tempfile
import shutil
import os, time
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import ListSortOrder


class RepositoryFetcher:
    """Fetches Python samples from GitHub repositories."""
    
    def __init__(self):
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            headers={'User-Agent': 'Python-to-JS-Converter'}
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def fetch_python_samples(self, repo_url: str) -> List[Dict[str, str]]:
        """
        Fetch Python samples from a GitHub repository URL.
        
        Args:
            repo_url: GitHub repository URL
            
        Returns:
            List of dictionaries containing file info: {name, content, path}
        """
        print(f"Fetching Python samples from: {repo_url}")
        
        try:
            api_url = self._convert_to_api_url(repo_url)
            print(f"API URL: {api_url}")
            
            python_files = []
            await self._fetch_directory_contents(api_url, python_files)
            
            print(f"Found {len(python_files)} Python files")
            return python_files
            
        except Exception as e:
            print(f"Error fetching Python samples: {e}")
            raise
    
    def _convert_to_api_url(self, github_url: str) -> str:
        """Convert GitHub URL to API URL."""
        url = github_url.strip()
        
        if 'github.com' in url:
            # Extract owner, repo, and path from URL
            parts = url.replace('https://github.com/', '').replace('http://github.com/', '')
            path_parts = parts.split('/')
            
            if len(path_parts) < 2:
                raise ValueError("Invalid GitHub URL format")
            
            owner = path_parts[0]
            repo = path_parts[1].replace('.git', '')
            
            # Handle tree/branch URLs
            if len(path_parts) > 2 and path_parts[2] == 'tree':
                # Skip 'tree' and branch name
                api_path = '/' + '/'.join(path_parts[4:]) if len(path_parts) > 4 else ''
            else:
                api_path = '/' + '/'.join(path_parts[2:]) if len(path_parts) > 2 else ''
            
            return f"https://api.github.com/repos/{owner}/{repo}/contents{api_path}"
        
        if 'api.github.com' in url:
            return url
        
        raise ValueError("Unsupported URL format. Please use a GitHub repository URL.")
    
    async def _fetch_directory_contents(self, api_url: str, python_files: List[Dict[str, str]]):
        """Recursively fetch directory contents."""
        try:
            async with self.session.get(api_url) as response:
                if response.status == 404:
                    raise ValueError("Repository or path not found")
                elif response.status == 403:
                    raise ValueError("Access denied or rate limited")
                elif response.status != 200:
                    raise ValueError(f"HTTP {response.status}: {await response.text()}")
                
                files = await response.json()
                
                for file_info in files:
                    if file_info['type'] == 'file' and file_info['name'].endswith('.py'):
                        print(f"Found Python file: {file_info['name']}")
                        
                        # Fetch file content
                        async with self.session.get(file_info['download_url']) as content_response:
                            if content_response.status == 200:
                                content = await content_response.text()
                                python_files.append({
                                    'name': file_info['name'],
                                    'content': content,
                                    'path': file_info['path']
                                })
                    
                    elif file_info['type'] == 'dir':
                        # Recursively fetch from subdirectories
                        try:
                            await self._fetch_directory_contents(file_info['url'], python_files)
                        except Exception as e:
                            print(f"Warning: Failed to fetch from subdirectory {file_info['name']}: {e}")
        
        except Exception as e:
            print(f"Error fetching directory contents: {e}")
            raise


class ApiDocParser:
    """Parses API documentation to discover JavaScript library methods."""
    
    def __init__(self):
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            headers={'User-Agent': 'Python-to-JS-Converter'}
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def parse_api_methods(self, docs_url: str) -> List[Dict[str, str]]:
        """
        Parse API documentation to discover available methods.
        
        Args:
            docs_url: URL to API documentation
            
        Returns:
            List of method information dictionaries
        """
        if not docs_url:
            return []
        
        print(f"Parsing API documentation from: {docs_url}")
        
        try:
            async with self.session.get(docs_url) as response:
                if response.status != 200:
                    print(f"Warning: Failed to fetch API docs (HTTP {response.status})")
                    return []
                
                content = await response.text()
                methods = self._extract_methods_from_html(content)
                
                print(f"Found {len(methods)} API methods")
                return methods[:50]  # Limit to prevent overwhelming
                
        except Exception as e:
            print(f"Warning: Failed to parse API documentation: {e}")
            return []
    
    def _extract_methods_from_html(self, html_content: str) -> List[Dict[str, str]]:
        """Extract method information from HTML content."""
        # Placeholder implementation - would use BeautifulSoup in real implementation
        methods = []
        
        # Basic pattern matching for common documentation formats
        import re
        
        # Look for method patterns in the HTML
        method_patterns = [
            r'<h[2-4][^>]*>([a-zA-Z_][a-zA-Z0-9_]*)\s*\(',  # Headers with method names
            r'<code[^>]*>([a-zA-Z_][a-zA-Z0-9_]*)\s*\(',     # Code blocks with methods
            r'function\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(',     # Function definitions
        ]
        
        for pattern in method_patterns:
            matches = re.findall(pattern, html_content, re.IGNORECASE)
            for match in matches:
                if len(match) < 50:  # Reasonable method name length
                    methods.append({
                        'name': match,
                        'description': 'Method discovered from documentation',
                        'signature': f"{match}()"
                    })
        
        # Remove duplicates
        seen = set()
        unique_methods = []
        for method in methods:
            if method['name'] not in seen:
                seen.add(method['name'])
                unique_methods.append(method)
        
        return unique_methods
    
    def get_common_mappings(self, js_library: str) -> Dict[str, str]:
        """Get common Python to JavaScript mappings for a library."""
        mappings = {
            '@azure/ai-agents': {
                'requests.get': 'client.get',
                'requests.post': 'client.post',
                'json.loads': 'JSON.parse',
                'json.dumps': 'JSON.stringify',
                'print': 'console.log',
                'len': 'length',
                'str': 'String',
                'int': 'parseInt',
                'float': 'parseFloat'
            },
            '@azure/openai': {
                'openai.ChatCompletion.create': 'client.getChatCompletions',
                'openai.Completion.create': 'client.getCompletions',
                'requests.post': 'client.post'
            },
            'default': {
                'print': 'console.log',
                'len': 'length',
                'str': 'String',
                'int': 'parseInt',
                'float': 'parseFloat',
                'json.loads': 'JSON.parse',
                'json.dumps': 'JSON.stringify'
            }
        }
        
        return mappings.get(js_library, mappings['default'])


class PythonToJsConverter:
    """Main converter class that orchestrates the conversion process."""
    
    def __init__(self):
        self.repo_fetcher = None
        self.api_parser = None
    
    async def convert_samples(self, repo_url: str, js_library: str, api_docs_url: Optional[str] = None) -> List[Dict[str, str]]:
        """
        Convert Python samples from a repository to JavaScript.
        
        Args:
            repo_url: GitHub repository URL containing Python samples
            js_library: JavaScript library name to use
            api_docs_url: Optional URL to API documentation
            
        Returns:
            List of converted samples with metadata
        """
        print(f"Starting conversion process...")
        print(f"Repository: {repo_url}")
        print(f"JavaScript Library: {js_library}")
        print(f"API Documentation: {api_docs_url or 'None provided'}")
        
        converted_samples = []
        
        async with RepositoryFetcher() as repo_fetcher, ApiDocParser() as api_parser:
            # Step 1: Fetch Python samples
            python_samples = await repo_fetcher.fetch_python_samples(repo_url)
            
            if not python_samples:
                print("No Python samples found in the repository")
                return []
            
            # Step 2: Parse API documentation if provided
            api_methods = []
            if api_docs_url:
                api_methods = await api_parser.parse_api_methods(api_docs_url)
            
            # Step 3: Convert each sample
            for i, sample in enumerate(python_samples, 1):
                print(f"Converting sample {i}/{len(python_samples)}: {sample['name']}")
                if sample['name'] == "__init__.py":
                    continue
                
                try:
                    js_code = await self.convert_single_sample(
                        sample['content'], 
                        js_library, 
                        api_docs_url,
                        api_methods
                    )
                    
                    converted_samples.append({
                        'original_name': sample['name'],
                        'original_path': sample['path'],
                        'js_name': sample['name'].replace('.py', '.js'),
                        'js_code': js_code,
                        'python_code': sample['content']
                    })
                    
                except Exception as e:
                    print(f"Error converting {sample['name']}: {e}")
                    # Include failed conversion with error comment
                    error_js = f"// Error converting {sample['name']}: {e}\n// Original Python code:\n/*\n{sample['content']}\n*/"
                    converted_samples.append({
                        'original_name': sample['name'],
                        'original_path': sample['path'],
                        'js_name': sample['name'].replace('.py', '.js'),
                        'js_code': error_js,
                        'python_code': sample['content']
                    })
        
        print(f"Conversion completed: {len(converted_samples)} samples processed")
        return converted_samples
    
    async def convert_single_sample(self, python_code: str, js_library: str, api_docs_url: Optional[str], api_methods: List[Dict[str, str]]) -> str:
        """
        Convert a single Python code sample to JavaScript.
        
        This method delegates to the convert_text function which should be implemented
        with the actual conversion logic.
        
        Args:
            python_code: Python source code to convert
            js_library: JavaScript library name
            api_docs_url: API documentation URL
            api_methods: List of discovered API methods
            
        Returns:
            Converted JavaScript code
        """
        return convert_text(python_code, js_library, api_docs_url or "")
    
    def save_samples_to_zip(self, samples: List[Dict[str, str]], output_path: str):
        """Save converted samples to a ZIP file."""
        print(f"Saving {len(samples)} samples to {output_path}")
        
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for sample in samples:
                zipf.writestr(sample['js_name'], sample['js_code'])
        
        print(f"ZIP file created: {output_path}")
    
    def save_samples_to_directory(self, samples: List[Dict[str, str]], output_dir: str):
        """Save converted samples to a directory."""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        print(f"Saving {len(samples)} samples to {output_path}")
        
        for sample in samples:
            file_path = output_path / sample['js_name']
            file_path.write_text(sample['js_code'], encoding='utf-8')
        
        print(f"Samples saved to directory: {output_path}")


def convert_text(text: str, lib_name: str, ref_url: str) -> str:
    """
    Convert Python code text to JavaScript.
    
    This is the main conversion function that should be implemented
    with the actual Python-to-JavaScript conversion logic.
    
    Args:
        text: Python source code to convert
        lib_name: JavaScript library name to use
        ref_url: URL to API reference documentation
        
    Returns:
        Converted JavaScript code
        
    TODO: Implement the actual conversion logic here
    """
    # Placeholder implementation - replace with actual conversion logic

    project_client = AIProjectClient(
        endpoint=os.environ["PROJECT_ENDPOINT"],
        credential=DefaultAzureCredential(),
    )

    with project_client:
        agents_client = project_client.agents

        content = f"""
        Convert the python code below to JavaScript using the {lib_name} library and the reference documentation at {ref_url}.
        
        Python code:
        {text}
        """
        # [START create_agent]
        agent = agents_client.create_agent(
            model=os.environ["MODEL_DEPLOYMENT_NAME"],
            name="python-to-js-converter",
            instructions="You are an expert Python to JavaScript code converter that can use reference API documentation for JS libraries to find appropriate methods corresponding to Python methods for the given code.",
        )
        # [END create_agent]
        print(f"Created agent, agent ID: {agent.id}")

        # [START create_thread]
        thread = agents_client.threads.create()
        # [END create_thread]
        print(f"Created thread, thread ID: {thread.id}")

        # List all threads for the agent
        # [START list_threads]
        threads = agents_client.threads.list()
        # [END list_threads]

        # [START create_message]
        message = agents_client.messages.create(thread_id=thread.id, role="user", content=content)
        # [END create_message]
        print(f"Created message, message ID: {message.id}")

        # [START create_run]
        run = agents_client.runs.create(thread_id=thread.id, agent_id=agent.id)

        # Poll the run as long as run status is queued or in progress
        while run.status in ["queued", "in_progress", "requires_action"]:
            # Wait for a second
            time.sleep(1)
            run = agents_client.runs.get(thread_id=thread.id, run_id=run.id)
            # [END create_run]
            print(f"Run status: {run.status}")

        if run.status == "failed":
            print(f"Run error: {run.last_error}")

        agents_client.delete_agent(agent.id)
        print("Deleted agent")

        # [START list_messages]
        messages = agents_client.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING)
        for msg in messages:
            if msg.text_messages:
                js_code = msg.text_messages[-1]
                print(js_code)
        # [END list_messages]
    
 
    return js_code


async def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description='Convert Python code samples to JavaScript',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python converter.py https://github.com/user/repo/tree/main/samples
  python converter.py https://github.com/user/repo/tree/main/samples --library @azure/ai-agents
  python converter.py https://github.com/user/repo/tree/main/samples --library @azure/openai --docs https://docs.microsoft.com/api
  python converter.py https://github.com/user/repo/tree/main/samples --output converted_samples.zip
        """
    )
    
    parser.add_argument(
        'repo_url',
        default='https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-agents/samples/agents_multiagent',
        help='URL to GitHub repository subfolder containing Python samples'
    )
    
    parser.add_argument(
        '--library', '-l',
        default='@azure/ai-agents',
        help='JavaScript library name (default: @azure/ai-agents)'
    )
    
    parser.add_argument(
        '--docs', '-d',
        default='https://learn.microsoft.com/en-us/javascript/api/@azure/ai-agents/?view=azure-node-preview',
        help='URL to API reference documentation for the JavaScript library'
    )
    
    parser.add_argument(
        '--output', '-o',
        help='Output file (.zip) or directory path (default: js-samples.zip)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        print("Verbose mode enabled")
        print(f"Arguments: {vars(args)}")
    
    try:
        # Initialize converter
        converter = PythonToJsConverter()
        
        # Convert samples
        samples = await converter.convert_samples(
            args.repo_url,
            args.library,
            args.docs
        )
        
        if not samples:
            print("No samples to convert")
            return 1
        
        # Determine output path
        output_path = args.output or 'js-samples.zip'
        
        # Save results
        if output_path.endswith('.zip'):
            converter.save_samples_to_zip(samples, output_path)
        else:
            converter.save_samples_to_directory(samples, output_path)
        
        print(f"\nConversion completed successfully!")
        print(f"Converted {len(samples)} Python samples to JavaScript")
        print(f"Target library: {args.library}")
        print(f"Output location: {output_path}")
        
        return 0
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(asyncio.run(main()))
