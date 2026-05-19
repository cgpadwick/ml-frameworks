# Changelog

All notable changes to ML Frameworks will be documented in this file.

## [Unreleased]

### Changed (v0.3.0) — breaking
- **Promoted PyTorch + pytest into base.** `torch`, `torchvision`, `torchaudio`, `pytest`, and `pytest-cov` are now always installed. Base goes from ~1.5GB to ~5.5GB but `import torch` and post-install verification work out of the box without any `-E ...` flags. Targets fast cold-start for downstream tools (e.g. MLE-Beast) that auto-create environments.
- **Renamed `ml` extra to `training`.** Torch itself moved to base, so the extra now contains just the PyTorch ecosystem add-ons (Lightning, ONNX, Triton, Optuna, …). Update any `-E ml` invocations to `-E training`.
- **Dropped `nlp-train` extra.** TRL, bitsandbytes, and DeepSpeed are no longer offered as a maintained group — install them directly if you need them. They had no documented use case in this repo and were the heaviest CUDA-touching deps in `-E all`.
- **Dropped `viz-app` extra.** Streamlit, Gradio, Dash, Bokeh, Jupyter, IPython are no longer offered as a maintained group — install directly if you need them. These were dashboard / notebook tooling, unused by automated ML pipelines.
- **`gnn` extra slimmed down.** Now just `torch-geometric` (torch came along into base).
- **`-E all` shrunk** to ~8-9GB installed (was 20-30GB+) because `nlp-train` and `viz-app` no longer feed into it.

Net effect: the CI test matrix drops from 11 groups to 9 (base, training, vision, vision-extra, nlp, viz, data, gnn, all).

### Added (prior)
- Initial release of pytorch-cu121 stack
- Comprehensive test suite with parametrized fixtures across all groups
- GitHub Actions CI/CD pipeline with matrix testing
- Support for Python 3.10, 3.11, 3.12

### Features
- **pytorch-cu121**: Complete PyTorch stack with CUDA 12.1 support
- **Optional groups**: Install only what you need
- **Tested compatibility**: Each group independently validated
- **PyTorch index support**: Automatic download from official CUDA 12.1 wheels
- **uv and pip compatible**: Works with both package managers

### Documentation
- Comprehensive README with installation examples
- Stack-specific documentation for pytorch-cu121
- CI/CD workflow documentation
- Development setup guide

## Planned Releases

### v1.0.0 (Planned)
- pytorch-cu121 stable release
- pytorch-cu118 support for older systems
- Documentation site

### v1.1.0 (Planned)
- all-cu121 (PyTorch + TensorFlow combined)
- tensorflow-cu121 stack
- Automated dependency updates

### v2.0.0 (Planned)
- Additional stacks (JAX, Hugging Face optimized, etc.)
- Pre-built Docker images
- Performance benchmarks
- Community-contributed stacks
