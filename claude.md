# ML Frameworks Project - Current Status

## What Works ✅
- Poetry-formatted `pyproject.toml` with all 9 dependency groups defined
- CUDA 12.1 source configured via `[[tool.poetry.source]]` (priority = explicit)
- Minimal Python package created: `stacks/pytorch-cu121/ml_stack_pytorch/`
- All problematic packages removed (detectron2 not on PyPI)
- Test infrastructure in place (`tests/conftest.py`)
- GitHub Actions workflows updated

## Core Issue 🚧
**Poetry's Optional Dependency Problem:**
- Poetry tries to resolve ALL optional dependencies during lock, even unneeded ones
- Some packages (detectron2, optuna variants) fail to resolve from CUDA index
- Makes `poetry install --extras base` fail even though we don't need those packages

**Pip Index Problem:**
- pip doesn't natively read `[tool.poetry.source]` from pyproject.toml
- Must pass `--extra-index-url https://download.pytorch.org/whl/cu121` explicitly
- This defeats the goal of hiding the index URL in the package config

## Three Viable Paths Forward

### Option 1: Use Pip (Simplest)
```bash
# Users install like this:
pip install -e stacks/pytorch-cu121[ml,vision] --extra-index-url https://download.pytorch.org/whl/cu121
```
- ✅ Works reliably
- ✅ Fast
- ❌ Index URL not hidden in config
- **Action:** Document as standard practice, update README

### Option 2: Use Poetry (Purest)
- Try `poetry lock --no-interaction` ahead of time to pre-generate lock file
- Store `poetry.lock` in repo so `poetry install` just uses it without resolving
- ✅ Index fully in config
- ✅ Reproducible
- ❌ Requires committing lock file (large)
- **Action:** Generate `poetry.lock`, commit it, use `poetry install` (no extras needed)

### Option 3: Use UV (Modern Alternative)
- UV is much faster than pip/poetry
- Can handle Poetry config with fewer issues
- ✅ Very fast
- ✅ Modern
- ❌ Less mature than Poetry
- **Action:** Switch CI to UV, provide UV install instructions

## Recommendation
**Go with Option 2 (Poetry + committed lock file)** because:
1. Index lives in config as originally intended
2. Lock file ensures reproducible installs
3. Works with Poetry's native commands
4. Users never need to remember the index URL

## Files Changed This Session

### Core Package Files
- `stacks/pytorch-cu121/pyproject.toml` - Poetry format, CUDA source configured
- `stacks/pytorch-cu121/ml_stack_pytorch/__init__.py` - Minimal package (created)
- `tests/conftest.py` - Test fixture infrastructure

### Removed
- `detectron2` from vision-extra group (not on PyPI)

### Documentation
- `.github/workflows/test.yml` - Updated for Poetry
- `.github/workflows/README.md` - Updated descriptions
- `CONTRIBUTING.md` - Updated dev setup for Poetry
- `README.md` - Updated install instructions

## Next Steps (Pick One)

### To Go With Option 2 (Recommended):
```bash
cd stacks/pytorch-cu121
poetry lock --no-interaction  # Generates poetry.lock
git add poetry.lock
# Now users just: poetry install --extras ml,vision
```

### To Go With Option 1 (Simpler):
```bash
# Just document the --extra-index-url as standard
# Update README with this as the install method
```

### To Go With Option 3 (Modern):
```bash
# Switch conftest.py to use UV instead
# Update workflows to use UV
```

## Current Project State
- ✅ All 9 groups defined and properly structured
- ✅ Dependencies validated (removed non-existent packages)
- ✅ Test infrastructure ready
- ✅ CI/CD workflows configured
- ⏳ Installation method: Blocked on poetry/pip philosophy choice

Choose your path and ping me. I'm ready to execute whichever option you prefer.
