# Using VS Code with GitHub Copilot

This guide explains how to use Visual Studio Code with GitHub Copilot to interact with the ART Code Generation System.

## Prerequisites

1. Install Visual Studio Code
2. Install the following VS Code extensions:
   - Python
   - Pylance
   - GitHub Copilot
   - GitHub Copilot Chat

## Setup

1. Clone the repository and open it in VS Code:
```bash
git clone https://github.com/yourusername/art-code-gen.git
code art-code-gen
```

2. Install the Python virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

3. Select the Python interpreter:
   - Press `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (Mac)
   - Type "Python: Select Interpreter"
   - Choose the interpreter from `.venv`

## Using GitHub Copilot

### Basic Usage

1. **Code Completion**
   - Start typing code and Copilot will suggest completions
   - Press `Tab` to accept a suggestion
   - Press `Alt+]` to see the next suggestion
   - Press `Alt+[` to see the previous suggestion

2. **Inline Comments**
   - Write a comment describing what you want to do
   - Copilot will suggest code based on your comment
   - Example:
   ```python
   # Function to analyze form structure and extract validation rules
   ```

3. **Documentation Generation**
   - Write a function or class
   - Add a docstring template
   - Copilot will suggest complete documentation

### Advanced Features

1. **Code Generation from Natural Language**
   - Use the Copilot Chat panel (Ctrl+Shift+I)
   - Describe what you want to implement
   - Example: "Create a function to validate form fields"

2. **Test Generation**
   - Write a function
   - Add a comment: "# Generate tests for this function"
   - Copilot will suggest unit tests

3. **Code Refactoring**
   - Select code to refactor
   - Use Copilot Chat to request refactoring
   - Example: "Refactor this code to use async/await"

### Project-Specific Features

1. **Form Analysis**
   - Use Copilot to generate form analysis code
   - Example: "Create a function to extract form validation rules"

2. **Code Generation**
   - Use Copilot to generate API endpoints
   - Example: "Generate a FastAPI endpoint for form submission"

3. **Template Generation**
   - Use Copilot to create Jinja2 templates
   - Example: "Create a template for form validation"

## Best Practices

1. **Clear Comments**
   - Write clear, descriptive comments
   - Use specific language about requirements
   - Include examples when possible

2. **Code Review**
   - Always review Copilot's suggestions
   - Test generated code thoroughly
   - Follow project coding standards

3. **Security**
   - Don't share sensitive information in comments
   - Review generated code for security issues
   - Follow security best practices

## Troubleshooting

1. **Copilot Not Responding**
   - Check internet connection
   - Verify GitHub Copilot is enabled
   - Restart VS Code

2. **Poor Suggestions**
   - Make comments more specific
   - Provide more context
   - Use project-specific terminology

3. **Performance Issues**
   - Reduce file size
   - Split large functions
   - Use more specific prompts

## Keyboard Shortcuts

- `Tab`: Accept suggestion
- `Alt+]`: Next suggestion
- `Alt+[`: Previous suggestion
- `Ctrl+Enter`: Show all suggestions
- `Ctrl+Shift+I`: Open Copilot Chat
- `Esc`: Dismiss suggestion

## Additional Resources

- [GitHub Copilot Documentation](https://docs.github.com/en/copilot)
- [VS Code Python Extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
- [Project Documentation](../README.md) 