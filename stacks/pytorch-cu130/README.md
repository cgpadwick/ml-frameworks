# PyTorch CUDA 13.0 ML Stack (Blackwell / DGX Spark)

A composable PyTorch ML stack with CUDA 13.0 support for NVIDIA Blackwell GPUs (GB10, sm_120/sm_121). Install only what you need!

## Target Hardware

This stack is designed for:
- **NVIDIA DGX Spark** (GB10 GPU + ARM64 Grace CPU)
- **Grace Hopper** systems
- **Blackwell architecture** GPUs (compute capability 12.0/12.1)

## Feature Groups

### Base (always included)
PyTorch + the standard scientific-Python toolkit — every install gets these:
- PyTorch 2.10.0, torchvision 0.25.0, torchaudio 2.10.0 (CUDA 13.0)
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
- OpenCV (opencv-contrib-python - includes all opencv-python features plus extra modules)
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

Poetry automatically uses the CUDA 13.0 PyTorch index configured in `pyproject.toml`.

### With pip
```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate

# Install PyTorch with CUDA 13.0
pip install torch==2.10.0 torchvision==0.25.0 torchaudio==2.10.0 --index-url https://download.pytorch.org/whl/cu130

# Install other dependencies as needed
pip install transformers datasets accelerate
```

## Usage Examples

```python
# Base (always available)
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
import torch

# Verify CUDA 13.0 / Blackwell support
print(f"PyTorch version: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"GPU: {torch.cuda.get_device_name(0)}")
    print(f"Compute capability: {torch.cuda.get_device_capability(0)}")

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

## Known Limitations (ARM64 + CUDA 13.0)

The DGX Spark combines ARM64 (aarch64) with CUDA 13.0, which is a relatively new configuration. Some packages may have limited support:

1. **flash-attention**: Not required - PyTorch's native SDPA with cuDNN 9.13 is faster on Blackwell.
2. **pyarrow**: May need cmake installed for building on ARM64.

> The previous `nlp-train` extra (TRL / bitsandbytes / DeepSpeed) and `viz-app` extra (Streamlit / Gradio / Jupyter / …) were removed in v0.3.0. Install those packages directly with `pip install ...` if you need them.

## Testing

All groups are independently tested for compatibility.

From the root directory:
```bash
# Test all groups
pytest -v

# Test specific group
pytest -k "pytorch-cu130-training"

# Test specific group import test
pytest tests/test_imports.py::TestImports::test_all_imports -k "pytorch-cu130-training"
```

## Requirements

- Python 3.10, 3.11, or 3.12
- CUDA 13.0 compatible GPU (Blackwell architecture: GB10, GB100, GB200)
- NVIDIA driver 560+ with CUDA 13.0 support
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
- All PyTorch packages pinned to compatible versions (torch 2.10.0, torchvision 0.25.0, torchaudio 2.10.0)
- CUDA 13.0 required for Blackwell GPUs (sm_120/sm_121)
- pyarrow bumped to ^14.0.0 for better ARM64 wheel availability

## Version Control

- All versions use PyTorch's CUDA 13.0 wheel repository
- Compatible with Python 3.10-3.12
- Tested on DGX Spark (GB10 + ARM64)

## Comparison with Other Stacks

| Stack | CUDA | PyTorch | Target GPUs |
|-------|------|---------|-------------|
| pytorch-cu118 | 11.8 | 2.3.1 | Ampere, older |
| pytorch-cu121 | 12.1 | 2.3.1 | Ampere, Ada Lovelace |
| pytorch-cu126 | 12.6 | 2.9.0 | Ampere, Ada, Hopper |
| **pytorch-cu130** | **13.0** | **2.10.0** | **Blackwell (GB10, etc.)** |
