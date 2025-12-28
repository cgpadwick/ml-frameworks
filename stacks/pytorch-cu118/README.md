# PyTorch CUDA 11.8 ML Stack

A composable PyTorch ML stack with CUDA 11.8 support. Install only what you need!

## Feature Groups

### Base (always included)
Core data science libraries:
- numpy (<2.0.0 for compatibility)
- scipy, pandas
- tqdm, pydantic, pyyaml, python-dotenv

### ML
Core machine learning:
- PyTorch, torchvision, torchaudio (CUDA 11.8)
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

Poetry automatically uses the CUDA 11.8 PyTorch index configured in `pyproject.toml`.

## Testing

From the repo root:
```bash
pytest -k "pytorch-cu118" -v
```

## Requirements

- Python 3.10, 3.11, or 3.12
- CUDA 11.8 compatible GPU (typically older NVIDIA driver stacks than CUDA 12.x)
- Disk usage depends on groups (up to ~50GB for `all`)

## Dependency Notes

- **numpy** capped at <2.0.0 due to widespread compatibility issues
- PyTorch packages are pinned to a compatible set (torch 2.3.1, torchvision 0.18.1, torchaudio 2.3.1)
- CUDA 11.8 is intended for older systems that can’t use CUDA 12.x
