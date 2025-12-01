# Changelog

All notable changes to ML Frameworks will be documented in this file.

## [Unreleased]

### Added
- Initial release of pytorch-cu121 stack
- 9 optional dependency groups: ml, vision, vision-extra, nlp, nlp-train, viz, data, dev
- Comprehensive test suite with 80 tests across all groups
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
