# Contributing to FPL Captain Picker

Thank you for your interest in contributing to FPL Captain Picker! This document provides guidelines and instructions for contributing to this project.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for everyone.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the issue list as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

- Use a clear and descriptive title
- Describe the exact steps to reproduce the problem
- Provide specific examples to demonstrate the steps
- Describe the behavior you observed after following the steps
- Explain which behavior you expected to see instead and why
- Include screenshots if applicable
- Include the gameweek number and any relevant player data

### Suggesting Enhancements

If you have a suggestion for a new feature or enhancement, please:

- Use a clear and descriptive title
- Provide a detailed description of the suggested functionality
- Explain why this enhancement would be useful
- List any similar features in other FPL tools, if applicable

### Pull Requests

1. Fork the repo and create your branch from `main`
2. If you've added code that should be tested, add tests
3. If you've changed APIs, update the documentation
4. Ensure the test suite passes
5. Make sure your code lints
6. Issue that pull request!

## Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/fpl-captain-picker.git
   ```
3. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

### Local Development

1. Set up your development environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   ```bash
   export OLLAMA_MODEL=mistral  # or your preferred model
   ```

3. Run the development server:
   ```bash
   python app.py
   ```

### Testing

Before submitting a pull request, please ensure:

1. All tests pass:
   ```bash
   python -m pytest
   ```

2. Code follows style guidelines:
   ```bash
   flake8
   ```

## Style Guide

- Follow PEP 8 style guide for Python code
- Use meaningful variable and function names
- Add comments for complex logic
- Keep functions small and focused
- Write docstrings for all functions and classes

## Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line

## Documentation

- Update the README.md if needed
- Add comments to code
- Update API documentation if you change endpoints
- Document any new environment variables

## Review Process

1. All pull requests require at least one review
2. CI checks must pass
3. Code must be properly documented
4. Tests must be included for new features

## Questions?

If you have any questions about contributing, please open an issue and we'll be happy to help! 