# Contributing to EchoOS

Thank you for your interest in contributing to EchoOS! This document provides guidelines and instructions for contributing.

## 🤝 How to Contribute

### Reporting Bugs

If you find a bug:

1. **Check existing issues** to avoid duplicates
2. **Create a new issue** with:
   - Clear, descriptive title
   - Steps to reproduce
   - Expected vs actual behavior
   - System information (OS, Python version)
   - Error logs from `echoos.log`
   - Screenshots if applicable

### Suggesting Features

For feature requests:

1. **Check existing issues** for similar requests
2. **Create a new issue** with:
   - Clear description of the feature
   - Use cases and benefits
   - Possible implementation approach
   - Any relevant examples

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
4. **Test thoroughly**
5. **Commit with clear messages**
   ```bash
   git commit -m "Add: Brief description of changes"
   ```
6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Create Pull Request** with:
   - Clear description of changes
   - Reference to related issues
   - Screenshots/demos if applicable

## 📝 Development Guidelines

### Code Style

- Follow **PEP 8** style guide
- Use **type hints** where appropriate
- Write **docstrings** for functions and classes
- Keep functions **focused and small**
- Use **meaningful variable names**

### Code Formatting

```bash
# Format code with black
black modules/ main.py

# Check with flake8
flake8 modules/ main.py
```

### Testing

```bash
# Run tests
pytest tests/

# Run with coverage
pytest --cov=modules tests/
```

### Documentation

- Update README.md for major changes
- Add docstrings to new functions
- Update INSTALLATION.md for setup changes
- Comment complex logic

## 🏗️ Project Structure

```
EchoOS-CrossPlatform/
├── main.py              # Entry point
├── modules/             # Core modules
│   ├── auth.py         # Authentication
│   ├── stt.py          # Speech-to-text
│   ├── tts.py          # Text-to-speech
│   ├── parser.py       # Command parsing
│   ├── executor.py     # Command execution
│   ├── app_discovery.py # App discovery
│   ├── accessibility.py # Accessibility
│   └── ui.py           # User interface
├── config/             # Configuration files
├── models/             # Voice models
├── scripts/            # Utility scripts
└── tests/              # Test files
```

## 🎯 Areas for Contribution

### High Priority

- [ ] Natural Language Understanding (NLU)
- [ ] Multi-language support
- [ ] Continuous authentication
- [ ] Mobile deployment
- [ ] Plugin system

### Medium Priority

- [ ] Voice command macros
- [ ] Cloud sync (optional)
- [ ] Advanced accessibility features
- [ ] Better error handling
- [ ] Performance optimizations

### Good First Issues

- [ ] Add more voice commands
- [ ] Improve documentation
- [ ] Add unit tests
- [ ] Fix UI bugs
- [ ] Add command aliases

## 🧪 Testing Your Changes

### Manual Testing

1. Test on both Windows and macOS if possible
2. Test with different microphones
3. Test in noisy environments
4. Test all affected commands
5. Check error handling

### Automated Testing

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_auth.py

# Run with verbose output
pytest -v tests/
```

## 📋 Commit Message Guidelines

Use clear, descriptive commit messages:

```
Add: New feature or functionality
Fix: Bug fix
Update: Changes to existing feature
Refactor: Code restructuring
Docs: Documentation changes
Test: Adding or updating tests
Style: Code style changes
```

Examples:
```
Add: Multi-language support for Spanish
Fix: Microphone detection on macOS
Update: Improve voice authentication accuracy
Docs: Add troubleshooting section to README
```

## 🔍 Code Review Process

1. **Automated checks** run on PR
2. **Maintainer review** within 48 hours
3. **Feedback and discussion**
4. **Approval and merge**

## 🌟 Recognition

Contributors will be:
- Listed in README.md
- Mentioned in release notes
- Credited in documentation

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 💬 Communication

- **GitHub Issues**: Bug reports and features
- **Pull Requests**: Code contributions
- **Email**: 1by22is076@bmsit.in

## ❓ Questions?

Feel free to:
- Open an issue for questions
- Email the maintainer
- Check existing documentation

---

**Thank you for contributing to EchoOS! 🎉**
