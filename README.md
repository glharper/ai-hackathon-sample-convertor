# Python to JavaScript Sample Converter

A tool that automatically converts Python code samples to JavaScript, designed for porting repository samples to use JavaScript libraries like Azure SDKs.

Available in two versions:
- **Web Application**: Node.js/Express web interface (`server.js`)
- **Python CLI**: Command-line tool (`converter.py`)

## Features

- **Repository Integration**: Fetch Python samples directly from GitHub repository URLs
- **API Documentation Parsing**: Automatically discover JavaScript library methods from documentation
- **Intelligent Conversion**: Convert Python syntax to JavaScript with library-specific transformations
- **Batch Processing**: Convert multiple files at once
- **Download Support**: Get all converted samples as a ZIP file

## How It Works

1. **Input a GitHub Repository URL** containing Python samples
2. **Specify a JavaScript Library** (default: @azure/ai-agents)
3. **Optionally provide API Documentation URL** for better conversion accuracy
4. **Get converted JavaScript samples** with proper imports and syntax

## Usage

### Starting the Web Application

```bash
npm install
npm start
```

The application will be available at `http://localhost:3000`

### Example Inputs

- **Repository URL**: `https://github.com/Azure-Samples/azure-ai-samples/tree/main/scenarios/agents/python`
- **JS Library**: `@azure/ai-agents`
- **API Docs**: `https://docs.microsoft.com/en-us/javascript/api/@azure/ai-agents/`

## Conversion Features

### Python to JavaScript Mappings

- `print()` → `console.log()`
- `True/False/None` → `true/false/null`
- `and/or/not` → `&&/||/!`
- `len()` → `.length`
- String formatting (`f"..."`) → Template literals (`` `...` ``)
- List methods (`.append()`) → Array methods (`.push()`)
- Exception handling (`try/except`) → `try/catch`

### Library-Specific Conversions

- Automatic import generation for specified JavaScript libraries
- API method mapping based on documentation parsing
- Async/await pattern application for API calls
- Library-specific client instantiation

### Advanced Features

- Recursive directory traversal for nested samples
- Error handling with fallback comments
- Code structure preservation
- Proper indentation and formatting

## Architecture

- **Frontend**: HTML/CSS/JavaScript with modern UI
- **Backend**: Express.js server
- **Services**:
  - `repositoryFetcher.js`: GitHub API integration
  - `apiDocParser.js`: Documentation parsing
  - `pythonToJsConverter.js`: Core conversion logic

## Supported Libraries

The converter works with any JavaScript library but has optimized support for:

- Azure SDK libraries (`@azure/*`)
- OpenAI libraries
- Generic Node.js packages

## Limitations

- Complex Python features may require manual adjustment
- Conversion accuracy depends on code complexity
- Some Python-specific patterns don't have direct JavaScript equivalents

## Development

### Project Structure

```
├── server.js              # Express server
├── public/                # Frontend assets
│   ├── index.html         # Main UI
│   ├── styles.css         # Styling
│   └── script.js          # Frontend logic
└── services/              # Backend services
    ├── repositoryFetcher.js
    ├── apiDocParser.js
    └── pythonToJsConverter.js
```

### Adding New Conversion Rules

Edit `services/pythonToJsConverter.js` to add new Python-to-JavaScript conversion patterns.

### Supporting New Libraries

Update the `getCommonMappings()` method in `apiDocParser.js` to add library-specific mappings.

## License

ISC

## Python CLI Usage

### Installation

```bash
pip install -r requirements.txt
```

### Command Line Interface

```bash
# Basic usage
python converter.py https://github.com/user/repo/tree/main/samples

# Specify JavaScript library
python converter.py https://github.com/user/repo/tree/main/samples --library @azure/ai-agents

# Include API documentation
python converter.py https://github.com/user/repo/tree/main/samples --library @azure/openai --docs https://docs.microsoft.com/api

# Save to specific location
python converter.py https://github.com/user/repo/tree/main/samples --output converted_samples.zip

# Save to directory instead of ZIP
python converter.py https://github.com/user/repo/tree/main/samples --output ./js_samples/

# Verbose output
python converter.py https://github.com/user/repo/tree/main/samples --verbose
```

### Programmatic Usage

```python
from converter import PythonToJsConverter, convert_text

# Convert single code snippet
js_code = convert_text(
    text="print('Hello World')",
    lib_name="@azure/ai-agents", 
    ref_url="https://docs.microsoft.com/api"
)

# Convert repository samples
async def convert_repo():
    converter = PythonToJsConverter()
    samples = await converter.convert_samples(
        repo_url="https://github.com/user/repo/tree/main/samples",
        js_library="@azure/ai-agents",
        api_docs_url="https://docs.microsoft.com/api"
    )
    converter.save_samples_to_zip(samples, "output.zip")
```

## Documentation

- **[Developer Guide](DEVELOPER_GUIDE.md)**: Comprehensive guide for extending and contributing to the project
- **[API Reference](README.md#conversion-features)**: Details on conversion patterns and supported libraries  
- **[Examples](test_converter.py)**: Code examples and usage demonstrations

## Quick Start

### Web Application
1. `npm install && npm start`
2. Open `http://localhost:3000`
3. Enter repository URL and library details
4. Download converted samples

### Python CLI
1. `pip install -r requirements.txt`
2. `python converter.py https://github.com/user/repo/tree/main/samples`
3. Find converted files in `js-samples.zip`

## Implementation Notes

### Core Conversion Function

The actual conversion logic is centralized in the `convert_text()` function in `converter.py`:

```python
def convert_text(text: str, lib_name: str, ref_url: str) -> str:
    """
    Convert Python code text to JavaScript.
    
    Args:
        text: Python source code to convert
        lib_name: JavaScript library name to use  
        ref_url: URL to API reference documentation
        
    Returns:
        Converted JavaScript code
    """
    # TODO: Implement actual conversion logic here
```

This function should be implemented with the sophisticated conversion logic, including:
- Syntax transformation (Python → JavaScript)
- Library-specific API mappings
- Import statement generation
- Async/await pattern application
- Error handling and fallbacks

### Architecture Comparison

**Python CLI Version:**
- `converter.py`: Main CLI application
- `RepositoryFetcher`: GitHub API integration
- `ApiDocParser`: Documentation parsing
- `PythonToJsConverter`: Orchestration
- `convert_text()`: Core conversion logic

**Web Application Version:**
- `server.js`: Express.js server
- `services/repositoryFetcher.js`: GitHub integration
- `services/apiDocParser.js`: Documentation parsing  
- `services/pythonToJsConverter.js`: Conversion logic
- `public/`: Frontend interface
