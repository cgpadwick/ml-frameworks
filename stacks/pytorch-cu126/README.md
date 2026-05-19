# PyTorch CUDA 12.6 ML Stack

A composable PyTorch ML stack with CUDA 12.6 support. Install only what you need!

## Feature Groups

### Base (always included)
PyTorch + the standard scientific-Python toolkit — every install gets these:
- PyTorch 2.9.0, torchvision 0.24.0, torchaudio 2.9.0 (CUDA 12.6)
- numpy (<2.0.0 for compatibility), scipy, pandas
- scikit-learn, joblib (table-stakes for tabular ML)
- matplotlib, seaborn (standard EDA plotting)
- tqdm, pydantic, pyyaml, python-dotenv
- requests, rich
- pytest, pytest-cov (so post-install verification works without extras)

### training
PyTorch ecosystem add-ons:
- PyTorch Lightning
- torchmetrics, torchinfo
- TensorBoard, ONNX, ONNX Runtime
- Triton, einops, Optuna, OmegaConf

### vision
Basic computer vision:
- OpenCV, OpenCV contrib
- scikit-image, Pillow
- albumentations

### vision-extra
Advanced CV frameworks:
- YOLOv8 (ultralytics)
- timm (vision transformers)

### nlp
Core natural language processing:
- Transformers, Datasets, Tokenizers
- SentencePiece
- PEFT, Accelerate
- evaluate, sacrebleu, rouge-score

### viz
Extra plotting backend (matplotlib + seaborn are in base):
- plotly

### data
Data processing & ETL (sklearn is in base):
- Polars, Dask
- PyArrow

### gnn
Graph neural networks (torch is in base, so this is just the GNN bits):
- torch-geometric

## Installation

### With Poetry (recommended)
```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install Poetry
pip install poetry

# Install base only (PyTorch + scientific Python, ~5.5GB)
poetry install --no-root

# Install base + specific groups
poetry install --no-root -E training -E vision
poetry install --no-root -E nlp -E viz

# Graph nets when needed
poetry install --no-root -E gnn

# Install all
poetry install --no-root -E all
```

Poetry automatically uses the CUDA 12.6 PyTorch index configured in `pyproject.toml`.

## Usage Examples

```python
# Base (always available)
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
import torch

# If installed [training]
import pytorch_lightning as pl

# If installed [vision]
import cv2
from PIL import Image

# If installed [vision-extra]
from ultralytics import YOLO

# If installed [nlp]
from transformers import AutoTokenizer

# If installed [viz]
import plotly.express as px

# If installed [data]
import polars as pl

# If installed [gnn]
from torch_geometric.nn import GCNConv
```

> The previous `nlp-train` extra (TRL / bitsandbytes / DeepSpeed) and `viz-app` extra (Streamlit / Gradio / Jupyter / …) were removed in v0.3.0. Install those packages directly with `pip install ...` if you need them.

## Testing

All groups are independently tested for compatibility.

From the root directory:
```bash
# Test all groups
pytest -v

# Test specific group
pytest -k "pytorch-cu126-training"

# Test specific group import test
pytest tests/test_imports.py::TestImports::test_all_imports -k "pytorch-cu126-training"
```

## Requirements

- Python 3.10, 3.11, or 3.12
- CUDA 12.6 compatible GPU (Ampere/Hopper architectures recommended)
- ~5.5GB for base; up to ~8-9GB for `-E all`

## Disk Usage Estimates

- **base** (PyTorch + sklearn + matplotlib/seaborn + pytest): ~5.5GB
- **base + training**: ~6GB
- **base + training + vision**: ~6.5GB
- **base + training + vision + nlp**: ~8GB
- **all**: ~8-9GB

## Common Combinations

### Vision development
```bash
poetry install --no-root -E training -E vision -E vision-extra
```

### LLM development
```bash
poetry install --no-root -E training -E nlp
```

### Full stack
```bash
poetry install --no-root -E all
```

## Dependency Notes

- **numpy** capped at <2.0.0 due to widespread compatibility issues
- All PyTorch packages pinned to compatible versions (torch 2.9.0, torchvision 0.24.0, torchaudio 2.9.0)
- CUDA 12.6 recommended for newer GPUs (Ampere/Hopper architectures)

## Version Control

- All versions use PyTorch's CUDA 12.6 wheel repository
- Compatible with Python 3.10-3.12
- Tested weekly for dependency compatibility
