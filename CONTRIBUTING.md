# Contributing to ML Frameworks

Thank you for your interest in contributing! Here's how to get started.

## Development Setup

```bash
# Clone and setup
git clone https://github.com/yourusername/ml-frameworks.git
cd ml-frameworks

# Create virtual environment with uv (or python -m venv)
uv venv
source .venv/bin/activate

# Install Poetry
pip install poetry

# Install stack for development (with all groups)
cd stacks/pytorch-cu121
poetry install --extras all
cd ../..

# Install dev tools
pip install black ruff mypy pre-commit
```

## Making Changes

### Code Style

We use automated formatting:

```bash
# Format code
black .

# Check style
ruff check . --fix

# Type checking
mypy tests/
```

### Testing

Run tests locally (sequential is fine):

```bash
# From root directory, ensure Poetry venv is active
cd stacks/pytorch-cu121
poetry run pytest ../../tests -v

# Test specific group
poetry run pytest ../../tests -k "pytorch-cu121-ml" -v

# Test with coverage
poetry run pytest ../../tests --cov=tests
```

### Before You Submit

1. **Run linting**:
   ```bash
   black .
   ruff check . --fix
   ```

2. **Run tests**:
   ```bash
   pytest -v
   ```

3. **Commit with clear message**:
   ```bash
   git commit -m "Add/fix [feature]: description"
   ```

4. **Push and create PR**:
   ```bash
   git push origin your-branch
   ```

## Adding New Stacks

To add a new stack (e.g., `pytorch-cu118`):

1. **Create directory**:
   ```bash
   mkdir -p stacks/pytorch-cu118
   ```

2. **Copy template**:
   ```bash
   cp stacks/pytorch-cu121/pyproject.toml stacks/pytorch-cu118/
   ```

3. **Modify** `pyproject.toml`:
   - Update `name` and `description`
   - Change PyTorch index URL if needed
   - Adjust dependencies as desired

4. **Add README**:
   ```bash
   cp stacks/pytorch-cu121/README.md stacks/pytorch-cu118/
   # Edit with stack-specific info
   ```

5. **Tests auto-discover** - no changes needed!

## Adding New Dependencies

### To an existing group:

Edit `stacks/pytorch-cu121/pyproject.toml`:

```toml
[tool.poetry.dependencies]
your-new-package = {version = "^1.0.0", optional = true}

[tool.poetry.extras]
ml = [
    "existing-package",
    "your-new-package",  # Add here
]
```

### Update test mappings:

If the package has a non-standard import, add to `tests/conftest.py`:

```python
package_to_import = {
    # ... existing mappings ...
    "your-new-package": "import your_new_package; assert your_new_package.__version__",
}
```

### Test locally:

```bash
cd stacks/pytorch-cu121
poetry install --extras ml
poetry run pytest ../../tests -k "pytorch-cu121-ml" -v
```

## PR Review Process

1. **Automated checks** run (18 jobs × test matrix)
2. **Code review** by maintainers
3. **Manual testing** (for risky changes)
4. **Merge** once approved and all checks pass

## Troubleshooting

### Import test fails for new package

Common issues:

1. **Non-standard import name**
   ```python
   # Add mapping in conftest.py
   "opencv-python": "import cv2; assert cv2.__version__",
   ```

2. **No `__version__` attribute**
   ```python
   # Just try importing
   "package-name": "import package_name",
   ```

3. **Submodule only**
   ```python
   "package-name": "from package_name.module import something",
   ```

### Dependency conflict

If adding a package causes conflicts:

1. Check version constraints in pyproject.toml
2. Try relaxing version pins
3. Run with verbose output: `pip install -vvv`
4. File an issue if it's a real incompatibility

## Questions?

- Check existing [GitHub Issues](https://github.com/yourusername/ml-frameworks/issues)
- Start a [Discussion](https://github.com/yourusername/ml-frameworks/discussions)
- Email maintainers

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
