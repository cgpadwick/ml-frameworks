# PyTorch CUDA 11.8 ML Stack

A composable PyTorch ML stack with CUDA 11.8 support. Install only what you need!

## Feature Groups

### Base (always included)
PyTorch + the standard scientific-Python toolkit — every install gets these:
- PyTorch 2.3.1, torchvision 0.18.1, torchaudio 2.3.1 (CUDA 11.8)
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

Poetry automatically uses the CUDA 11.8 PyTorch index configured in `pyproject.toml`.

> The previous `nlp-train` extra (TRL / bitsandbytes / DeepSpeed) and `viz-app` extra (Streamlit / Gradio / Jupyter / …) were removed in v0.3.0. Install those packages directly with `pip install ...` if you need them.

## Testing

From the repo root:
```bash
pytest -k "pytorch-cu118" -v
```

## Requirements

- Python 3.10, 3.11, or 3.12
- CUDA 11.8 compatible GPU (typically older NVIDIA driver stacks than CUDA 12.x)
- ~5.5GB for base; up to ~8-9GB for `-E all`

## Dependency Notes

- **numpy** capped at <2.0.0 due to widespread compatibility issues
- PyTorch packages are pinned to a compatible set (torch 2.3.1, torchvision 0.18.1, torchaudio 2.3.1)
- CUDA 11.8 is intended for older systems that can't use CUDA 12.x
