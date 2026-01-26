# ML Frameworks

[![Tests](https://github.com/cgpadwick/ml-frameworks/workflows/Test%20ML%20Stacks/badge.svg)](https://github.com/cgpadwick/ml-frameworks/actions)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Composable, tested ML stacks - install only what you need. Each stack is independently validated for compatibility with GitHub Actions CI/CD.

## Available Stacks

Currently available:

- **pytorch-cu121** - Complete PyTorch stack with CUDA 12.1
  - PyTorch 2.3.1, Lightning, transformers, YOLOv8, timm
  - NLP, vision, data processing, visualization, dev tools
  - ~50GB installation
  - Recommended for wider GPU compatibility

- **pytorch-cu118** - Complete PyTorch stack with CUDA 11.8
  - PyTorch 2.3.1, Lightning, transformers, YOLOv8, timm
  - NLP, vision, data processing, visualization, dev tools
  - ~50GB installation
  - Recommended for older driver stacks / systems that can't use CUDA 12.x

- **pytorch-cu126** - Complete PyTorch stack with CUDA 12.6
  - PyTorch 2.9.0, Lightning, transformers, YOLOv8, timm
  - NLP, vision, data processing, visualization, dev tools
  - ~50GB installation
  - Recommended for newer GPUs (Ampere/Hopper architectures)

Planned:
- **all-cu121** - All-in-one (PyTorch + TensorFlow + everything)
- **tensorflow-cu121** - TensorFlow alternative

## Quick Start

### Install a Stack with Poetry

**macOS/Linux:**
```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate

# Install Poetry
pip install poetry

# Install stack with desired groups
# For CUDA 11.8:
cd stacks/pytorch-cu118
poetry install --no-root -E ml -E vision        # base + ml + vision groups
poetry install --no-root -E all                 # all groups
poetry install --no-root                        # base only

# For CUDA 12.1:
cd stacks/pytorch-cu121
poetry install --no-root -E ml -E vision        # base + ml + vision groups
poetry install --no-root -E all                 # all groups
poetry install --no-root                        # base only

# For CUDA 12.6:
cd stacks/pytorch-cu126
poetry install --no-root -E ml -E vision        # base + ml + vision groups
```

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate

pip install poetry

# For CUDA 11.8:
cd stacks\pytorch-cu118
poetry install --no-root -E ml -E vision

# For CUDA 12.1:
cd stacks\pytorch-cu121
poetry install --no-root -E ml -E vision

# For CUDA 12.6:
cd stacks\pytorch-cu126
poetry install --no-root -E ml -E vision
```

### Why Poetry?

Poetry reads the CUDA PyTorch index configuration from `pyproject.toml` automatically. The lock file (`poetry.lock`) ensures reproducible installs across all environments.

## Testing

Tests create fresh virtual environments for each stack and dependency group to verify all packages install and import correctly.

**Run all tests:**
```bash
pytest tests/test_imports.py -v
```

**Run tests for specific group:**
```bash
pytest tests/test_imports.py -k "pytorch-cu118-ml" -v
pytest tests/test_imports.py -k "pytorch-cu121-ml" -v
```

**Run specific test class:**
```bash
pytest tests/test_imports.py::TestImports -v
```

### What Tests Do

For each dependency group:
1. Create a fresh Python 3.10 virtual environment
2. Install Poetry into the venv
3. Run `poetry install --no-root -E {group}` to install that group's dependencies
4. Verify every package imports successfully
5. Test CUDA functionality (if torch is installed)
6. Validate major framework versions (torch, transformers, etc.)

**Note:** Tests are slow because each group gets its own fresh venv and full Poetry installation. Plan for 2-5 minutes per group depending on dependencies.

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
│   ├── pytorch-cu126/      # PyTorch with CUDA 12.6
│   │   ├── pyproject.toml  # Stack dependencies
│   │   └── README.md       # Stack documentation
│   ├── pytorch-cu118/      # PyTorch with CUDA 11.8
│   └── all-cu121/          # (Coming soon)
└── tests/                  # Shared test infrastructure
    ├── conftest.py         # Parametrized fixtures for all stacks
    └── test_imports.py     # Import & compatibility tests
```

## PyTorch Stack Groups

`pytorch-cu118`, `pytorch-cu121`, and `pytorch-cu126` share the same modular structure with 9 optional dependency groups. The main differences are the CUDA and PyTorch versions. Install only what you need!

| Group | Purpose | Key Packages |
|-------|---------|--------------|
| **base** | Core data science | numpy, pandas, scipy, pydantic |
| **ml** | ML training | PyTorch, Lightning, ONNX, Triton, Optuna |
| **vision** | Basic CV | OpenCV, Pillow, albumentations, scikit-image |
| **vision-extra** | Advanced CV | YOLOv8, timm |
| **nlp** | NLP tasks | transformers, datasets, PEFT, accelerate |
| **nlp-train** | NLP training | TRL, bitsandbytes, DeepSpeed |
| **viz** | Visualization | matplotlib, plotly, streamlit, jupyter |
| **data** | Data processing | Polars, Dask, PyArrow, scikit-learn |
| **all** | Everything | All of the above |

### Installation Examples

Choose your CUDA version (cu118, cu121, or cu126) and install the groups you need:

```bash
# For CUDA 11.8:
cd stacks/pytorch-cu118

# For CUDA 12.1:
cd stacks/pytorch-cu121

# For CUDA 12.6:
cd stacks/pytorch-cu126

# Then install desired groups:
poetry install --no-root                    # base only
poetry install --no-root -E ml              # base + ml
poetry install --no-root -E ml -E vision    # base + ml + vision
poetry install --no-root -E all             # everything
```

Each group is independently tested for compatibility across all CUDA variants!

## Requirements

- Python 3.10, 3.11, or 3.12
- CUDA compatible GPU (or CPU mode)
- ~50GB disk space for a full PyTorch stack (`-E all`)

## Adding New Stacks

To add a new stack variant:

1. Create directory: `stacks/pytorch-cu117/`
2. Copy and modify `pyproject.toml` (change CUDA version, dependencies)
3. Add `README.md` with stack documentation
4. Run `pytest` - your stack will be auto-discovered and tested!

Example:
```bash
mkdir -p stacks/pytorch-cu117
cp stacks/pytorch-cu121/pyproject.toml stacks/pytorch-cu117/
# Edit to use CUDA 11.8 PyTorch index
pytest  # Automatically discovered!
```

## Development

To work on the test infrastructure:

```bash
cd /path/to/ml-frameworks
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install pytest tomli   # tomli for Python 3.10 compatibility
pytest tests/test_imports.py -v
```

## CI/CD & Testing

Every push runs automated tests across all dependency groups. Tests create fresh environments for each group to ensure isolation and reproducibility.

**Test Coverage:**
- **9 dependency groups** independently tested (base, ml, vision, vision-extra, nlp, nlp-train, viz, data, all)
- **Package imports** verified for all dependencies
- **Framework versions** validated (torch, transformers, lightning, etc.)
- **CUDA functionality** tested (with graceful skip on CPU-only systems)
- **Linting & formatting** with black and ruff

**Execution:**
- Each group gets a fresh venv and Poetry installation
- Estimated ~2-5 minutes per group depending on dependencies
- Total runtime: ~20-45 minutes for full suite

Tests run on every push and PR. Failures block merge.

See [.github/workflows/README.md](.github/workflows/README.md) for workflow configuration details.

## License

MIT
