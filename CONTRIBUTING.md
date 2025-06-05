# 🤝 Contributing to VLM Studio Lite

We welcome contributions from the community! This guide will help you get started with contributing to VLM Studio Lite, whether you're fixing bugs, adding features, or improving documentation.

## 📋 Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Setup](#development-setup)
4. [Contributing Guidelines](#contributing-guidelines)
5. [Submitting Changes](#submitting-changes)
6. [Code Style](#code-style)
7. [Testing](#testing)
8. [Documentation](#documentation)

---

## 📜 Code of Conduct

This project adheres to a code of conduct that we expect all contributors to follow:

### Our Pledge
- **Be respectful** and inclusive to all participants
- **Be collaborative** and constructive in discussions
- **Be patient** with newcomers and different experience levels
- **Be professional** in all interactions

### Unacceptable Behavior
- Harassment, discrimination, or offensive comments
- Personal attacks or trolling
- Spam or excessive self-promotion
- Violation of privacy or confidentiality

## 🚀 Getting Started

### What Can You Contribute?

#### **🐛 Bug Fixes**
- Fix provider connection issues
- Resolve UI/UX problems
- Correct documentation errors
- Address performance bottlenecks

#### **✨ New Features**
- Add new LLM providers
- Enhance agent monitoring capabilities
- Implement new UI components
- Create additional agent types

#### **📚 Documentation**
- Improve setup instructions
- Add usage examples
- Create tutorials and guides
- Translate documentation

#### **🧪 Testing**
- Write unit tests
- Create integration tests
- Test edge cases
- Verify cross-platform compatibility

### **Finding Issues to Work On**

1. **Browse Issues**: Check [GitHub Issues](https://github.com/sorrowscry86/Codeystack/issues)
2. **Good First Issues**: Look for `good-first-issue` label
3. **Help Wanted**: Check `help-wanted` labeled issues
4. **Discussions**: Join [GitHub Discussions](https://github.com/sorrowscry86/Codeystack/discussions)

---

## 🛠️ Development Setup

### **1. Fork and Clone**

```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/Codeystack.git
cd Codeystack

# Add upstream remote
git remote add upstream https://github.com/sorrowscry86/Codeystack.git
```

### **2. Set Up Development Environment**

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest black flake8 mypy pre-commit
```

### **3. Configure Environment**

```bash
# Copy example environment file
cp .env.example .env

# Edit with your API keys (for testing)
# Don't commit real API keys!
```

### **4. Verify Setup**

```bash
# Run tests
pytest

# Check code style
black --check .
flake8 .

# Type checking
mypy .

# Start application
python app.py  # Backend
streamlit run studio_lite.py  # Frontend
```

---

## 📝 Contributing Guidelines

### **Branch Naming Convention**

```bash
# Feature branches
feature/add-new-provider
feature/enhance-agent-dashboard

# Bug fix branches  
bugfix/fix-ollama-connection
bugfix/resolve-ui-crash

# Documentation branches
docs/update-api-documentation
docs/add-deployment-guide

# Hotfix branches (urgent production fixes)
hotfix/critical-security-fix
```

### **Commit Message Format**

Use conventional commits for clear history:

```bash
# Format: type(scope): description

# Examples:
feat(providers): add Azure OpenAI provider support
fix(ui): resolve agent status display issue
docs(readme): update installation instructions
test(integration): add provider connection tests
refactor(backend): optimize chat endpoint performance
style(frontend): improve agent dashboard layout
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (no logic changes)
- `refactor`: Code refactoring
- `test`: Adding or modifying tests
- `chore`: Maintenance tasks

### **Pull Request Guidelines**

#### **Before Creating a PR:**
1. **Sync with upstream**: `git pull upstream main`
2. **Run tests**: `pytest`
3. **Check code style**: `black . && flake8 .`
4. **Update documentation** if needed
5. **Test your changes** thoroughly

#### **PR Title Format:**
```
[Type] Brief description of changes

Examples:
[Feature] Add support for Claude 3.5 Sonnet via Anthropic API
[Bug Fix] Resolve agent status persistence issue
[Documentation] Add comprehensive API documentation
```

#### **PR Description Template:**
```markdown
## Description
Brief description of what this PR does.

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing
- [ ] Tested locally
- [ ] Added/updated tests
- [ ] All tests pass

## Screenshots (if applicable)
Add screenshots of UI changes

## Checklist
- [ ] My code follows the style guidelines
- [ ] I have performed a self-review
- [ ] I have commented my code where necessary
- [ ] I have made corresponding changes to documentation
- [ ] My changes generate no new warnings
- [ ] New and existing tests pass
```

---

## 🎨 Code Style

### **Python Style Guide**

We follow [PEP 8](https://pep8.org/) with some modifications:

```python
# Use Black for formatting
black --line-length 88 .

# Configuration in pyproject.toml
[tool.black]
line-length = 88
target-version = ['py311']
include = '\.pyi?$'
```

### **Code Organization**

```python
# File structure example
"""
Module docstring describing purpose and usage.
"""

# Standard library imports
import os
import json
from typing import Dict, List, Optional

# Third-party imports  
import streamlit as st
import requests
from flask import Flask

# Local imports
from .providers.base import BaseLLMProvider
from .config import settings

# Constants
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3

class ExampleClass:
    """
    Class docstring with description.
    
    Args:
        param1: Description of parameter
        param2: Description of parameter
    """
    
    def __init__(self, param1: str, param2: int = 10):
        self.param1 = param1
        self.param2 = param2
    
    def public_method(self) -> str:
        """Public method with clear docstring."""
        return self._private_method()
    
    def _private_method(self) -> str:
        """Private method (underscore prefix)."""
        return f"{self.param1}_{self.param2}"

def utility_function(data: Dict[str, any]) -> Optional[str]:
    """
    Utility function with type hints.
    
    Args:
        data: Input data dictionary
        
    Returns:
        Processed string or None if invalid
        
    Raises:
        ValueError: If data is malformed
    """
    if not data:
        return None
    
    try:
        return str(data.get('value', ''))
    except Exception as e:
        raise ValueError(f"Invalid data format: {e}")
```

### **Frontend Style (Streamlit)**

```python
# Streamlit best practices

# Use descriptive variable names
llm_provider = st.selectbox("Choose Provider", options)

# Group related UI elements
with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("API Key", type="password")

# Use containers for layout
col1, col2 = st.columns(2)
with col1:
    st.metric("Active Agents", active_count)
with col2:
    st.metric("Completed Tasks", task_count)

# Session state management
if 'agent_data' not in st.session_state:
    st.session_state.agent_data = initialize_agents()
```

---

## 🧪 Testing

### **Testing Framework**

We use `pytest` for testing:

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_providers.py

# Run with coverage
pytest --cov=. --cov-report=html

# Run integration tests
pytest tests/integration/
```

### **Test Structure**

```python
# tests/test_example.py
import pytest
from unittest.mock import Mock, patch

from app import create_app
from llm_providers.openai_provider import OpenAIProvider

class TestOpenAIProvider:
    """Test cases for OpenAI provider."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.provider = OpenAIProvider(api_key="test-key")
    
    def test_initialization(self):
        """Test provider initialization."""
        assert self.provider.api_key == "test-key"
        assert self.provider.name == "openai"
    
    @patch('requests.post')
    def test_chat_completion(self, mock_post):
        """Test chat completion functionality."""
        # Mock successful response
        mock_response = Mock()
        mock_response.json.return_value = {
            'choices': [{'message': {'content': 'Test response'}}]
        }
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        
        # Test the method
        result = self.provider.chat(
            messages=[{"role": "user", "content": "Hello"}],
            model="gpt-4"
        )
        
        # Assertions
        assert result['content'] == 'Test response'
        mock_post.assert_called_once()
    
    def test_invalid_api_key(self):
        """Test behavior with invalid API key."""
        with pytest.raises(ValueError):
            OpenAIProvider(api_key="")

# Integration tests
class TestIntegration:
    """Integration test cases."""
    
    def setup_method(self):
        """Set up test app."""
        self.app = create_app(testing=True)
        self.client = self.app.test_client()
    
    def test_health_endpoint(self):
        """Test health check endpoint."""
        response = self.client.get('/')
        assert response.status_code == 200
        data = response.get_json()
        assert 'available_providers' in data
```

### **Testing Guidelines**

1. **Write tests for new features**
2. **Maintain test coverage above 80%**
3. **Use descriptive test names**
4. **Mock external dependencies**
5. **Test edge cases and error conditions**

---

## 📖 Documentation

### **Documentation Standards**

#### **Code Documentation**
```python
def process_chat_request(provider: str, model: str, messages: List[Dict]) -> Dict:
    """
    Process a chat completion request through the specified provider.
    
    This function validates the request parameters, initializes the appropriate
    LLM provider, and handles the chat completion with proper error handling.
    
    Args:
        provider: Name of the LLM provider ('openai', 'ollama', etc.)
        model: Specific model identifier for the provider
        messages: List of message dictionaries with 'role' and 'content' keys
        
    Returns:
        Dictionary containing the chat response with keys:
        - 'content': The generated response text
        - 'usage': Token usage information (if available)
        - 'model': Model used for generation
        
    Raises:
        ValueError: If provider is not supported or parameters are invalid
        ConnectionError: If provider service is unavailable
        
    Example:
        >>> messages = [{"role": "user", "content": "Hello!"}]
        >>> result = process_chat_request("openai", "gpt-4", messages)
        >>> print(result['content'])
        'Hello! How can I help you today?'
    """
```

#### **README Updates**
When adding features, update:
- Feature list in main README
- Installation instructions (if needed)
- Usage examples
- Configuration options

#### **API Documentation**
Update `API_DOCUMENTATION.md` for:
- New endpoints
- Changed request/response formats
- New parameters
- Error codes

### **Documentation Tools**

```bash
# Generate API docs
pdoc --html . -o docs/

# Lint documentation
markdownlint *.md

# Spell check
cspell "**/*.md"
```

---

## 🔄 Review Process

### **Code Review Checklist**

**For Authors:**
- [ ] Code follows style guidelines
- [ ] Tests are included and passing
- [ ] Documentation is updated
- [ ] No sensitive data in commits
- [ ] Commit messages are clear

**For Reviewers:**
- [ ] Code is readable and maintainable
- [ ] Logic is correct and efficient
- [ ] Error handling is appropriate
- [ ] Tests cover edge cases
- [ ] Documentation is accurate

### **Review Guidelines**

1. **Be constructive** in feedback
2. **Explain the "why"** behind suggestions
3. **Consider multiple solutions**
4. **Test the changes** locally if possible
5. **Approve** when ready, or **request changes** with specific feedback

---

## 🏆 Recognition

### **Contributors Wall**

We maintain a contributors list in our README and celebrate contributions:

- **🥇 Major Contributors**: Significant features or improvements
- **🐛 Bug Hunters**: Critical bug fixes
- **📚 Documentation Heroes**: Comprehensive documentation improvements
- **🧪 Test Champions**: Extensive testing contributions

### **How to Get Credit**

1. **GitHub Profile**: Contributions appear on your profile
2. **Release Notes**: Major contributions mentioned in releases
3. **Contributors Section**: Added to project README
4. **Community Recognition**: Highlighted in discussions

---

## 📞 Getting Help

### **Where to Ask Questions**

1. **GitHub Discussions**: General questions and ideas
2. **GitHub Issues**: Bug reports and feature requests
3. **Discord**: Real-time chat (if available)
4. **Email**: Direct contact for sensitive issues

### **Response Times**

- **Issues**: Within 48 hours
- **Pull Requests**: Within 72 hours
- **Discussions**: Within 24 hours

### **Mentorship**

New contributors can request mentorship for:
- Understanding the codebase
- Setting up development environment
- Guidance on first contributions
- Code review and feedback

---

## 🎉 Thank You!

Every contribution, no matter how small, makes VLM Studio Lite better for everyone. We appreciate:

- **Code contributions** that add value
- **Bug reports** that help us improve
- **Documentation** that helps others
- **Community participation** that builds connections
- **Feedback** that guides our direction

**Ready to contribute?** Check out our [good first issues](https://github.com/sorrowscry86/Codeystack/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22) and get started!

---

*This contributing guide is based on best practices and will evolve with our community. Suggestions for improvements are always welcome!*
