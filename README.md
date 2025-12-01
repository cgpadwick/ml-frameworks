# ML Frameworks

[![Tests](https://github.com/yourusername/ml-frameworks/workflows/Test%20ML%20Stacks/badge.svg)](https://github.com/yourusername/ml-frameworks/actions)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Composable, tested ML stacks - install only what you need. Each stack is independently validated for compatibility with GitHub Actions CI/CD.

## Available Stacks

Currently available:

- **pytorch-cu121** - Complete PyTorch stack with CUDA 12.1
  - PyTorch, Lightning, transformers, YOLOv8, timm, MMDetection
  - NLP, vision, data processing, visualization, dev tools
  - ~50GB installation

Planned:
- **pytorch-cu118** - PyTorch with CUDA 11.8 (for older systems)
- **all-cu121** - All-in-one (PyTorch + TensorFlow + everything)
- **tensorflow-cu121** - TensorFlow alternative

## Quick Start

### Install UV (Recommended)

UV is significantly faster than pip and poetry:

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**
```bash
powershell -ExecutionPolicy BypassUser -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Install a Stack

**With Poetry (Recommended):**
```bash
# Create virtual environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install Poetry
pip install poetry

# Install a stack from its directory (with specific groups)
cd stacks/pytorch-cu121
poetry install --extras ml,vision        # Install base + ml + vision groups
poetry install --extras all              # Install all groups
poetry install                           # Install base only
```

**Or with pip + index URL (legacy):**
```bash
python -m venv venv
source venv/bin/activate
cd stacks/pytorch-cu121
pip install -e . --index-url https://download.pytorch.org/whl/cu121
```

## Testing

Each stack is tested independently in isolated environments to verify compatibility.

Run tests:
```bash
# From root directory
cd stacks/pytorch-cu121
poetry install --extras all  # Install all dependencies for testing
cd ../..
poetry run pytest tests -v

# Or test specific group
cd stacks/pytorch-cu121
poetry install --extras ml
cd ../..
poetry run pytest tests -k "pytorch-cu121-ml" -v
```

Tests will:
1. Build a fresh venv for each discovered stack
2. Install that stack's dependencies with appropriate CUDA version (via Poetry sources)
3. Verify every package imports successfully
4. Check CUDA availability (PyTorch stacks)
5. Validate major framework versions

## Project Structure

```
ml-frameworks/
├── pyproject.toml          # Root package (metadata + test config)
├── pytest.ini              # Pytest configuration
├── README.md               # This file
├── .gitignore              # Git ignore rules
├── ml_frameworks/          # Root Python package
│   └── __init__.py
├── stacks/                 # Stack definitions
│   ├── pytorch-cu121/      # PyTorch with CUDA 12.1
│   │   ├── pyproject.toml  # Stack dependencies
│   │   └── README.md       # Stack documentation
│   ├── pytorch-cu118/      # (Coming soon)
│   └── all-cu121/          # (Coming soon)
└── tests/                  # Shared test infrastructure
    ├── conftest.py         # Parametrized fixtures for all stacks
    └── test_imports.py     # Import & compatibility tests
```

## pytorch-cu121 Stack

A modular PyTorch stack with 9 optional dependency groups:

| Group | Purpose | Key Packages |
|-------|---------|--------------|
| **base** | Core data science | numpy, pandas, scipy |
| **ml** | ML training | PyTorch, Lightning, ONNX, Triton |
| **vision** | Basic CV | OpenCV, Pillow, albumentations |
| **vision-extra** | Advanced CV | YOLOv8, timm, MMDetection, Detectron2 |
| **nlp** | NLP tasks | transformers, datasets, PEFT |
| **nlp-train** | NLP training | TRL, bitsandbytes, DeepSpeed, flash-attn |
| **viz** | Visualization | matplotlib, plotly, streamlit, jupyter |
| **data** | Data processing | Polars, Dask, PyArrow, scikit-learn |
| **dev** | Developer tools | pytest, black, ruff, mypy |

Install only what you need:
```bash
uv pip install -e stacks/pytorch-cu121              # base only
uv pip install -e stacks/pytorch-cu121[ml]          # base + ml
uv pip install -e stacks/pytorch-cu121[ml,vision]   # base + ml + vision
uv pip install -e stacks/pytorch-cu121[all]         # everything
```

Each group is independently tested for compatibility!

## Requirements

- Python 3.10, 3.11, or 3.12
- CUDA compatible GPU (or CPU mode)
- ~50GB disk space for full pytorch-cu121 installation

## Adding New Stacks

To add a new stack variant:

1. Create directory: `stacks/pytorch-cu118/`
2. Copy and modify `pyproject.toml` (change CUDA version, dependencies)
3. Add `README.md` with stack documentation
4. Run `pytest` - your stack will be auto-discovered and tested!

Example:
```bash
mkdir -p stacks/pytorch-cu118
cp stacks/pytorch-cu121/pyproject.toml stacks/pytorch-cu118/
# Edit to use CUDA 11.8 PyTorch index
pytest  # Automatically discovered!
```

## Development

To work on the test infrastructure:

```bash
cd /path/to/ml-frameworks
uv venv
source .venv/bin/activate
uv pip install -e .
pytest -v
```

## CI/CD & Testing

Every push runs automated tests across all dependency groups:

- **18 parallel jobs** (Python 3.10, 3.11 × 9 groups)
- **80 import tests** validating package compatibility
- **Framework version checks** for major libraries
- **Linting** with black and ruff
- **~30-45 minutes** total (optimized with pip caching)

Tests run on every push and PR. Failures block merge.

See [.github/workflows/README.md](.github/workflows/README.md) for details.

## License

MIT
