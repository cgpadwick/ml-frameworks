# PyTorch CUDA 13.0 ML Stack (Blackwell / DGX Spark)

A composable PyTorch ML stack with CUDA 13.0 support for NVIDIA Blackwell GPUs (GB10, sm_120/sm_121). Install only what you need!

## Target Hardware

This stack is designed for:
- **NVIDIA DGX Spark** (GB10 GPU + ARM64 Grace CPU)
- **Grace Hopper** systems
- **Blackwell architecture** GPUs (compute capability 12.0/12.1)

## Feature Groups

### Base (always included)
Core data science libraries:
- numpy (<2.0.0 for compatibility)
- scipy, pandas
- tqdm, pydantic, pyyaml, python-dotenv

### ML
Core machine learning:
- PyTorch 2.9.1, torchvision 0.24.1, torchaudio 2.9.1 (CUDA 13.0)
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
- bitsandbytes (quantization) - *may have limited aarch64 support*
- DeepSpeed - *may have limited aarch64 support*

### Viz
Visualization & dashboards:
- matplotlib, seaborn, plotly, bokeh
- Streamlit, Dash, Gradio
- Jupyter, IPython

### Data
Data processing & ETL:
- Polars, Dask
- PyArrow
- scikit-learn

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
pip install torch==2.9.1 torchvision==0.24.1 torchaudio==2.9.1 --index-url https://download.pytorch.org/whl/cu130

# Install other dependencies as needed
pip install transformers datasets accelerate
```

## Usage Examples

```python
# Base (always available)
import numpy as np
import pandas as pd

# If installed [ml]
import torch
import pytorch_lightning as pl

# Verify CUDA 13.0 / Blackwell support
print(f"PyTorch version: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"GPU: {torch.cuda.get_device_name(0)}")
    print(f"Compute capability: {torch.cuda.get_device_capability(0)}")

# If installed [vision]
import cv2
from PIL import Image

# If installed [vision-extra]
from ultralytics import YOLO

# If installed [nlp]
from transformers import AutoTokenizer

# If installed [viz]
import matplotlib.pyplot as plt
import streamlit as st

# If installed [data]
import polars as pl
```

## Known Limitations (ARM64 + CUDA 13.0)

The DGX Spark combines ARM64 (aarch64) with CUDA 13.0, which is a relatively new configuration. Some packages may have limited support:

1. **bitsandbytes**: May not have pre-built aarch64 + cu130 wheels. Build from source if needed.
2. **deepspeed**: ARM64 support may be limited. Check latest releases.
3. **flash-attention**: Not required - PyTorch's native SDPA with cuDNN 9.13 is faster on Blackwell.
4. **pyarrow**: May need cmake installed for building on ARM64.

### Workarounds

If you encounter issues with specific packages:
```bash
# Skip problematic packages in nlp-train
poetry install --no-root -E ml -E nlp -E viz  # Skip nlp-train

# Or install without bitsandbytes/deepspeed
pip install trl  # Just TRL without the quantization/distributed packages
```

## Testing

All groups are independently tested for compatibility.

From the root directory:
```bash
# Test all groups
pytest -v

# Test specific group
pytest -k "pytorch-cu130-ml"

# Test specific group import test
pytest tests/test_imports.py::TestImports::test_all_imports -k "pytorch-cu130-ml"
```

## Requirements

- Python 3.10, 3.11, or 3.12
- CUDA 13.0 compatible GPU (Blackwell architecture: GB10, GB100, GB200)
- NVIDIA driver 560+ with CUDA 13.0 support
- ~3GB for base, increases with each group (up to ~50GB for all)

## Disk Usage Estimates

- **base**: ~1GB
- **base + ml**: ~15GB
- **base + ml + vision**: ~20GB
- **base + ml + vision + nlp**: ~30GB
- **base + ml + vision + nlp + viz**: ~35GB
- **all**: ~50GB

## Common Combinations

### Beginner (10GB)
```bash
poetry install --no-root -E ml -E vision -E viz
```

### LLM Development (30GB)
```bash
poetry install --no-root -E ml -E nlp -E viz
# Note: nlp-train group excluded due to potential ARM64 compatibility issues
```

### Computer Vision (25GB)
```bash
poetry install --no-root -E ml -E vision -E vision-extra -E viz
```

### Full Stack (50GB)
```bash
poetry install --no-root -E all
# Note: Some packages in nlp-train may fail on ARM64
```

## Dependency Notes

- **numpy** capped at <2.0.0 due to widespread compatibility issues
- All PyTorch packages pinned to compatible versions (torch 2.9.1, torchvision 0.24.1, torchaudio 2.9.1)
- CUDA 13.0 required for Blackwell GPUs (sm_120/sm_121)
- pyarrow bumped to ^14.0.0 for better ARM64 wheel availability

## Version Control

- All versions use PyTorch's CUDA 13.0 wheel repository
- Compatible with Python 3.10-3.12
- Tested on DGX Spark (GB10 + ARM64)

## Comparison with Other Stacks

| Stack | CUDA | PyTorch | Target GPUs |
|-------|------|---------|-------------|
| pytorch-cu118 | 11.8 | 2.1.x | Ampere, older |
| pytorch-cu121 | 12.1 | 2.3.x | Ampere, Ada Lovelace |
| pytorch-cu126 | 12.6 | 2.9.0 | Ampere, Ada, Hopper |
| **pytorch-cu130** | **13.0** | **2.9.1** | **Blackwell (GB10, etc.)** |
