# Python to JavaScript Converter - Developer Guide

## Project Overview

This project provides both a **web application** and **command-line tool** for converting Python code samples to JavaScript, with special focus on Azure SDK library migrations.

## Project Structure

```
hackathon/
├── README.md                    # Main documentation
├── requirements.txt             # Python dependencies
├── package.json                 # Node.js dependencies
├── .github/
│   └── copilot-instructions.md  # Copilot workspace instructions
│
├── Web Application (Node.js)
├── server.js                    # Express.js web server
├── public/                      # Frontend assets
│   ├── index.html              # Main UI
│   ├── styles.css              # Styling
│   └── script.js               # Frontend JavaScript
└── services/                    # Backend services
    ├── repositoryFetcher.js     # GitHub API integration
    ├── apiDocParser.js          # Documentation parsing
    └── pythonToJsConverter.js   # Conversion logic
│
├── Python CLI Tool
├── converter.py                 # Main CLI application
├── test_converter.py           # Test examples
├── example_converter.py        # Advanced conversion example
└── quick_test.py               # Simple test file
```

## Core Components

### 1. Repository Fetching (`RepositoryFetcher`)

**Purpose**: Fetch Python files from GitHub repositories using the GitHub API.

**Key Features**:
- Converts GitHub URLs to API URLs
- Recursive directory traversal
- Handles authentication and rate limiting
- Supports various GitHub URL formats

**Usage**:
```python
async with RepositoryFetcher() as fetcher:
    samples = await fetcher.fetch_python_samples(repo_url)
```

### 2. API Documentation Parsing (`ApiDocParser`)

**Purpose**: Parse JavaScript library documentation to discover available methods.

**Key Features**:
- HTML parsing with pattern matching
- Method signature extraction
- Common library mappings
- Fallback to default mappings

**Usage**:
```python
async with ApiDocParser() as parser:
    methods = await parser.parse_api_methods(docs_url)
```

### 3. Code Conversion (`convert_text` function)

**Purpose**: Core conversion logic from Python to JavaScript.

**Current Implementation**: Basic placeholder with simple substitutions.

**Expected Enhancement**: Sophisticated syntax transformation (see `example_converter.py`).

### 4. Orchestration (`PythonToJsConverter`)

**Purpose**: Coordinate the entire conversion process.

**Key Features**:
- Async workflow management
- Error handling and recovery
- Output formatting (ZIP/directory)
- Progress reporting

## Conversion Architecture

### Input Processing
1. **Repository URL** → GitHub API calls → Python files
2. **API Documentation URL** → HTML parsing → Method mappings
3. **JavaScript Library Name** → Import generation + client setup

### Conversion Pipeline
1. **Fetch** Python samples from repository
2. **Parse** API documentation for method mappings
3. **Convert** each sample using `convert_text()`
4. **Package** results as ZIP or directory

### Output Generation
- Individual JavaScript files
- Proper import statements
- Library-specific client setup
- Error handling and comments

## Key Interfaces

### Main Conversion Function
```python
def convert_text(text: str, lib_name: str, ref_url: str) -> str:
    """
    Convert Python code to JavaScript.
    
    Args:
        text: Python source code
        lib_name: Target JavaScript library
        ref_url: API documentation URL
        
    Returns:
        Converted JavaScript code
    """
```

### CLI Interface
```bash
python converter.py REPO_URL [OPTIONS]

Options:
  --library LIBRARY     JavaScript library name
  --docs DOCS          API documentation URL  
  --output OUTPUT      Output file/directory
  --verbose            Enable verbose output
```

### Web API Interface
```javascript
POST /api/convert
{
    "repoUrl": "https://github.com/user/repo/tree/main/samples",
    "jsLibrary": "@azure/ai-agents", 
    "apiDocsUrl": "https://docs.microsoft.com/api"
}

Response:
{
    "success": true,
    "samplesCount": 5,
    "samples": [...]
}
```

## Extension Points

### 1. Enhanced Conversion Logic

Replace the placeholder `convert_text()` implementation with sophisticated logic:

