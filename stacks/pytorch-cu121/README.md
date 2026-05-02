# PyTorch CUDA 12.1 ML Stack

A composable PyTorch ML stack with CUDA 12.1 support. Install only what you need!

## Feature Groups

### Base (always included)
Core data science + EDA libraries — every install gets these:
- numpy (<2.0.0 for compatibility), scipy, pandas
- scikit-learn, joblib (table-stakes for tabular ML)
- matplotlib, seaborn (standard EDA plotting)
- tqdm, pydantic, pyyaml, python-dotenv
- requests, rich

### ML
Core machine learning:
- PyTorch, torchvision, torchaudio (CUDA 12.1)
- PyTorch Lightning
- torchmetrics, torchinfo
- TensorBoard, ONNX, ONNX Runtime
- Triton, einops, Optuna, OmegaConf

### Vision
Basic computer vision:
- OpenCV, OpenCV contrib
- scikit-image, Pillow
- albumentations

### Vision-Extra
Advanced CV frameworks:
- YOLOv8 (ultralytics)
- timm (vision transformers)

### NLP
Core natural language processing:
- Transformers, Datasets, Tokenizers
- SentencePiece
- PEFT, Accelerate
- evaluate, sacrebleu, rouge-score

### NLP-Train
NLP training utilities:
- TRL (Transformer Reinforcement Learning)
- bitsandbytes (quantization)
- DeepSpeed

### Viz
Optional plotting backend (matplotlib + seaborn are in base):
- plotly

### Viz-App
Dashboard & notebook tooling (heavy, opt-in):
- bokeh
- Streamlit, Dash, Gradio
- Jupyter, IPython

### Data
Data processing & ETL (sklearn is in base):
- Polars, Dask
- PyArrow

### GNN
Graph neural networks (heavyweight, opt-in):
- torch-geometric

## Installation

### With Poetry (recommended)
```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install Poetry
pip install poetry

# Install base only
poetry install --no-root

# Install base + specific groups
poetry install --no-root -E ml -E vision
poetry install --no-root -E nlp -E viz

# Add dashboard/notebook tooling or graph nets when needed
poetry install --no-root -E viz-app
poetry install --no-root -E gnn

# Install all
poetry install --no-root -E all
```

Poetry automatically uses the CUDA 12.1 PyTorch index configured in `pyproject.toml`.

## Usage Examples

```python
# Base (always available)
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns

# If installed [ml]
import torch
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

# If installed [viz-app]
import streamlit as st

# If installed [data]
import polars as pl

# If installed [gnn]
from torch_geometric.nn import GCNConv
```

## Testing

All groups are independently tested for compatibility.

From the root directory:
```bash
# Test all groups
pytest -v

# Test specific group
pytest -k "pytorch-cu121-ml"

# Test specific group import test
pytest tests/test_imports.py::TestImports::test_all_imports -k "pytorch-cu121-ml"
```

## Requirements

- Python 3.10, 3.11, or 3.12
- CUDA 12.1 compatible GPU (optional - CPU mode works too)
- ~3GB for base, increases with each group (up to ~50GB for all)

## Disk Usage Estimates

- **base** (incl. sklearn + matplotlib/seaborn): ~1.5GB
- **base + ml**: ~15GB
- **base + ml + vision**: ~20GB
- **base + ml + vision + nlp**: ~30GB
- **base + ml + vision + nlp + viz-app**: ~35GB
- **all**: ~50GB

## Common Combinations

### Beginner (10GB)
```bash
poetry install --no-root -E ml -E vision
```

### LLM Development (30GB)
```bash
poetry install --no-root -E ml -E nlp -E nlp-train
```

### Computer Vision (25GB)
```bash
poetry install --no-root -E ml -E vision -E vision-extra
```

### Full Stack (50GB)
```bash
poetry install --no-root -E all
```

## Dependency Notes

- **numpy** capped at <2.0.0 due to widespread compatibility issues
- All PyTorch packages pinned to compatible versions (torch 2.3.1, torchvision 0.18.1, torchaudio 2.3.1)

## Version Control

- All versions use PyTorch's CUDA 12.1 wheel repository
- Compatible with Python 3.10-3.12
- Tested weekly for dependency compatibility
