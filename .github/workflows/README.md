# GitHub Actions Workflows

Automated testing and deployment workflows for ML Frameworks stacks.

## Workflows

### test.yml - Main Test Suite

**Triggers:** Push to main/develop, pull requests

**Matrix Testing:**
- Python versions: 3.10, 3.11
- Stacks: pytorch-cu118, pytorch-cu121, pytorch-cu126
- Groups: base, ml, vision, vision-extra, nlp, nlp-train, viz, data, dev, all
- Total: 18 test jobs (excludes 'all' on Python 3.10 to save CI time)

**What it does:**
1. Checks out code
2. Sets up Python + Poetry
3. Creates venv for each group
4. Installs stack dependencies with CUDA 12.1 PyTorch (via Poetry sources)
5. Runs import tests
6. Validates framework versions
7. Runs linting (black, ruff)

**Expected duration:** ~30-45 minutes total (10+ parallel jobs)

**Artifacts:** Test reports (if configured)

### release.yml - PyPI Release

**Triggers:** Git tags matching `v*` (e.g., `v1.0.0`)

**What it does:**
1. Builds wheel distribution
2. Validates package contents
3. Publishes to PyPI (with token-based auth)
4. Creates GitHub Release

**Requirements:**
- PyPI trusted publisher configured
- GitHub environment `pypi` with proper permissions

## Status Badges

Add to README.md:

```markdown
![Tests](https://github.com/yourname/ml-frameworks/workflows/Test%20ML%20Stacks/badge.svg)
![Release](https://github.com/yourname/ml-frameworks/workflows/Release%20to%20PyPI/badge.svg)
```

## CI/CD Strategy

### Test Parallelization
- **Matrix jobs** run each group on separate runners
- **No conflicts** - isolated disk, network, memory per job
- **Fast feedback** - all jobs run simultaneously
- **Robust** - failure in one group doesn't block others

### Dependency Caching
- `actions/setup-python` with `cache: 'pip'` caches pip packages
- Significantly speeds up subsequent runs (saves 5-10 minutes)

### CUDA Considerations
- PyTorch CUDA index configured in each stack `pyproject.toml` via Poetry sources (cu118, cu121, cu126)
- Poetry respects source priorities automatically
- CPU-only PyTorch still works in GitHub Actions runners
- CUDA tests gracefully skip if not available

## Local Development

To mimic CI locally:

```bash
# Test all groups sequentially (faster locally)
pytest -v

# Or test specific group
pytest -k "pytorch-cu121-ml" -v

# Run linting
black . --check
ruff check .
```

## Troubleshooting

### Tests timeout (>120 min)
- Reduce matrix size temporarily
- Cache issue? Clear GitHub Actions cache
- PyPI CDN slow? Tests will retry

### Memory/disk issues
- Matrix job limits: ~50GB disk, ~7GB RAM available
- Reduce number of parallel matrix dimensions
- Monitor Actions logs for OOM errors

### PyPI publish fails
- Verify trusted publisher is configured
- Check PyPI token hasn't expired
- Ensure package version is unique

## Adding New Groups

When adding new groups to `pyproject.toml`:

1. **Workflow auto-detects via matrix** - no workflow changes needed!
2. Test immediately passes on next push
3. If it fails, fix dependencies and push again

## Future Enhancements

- [ ] Nightly tests on CPU-only runners
- [ ] Benchmark tracking (install time per group)
- [ ] Docker image builds for pre-built stacks
- [ ] Automated dependency updates (Dependabot)
- [ ] Coverage reports
- [ ] Performance regression detection
