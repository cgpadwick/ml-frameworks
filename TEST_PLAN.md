# Test Plan - Analysis & Fixes Needed

## Current State Analysis

### conftest.py Issues

**1. Wrong pyproject.toml Format (CRITICAL)**
- **Line 44, 88, 94**: Expects `project.optional-dependencies` (setuptools format)
- **Actually has**: `tool.poetry.dependencies` and `tool.poetry.extras` (Poetry format)
- **Impact**: `get_groups_for_stack()` will return empty list, `dependencies` fixture will fail to find groups

**2. Using pip instead of Poetry (CRITICAL)**
- **Lines 181-199**: Uses `pip install -e [stack_path][group]` with `--extra-index-url`
- **Problem**: pip doesn't read Poetry's `[[tool.poetry.source]]` configuration
- **Impact**: This simulates a user running pip, NOT how users would actually install (they'd use `poetry install`)

**3. Dependency Parsing Doesn't Handle Poetry Format**
- **Lines 117-130**: Tries to parse version specs from dependency strings
- **Current**: Parses `package-name>=1.0.0` format
- **Actually**: Poetry stores as either:
  - Simple: `torch = {version = "2.3.1", source = "pytorch-cu121", optional = true}`
  - Complex: `torch = "^2.3.1"`
- **Impact**: Parse logic will still work but is fragile and unnecessary

**4. Hardcoded Package Mappings (MINOR)**
- **Lines 98-113**: Has hardcoded `flash-attn` import which we just removed
- **Missing mappings**: No mapping for many newer packages added to groups
- **Impact**: Falls back to default for unmapped packages, which often works but is inconsistent

### test_imports.py Issues

**1. Too Strict Import Testing**
- **Lines 29-51**: Tests `import X; assert X.__version__` for every package
- **Problem**: Some packages don't have `__version__` at top level (e.g., PIL.Image doesn't have it)
- **Impact**: False negatives for valid imports

**2. TestFrameworkVersions Tests Non-Existent Packages**
- **Lines 96-103**: Tests mmcv and mmdet unconditionally in @parametrize
- **Problem**: These won't be in all groups, and mmcv might not even be in our stacks
- **Impact**: These tests will either skip or fail in confusing ways

**3. CUDA Test Too Strict**
- **Lines 69-88**: `assert torch.cuda.is_available()`
- **Problem**: WSL2 often doesn't have GPU passthrough, system CI might not have GPU
- **Impact**: Test skips even on valid installations, reducing confidence

**4. Dependencies Processing Logic is Convoluted**
- **Lines 77-95**: Complex if/else to handle "base" special case
- **Problem**: Mixes reading from pyproject and instantiating the test
- **Impact**: Hard to debug, mixes concerns

## Design Issues (Not Bugs, But Problematic)

### Not Testing How Users Actually Install
- **Current**: Uses pip editable install (`pip install -e`)
- **User reality**: Would use `poetry install -E group` (as documented in stack README)
- **Impact**: Tests pass but don't validate the actual user installation flow

### Not Using poetry.lock
- **Current**: Tests ignore poetry.lock completely
- **Better**: Tests should validate poetry.lock can be used directly
- **Impact**: Doesn't verify reproducible installs work

### Test Environment Setup is Slow
- **Current**: Creates fresh venv + installs for each group from scratch
- **Better**: Could reuse venv with different extras installed, or use poetry directly
- **Impact**: Tests take forever, not suitable for CI quick feedback

## What the Tests Should Actually Do (User Perspective)

A real user would:
1. Clone the repo
2. `cd stacks/pytorch-cu121`
3. `poetry install` or `poetry install -E ml,vision`
4. Try to import packages and use them

**Our tests should simulate exactly this flow.**

---

## Fix Plan

### Phase 1: Update conftest.py to Handle Poetry Format

**Changes needed:**

1. **Update `get_groups_for_stack()` (line 33-46)**
   - Read from `tool.poetry.extras` instead of `project.optional-dependencies`
   - Return list of group names (already does this correctly)
   - Verify detection works with Poetry format

2. **Update `dependencies` fixture (line 77-132)**
   - Parse `tool.poetry.dependencies` for base deps
   - Parse `tool.poetry.extras[group]` for optional deps
   - Build import statements more intelligently:
     - For most packages: just `import {package_name}` (no version check)
     - For special cases (opencv, pyyaml, etc.): use known import names
   - Remove flash-attn from package mappings
   - Simplify logic to just return valid packages from extras

3. **Update `test_env` fixture (line 136-210)** - THIS IS THE KEY CHANGE
   - Instead of using pip editable install, use Poetry
   - Install poetry in the venv: `pip install poetry`
   - Use `poetry install -E {group}` (if group != "base", otherwise just `poetry install`)
   - Work from within the stack directory
   - Remove `--extra-index-url` flag (it's in pyproject.toml already via tool.poetry.source)

### Phase 2: Simplify test_imports.py

**Changes needed:**

1. **Simplify TestImports.test_all_imports() (line 11-63)**
   - Remove the version check (`assert X.__version__`)
   - Just test successful import without exit code checks
   - Simplify to: try import, catch ImportError, collect failures
   - More like what a real user would do

2. **Remove or Fix TestFrameworkVersions (line 91-128)**
   - Either make it properly conditional (only test installed frameworks)
   - Or replace with a simpler test that just validates the actual dependency groups

3. **Fix TestPyTorchCUDA (line 66-88)**
   - Change `assert` to conditional skip if CUDA unavailable
   - Or remove this test entirely since CUDA isn't critical to the installation

### Phase 3: Validate Changes

**Test the new test flow:**
- Run on pytorch-cu121 with different group combinations
- Verify poetry install is actually being used
- Confirm tests pass with the poetry.lock we created

---

## Summary of Problems

| Issue | Severity | Type | Impact |
|-------|----------|------|--------|
| Reading wrong pyproject format | CRITICAL | Data | Tests will fail to find groups |
| Using pip instead of poetry | CRITICAL | Testing | Not validating actual user flow |
| flash-attn hardcoded but removed | HIGH | Data | Import test will fail |
| Too strict import testing (__version__) | MEDIUM | Testing | False negatives for valid imports |
| Hardcoded framework tests | MEDIUM | Testing | Brittle and confusing failures |
| CUDA assertions | MEDIUM | Testing | False negatives on non-GPU systems |

## Key Insight

**The tests are trying to simulate installation but don't actually use Poetry.** This is backwards - they should use Poetry directly since that's what users will use. Everything follows from this one fundamental issue.