```python
# Current: Simple text substitution
def convert_text(text: str, lib_name: str, ref_url: str) -> str:
    # Basic replacements
    return text.replace('print(', 'console.log(')

# Enhanced: Syntax tree transformation
def convert_text_advanced(text: str, lib_name: str, ref_url: str) -> str:
    converter = AdvancedPythonToJsConverter(lib_name, ref_url)
    return converter.convert(text)
```

See `example_converter.py` for a more sophisticated implementation.

### 2. Library Support

Add new JavaScript library mappings in `ApiDocParser.get_common_mappings()`:

```python
mappings = {
    '@azure/ai-agents': {...},
    '@azure/openai': {...},
    'your-library': {
        'python_method': 'js_method',
        # ... more mappings
    }
}
```

### 3. Documentation Parsers

Extend `ApiDocParser` to support different documentation formats:

```python
def parse_api_methods(self, docs_url: str) -> List[Dict[str, str]]:
    if 'swagger' in docs_url:
        return self._parse_swagger_docs(docs_url)
    elif 'typedoc' in docs_url:
        return self._parse_typedoc_docs(docs_url)
    # ... other formats
```

### 4. Output Formats

Add new output formats in `PythonToJsConverter`:

```python
def save_samples_to_npm_package(self, samples: List[Dict], package_name: str):
    # Create NPM package structure
    
def save_samples_to_workspace(self, samples: List[Dict], workspace_path: str):
    # Create VS Code workspace
```

## Testing and Development

### Running Tests
```bash
# Python CLI tests
python test_converter.py

# Web application
npm start  # http://localhost:3000

# Advanced conversion example
python example_converter.py
```

### Development Workflow

1. **Modify conversion logic** in `convert_text()` function
2. **Test with simple examples** using `quick_test.py`
3. **Add library mappings** in `ApiDocParser`
4. **Test with real repositories** using CLI or web interface
5. **Add error handling** and edge cases

### Debugging

**Enable verbose output**:
```bash
python converter.py REPO_URL --verbose
```

**Check intermediate results**:
```python
# Add debug prints in convert_text()
def convert_text(text: str, lib_name: str, ref_url: str) -> str:
    print(f"Converting: {text[:100]}...")
    result = # ... conversion logic
    print(f"Result: {result[:100]}...")
    return result
```

## Common Conversion Patterns

### Python → JavaScript Mappings

| Python | JavaScript | Notes |
|--------|------------|-------|
| `print()` | `console.log()` | Output |
| `True/False/None` | `true/false/null` | Literals |
| `len(x)` | `x.length` | Length |
| `and/or/not` | `&&/||/!` | Logic |
| `f"text {var}"` | `` `text ${var}` `` | Formatting |
| `list.append()` | `array.push()` | Arrays |
| `dict['key']` | `obj.key` or `obj['key']` | Objects |

### Control Structures

| Python | JavaScript |
|--------|------------|
| `if condition:` | `if (condition) {` |
| `for i in range(n):` | `for (let i = 0; i < n; i++) {` |
| `for item in items:` | `for (const item of items) {` |
| `try: ... except:` | `try { ... } catch (error) {` |

### Library-Specific Patterns

| Python (requests) | JavaScript (axios) |
|------------------|-------------------|
| `requests.get(url)` | `await axios.get(url)` |
| `response.status_code` | `response.status` |
| `response.text` | `response.data` |

## Future Enhancements

### Planned Features
- **AST-based conversion** for better accuracy
- **Type annotation support** for TypeScript output
- **Interactive conversion** with user feedback
- **Batch repository processing** for large migrations
- **Integration with VS Code** as an extension

### Integration Opportunities
- **GitHub Actions** for automated conversion workflows
- **Azure DevOps** pipeline integration
- **NPM package** for programmatic usage
- **VS Code extension** for inline conversion

## Contributing

### Code Style
- Follow PEP 8 for Python code
- Use TypeScript-style JSDoc for JavaScript
- Add type hints where possible
- Include comprehensive error handling

### Pull Request Guidelines
1. Add tests for new conversion patterns
2. Update documentation for new features
3. Ensure backward compatibility
4. Include examples in commit messages

For questions and contributions, see the main README.md file.
