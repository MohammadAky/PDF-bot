# Contributing to PDF Bot

First off, thank you for considering contributing to PDF Bot! It's people like you that make PDF Bot such a great tool.

## 🎯 Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## 🚀 How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the issue list as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps which reproduce the problem**
- **Provide specific examples to demonstrate the steps**
- **Describe the behavior you observed after following the steps**
- **Explain which behavior you expected to see instead and why**
- **Include screenshots if possible**
- **Include your Python version and OS**

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

- **Use a clear and descriptive title**
- **Provide a step-by-step description of the suggested enhancement**
- **Provide specific examples to demonstrate the steps**
- **Describe the current behavior and explain the behavior you expected to see instead**
- **Explain why this enhancement would be useful**

### Pull Requests

- Fill in the required template
- Follow the Python style guide (PEP 8)
- Include appropriate test cases
- Update documentation as needed
- End all files with a newline

## 🔧 Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/PDF-bot.git
cd PDF-bot

# Add upstream remote
git remote add upstream https://github.com/MohammadAky/PDF-bot.git
```

### 2. Create Development Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-asyncio black flake8 mypy
```

### 3. Set Up Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your test bot token
nano .env
```

### 4. Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=.

# Run specific test file
pytest tests/test_pdf_organizer.py
```

## 📝 Style Guide

### Python Style

We follow PEP 8 with these specifics:

- Use 4 spaces for indentation
- Maximum line length is 100 characters
- Use double quotes for strings
- Use type hints where appropriate

```python
# Good
def merge_pdfs(pdf_paths: List[str], output_path: str = None) -> str:
    """Merge multiple PDF files into one"""
    pass

# Bad
def merge_pdfs(pdf_paths, output_path=None):
    pass
```

### Documentation

- Use docstrings for all public modules, functions, classes, and methods
- Follow Google style for docstrings

```python
def extract_pages(pdf_path: str, page_spec: str, output_path: str = None) -> str:
    """
    Extract specific pages from a PDF

    Args:
        pdf_path: Path to input PDF
        page_spec: Page specification (e.g., "1,3,5" or "1-5,8,10-15")
        output_path: Output file path (optional)

    Returns:
        Path to output PDF

    Raises:
        ValueError: If page specification is invalid
        FileNotFoundError: If input PDF doesn't exist
    """
    pass
```

### Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line

```
Add PDF compression feature

- Implement compression service
- Add compression level options
- Update documentation
- Add tests

Closes #123
```

## 🏗️ Project Structure

When adding new features, follow the existing structure:

```
services/          # Business logic and PDF operations
├── pdf_converter.py
├── pdf_organizer.py
├── pdf_optimizer.py
└── ...

bot/               # Telegram bot interface
├── handlers.py    # Message and command handlers
├── callbacks.py   # Button callbacks
└── keyboards.py   # Keyboard layouts

utils/             # Utility functions
├── file_manager.py
├── validators.py
└── ...

config/            # Configuration
├── settings.py
└── texts.py       # Multilingual texts
```

## 🧪 Testing

### Writing Tests

```python
import pytest
from services.pdf_organizer import merge_pdfs

@pytest.mark.asyncio
async def test_merge_pdfs():
    """Test merging multiple PDFs"""
    # Arrange
    pdf_paths = ["test1.pdf", "test2.pdf"]

    # Act
    result = await merge_pdfs(pdf_paths)

    # Assert
    assert os.path.exists(result)
    assert result.endswith(".pdf")
```

### Running Specific Tests

```bash
# Test specific module
pytest tests/test_pdf_organizer.py

# Test specific function
pytest tests/test_pdf_organizer.py::test_merge_pdfs

# Test with verbose output
pytest -v

# Test with print statements
pytest -s
```

## 📦 Adding New Features

### 1. Plan Your Feature

- Check if there's an existing issue
- If not, create an issue to discuss the feature
- Get feedback before starting implementation

### 2. Implement the Feature

```python
# services/pdf_my_feature.py
async def my_new_feature(pdf_path: str) -> str:
    """
    Description of what your feature does

    Args:
        pdf_path: Path to input PDF

    Returns:
        Path to output PDF
    """
    try:
        # Your implementation
        return output_path
    except Exception as e:
        logger.error(f"Error in my_new_feature: {e}")
        raise
```

### 3. Add Translations

```python
# config/texts.py
TEXTS = {
    "en": {
        "my_feature": "🎯 My New Feature",
        "my_feature_instruction": "📤 Send a PDF to process",
        # ...
    },
    "fa": {
        "my_feature": "🎯 ویژگی جدید من",
        "my_feature_instruction": "📤 یک PDF برای پردازش ارسال کنید",
        # ...
    }
}
```

### 4. Add Handler

```python
# bot/callbacks.py
if data == "my_feature":
    user_states[user_id] = "my_feature_processing"
    await query.edit_message_text(
        get_text(user_id, "my_feature_instruction"),
        reply_markup=get_back_keyboard(user_id)
    )
    return
```

### 5. Add Tests

```python
# tests/test_my_feature.py
import pytest
from services.pdf_my_feature import my_new_feature

@pytest.mark.asyncio
async def test_my_new_feature():
    # Test implementation
    pass
```

### 6. Update Documentation

- Add feature to README.md
- Update CHANGELOG.md
- Add usage examples

## 🔍 Code Review Process

1. **Automated Checks**: Your PR will be automatically checked for:

   - Code style (flake8)
   - Type hints (mypy)
   - Tests passing (pytest)

2. **Manual Review**: A maintainer will review:

   - Code quality and style
   - Test coverage
   - Documentation
   - Functionality

3. **Feedback**: Address any feedback from reviewers

4. **Merge**: Once approved, your PR will be merged!

## 🌍 Translations

We welcome translations to new languages!

### Adding a New Language

1. Add language code to `config/settings.py`:

```python
SUPPORTED_LANGUAGES = ["en", "fa", "de"]  # Add your language
```

2. Add all translations to `config/texts.py`:

```python
TEXTS = {
    "en": { ... },
    "fa": { ... },
    "de": {  # Your new language
        "welcome": "Willkommen...",
        # ... all other keys
    }
}
```

3. Add language button to keyboards:

```python
# bot/keyboards.py
def get_language_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"),
            InlineKeyboardButton("🇮🇷 فارسی", callback_data="lang_fa"),
            InlineKeyboardButton("🇩🇪 Deutsch", callback_data="lang_de"),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)
```

## 📋 Checklist

Before submitting your PR, make sure:

- [ ] Code follows the style guide
- [ ] All tests pass
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] Translations added (if applicable)
- [ ] Commit messages are clear
- [ ] Branch is up to date with main
- [ ] No merge conflicts

## 🎓 Resources

- [Python-telegram-bot Documentation](https://docs.python-telegram-bot.org/)
- [PyPDF2 Documentation](https://pypdf2.readthedocs.io/)
- [Python Style Guide (PEP 8)](https://pep8.org/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)

## 💬 Questions?

- Open an issue with the "question" label
- Contact maintainers on Telegram: @YourSupportUsername
- Check existing issues and discussions

## 🙏 Thank You!

Your contributions to open source, large or small, make projects like this possible. Thank you for taking the time to contribute.

---

**Happy coding! 🚀**
