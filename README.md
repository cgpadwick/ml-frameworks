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

- **pytorch-cu130** - Complete PyTorch stack with CUDA 13.0 (Blackwell)
  - PyTorch 2.9.1, Lightning, transformers, YOLOv8, timm
  - NLP, vision, data processing, visualization, dev tools
  - ~50GB installation
  - Recommended for NVIDIA Blackwell GPUs (DGX Spark GB10, sm_120/sm_121)

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

# cd into the stack you want, then run ONE of the install variants below.
# Note: each `poetry install` replaces the previously-installed extras;
# the lines below are alternatives, not steps to run in sequence.

# CUDA 11.8 / 12.1 / 12.6 / 13.0:
cd stacks/pytorch-cu121          # or pytorch-cu118 / pytorch-cu126 / pytorch-cu130

poetry install --no-root                        # base only (numpy, pandas, sklearn, matplotlib, seaborn, ...)
poetry install --no-root -E ml -E vision        # base + ml + vision
poetry install --no-root -E ml -E nlp           # base + ml + nlp
poetry install --no-root -E all                 # everything (~50GB)
```

The **base** install is no longer minimal: it now includes scikit-learn, matplotlib, seaborn, joblib, requests, and rich — the standard tabular-ML / EDA toolkit. See the [Stack Groups table](#pytorch-stack-groups) below for what the optional `-E ...` groups add.

**Windows:**
```bat
python -m venv .venv
.venv\Scripts\activate

pip install poetry

cd stacks\pytorch-cu121          REM or pytorch-cu118 / pytorch-cu126 / pytorch-cu130
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
│   ├── pytorch-cu118/      # PyTorch with CUDA 11.8
│   ├── pytorch-cu121/      # PyTorch with CUDA 12.1
│   │   ├── pyproject.toml  # Stack dependencies
│   │   └── README.md       # Stack documentation
│   ├── pytorch-cu126/      # PyTorch with CUDA 12.6
│   │   ├── pyproject.toml  # Stack dependencies
│   │   └── README.md       # Stack documentation
│   ├── pytorch-cu130/      # PyTorch with CUDA 13.0 (Blackwell/DGX Spark)
│   │   ├── pyproject.toml  # Stack dependencies
│   │   └── README.md       # Stack documentation
│   └── all-cu121/          # (Coming soon)
└── tests/                  # Shared test infrastructure
    ├── conftest.py         # Parametrized fixtures for all stacks
    └── test_imports.py     # Import & compatibility tests
```

## PyTorch Stack Groups

`pytorch-cu118`, `pytorch-cu121`, `pytorch-cu126`, and `pytorch-cu130` share the same modular structure: a `base` install that ships with every stack, plus 9 optional groups you can layer on with `-E`. The main differences are the CUDA and PyTorch versions. Install only what you need!

| Group | Purpose | Key Packages |
|-------|---------|--------------|
| **base** *(always installed)* | Core data + EDA toolkit | numpy, pandas, scipy, scikit-learn, joblib, matplotlib, seaborn, pydantic, requests, rich |
| **ml** | ML training | PyTorch, Lightning, ONNX, Triton, Optuna |
| **vision** | Basic CV | OpenCV, Pillow, albumentations, scikit-image |
| **vision-extra** | Advanced CV | YOLOv8, timm |
| **nlp** | NLP tasks | transformers, datasets, PEFT, accelerate |
| **nlp-train** | NLP training | TRL, bitsandbytes, DeepSpeed |
| **viz** | Extra plotting backend | plotly |
| **viz-app** | Dashboards & notebooks | bokeh, streamlit, dash, gradio, jupyter, ipython |
| **data** | Data processing & ETL | Polars, Dask, PyArrow |
| **gnn** | Graph neural networks | torch-geometric (+ torch, torchvision, torchaudio) |
| **all** | Everything | Union of all groups above |

### Installation Examples

Choose your CUDA version (cu118 / cu121 / cu126 / cu130), then pick **one** install line — each `poetry install` replaces the prior set of extras, so you can't compose them by running multiple lines in sequence.

```bash
cd stacks/pytorch-cu121          # or pytorch-cu118 / pytorch-cu126 / pytorch-cu130

poetry install --no-root                              # base only (sklearn + matplotlib + seaborn included)
poetry install --no-root -E ml                        # base + ml
poetry install --no-root -E ml -E vision              # base + ml + vision
poetry install --no-root -E ml -E nlp                 # base + ml + nlp
poetry install --no-root -E ml -E vision -E viz-app   # base + ml + vision + dashboards
poetry install --no-root -E gnn                       # base + torch + torch-geometric (graph nets)
poetry install --no-root -E all                       # everything
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
- **11 dependency groups** independently tested (base, ml, vision, vision-extra, nlp, nlp-train, viz, viz-app, data, gnn, all)
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
