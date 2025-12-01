"""Root pytest configuration for ML Frameworks.

Tests each stack's optional dependency groups independently in isolated environments.
"""
import os
import subprocess
import sys
from pathlib import Path

try:
    import tomllib
except ImportError:
    import tomli as tomllib

import pytest


def get_stack_directories() -> list[Path]:
    """
    Discover all stack directories (subdirectories of stacks/ with pyproject.toml).

    Returns:
        List of paths to stack directories
    """
    stacks_dir = Path(__file__).parent.parent / "stacks"
    stacks = []

    if stacks_dir.exists():
        for item in stacks_dir.iterdir():
            if item.is_dir():
                pyproject = item / "pyproject.toml"
                if pyproject.exists():
                    stacks.append(item)

    return sorted(stacks)


def get_groups_for_stack(stack_path: Path) -> list[str]:
    """
    Get all optional dependency groups for a stack.

    Returns:
        List of group names (["base"] + all optional groups)
    """
    pyproject_path = stack_path / "pyproject.toml"
    with open(pyproject_path, "rb") as f:
        pyproject = tomllib.load(f)

    # Support both Poetry format (tool.poetry.extras) and setuptools format
    if "tool" in pyproject and "poetry" in pyproject["tool"]:
        # Poetry format: tool.poetry.extras
        optional_deps = pyproject["tool"]["poetry"].get("extras", {})
    else:
        # Setuptools format: project.optional-dependencies
        optional_deps = pyproject.get("project", {}).get("optional-dependencies", {})

    # Build list of groups, avoiding duplicates (in case "base" is in extras)
    groups = set(optional_deps.keys())
    groups.add("base")
    return sorted(groups)


# Generate parametrized list of (stack, group) combinations
def pytest_generate_tests(metafunc):
    """Parametrize stack_path and group fixtures."""
    if "stack_path" in metafunc.fixturenames:
        stacks = get_stack_directories()

        # If both stack_path and group are needed, parametrize both
        if "group" in metafunc.fixturenames:
            params = []
            ids = []
            for stack in stacks:
                groups = get_groups_for_stack(stack)
                for group in groups:
                    params.append((stack, group))
                    ids.append(f"{stack.name}-{group}")
            metafunc.parametrize("stack_path,group", params, ids=ids)
        else:
            # Only stack_path
            metafunc.parametrize("stack_path", stacks, ids=lambda p: p.name)


@pytest.fixture(scope="function")
def pyproject_path(stack_path: Path) -> Path:
    """Return path to pyproject.toml for the current stack."""
    return stack_path / "pyproject.toml"


@pytest.fixture(scope="function")
def dependencies(pyproject_path: Path, group: str) -> list[str]:
    """
    Read dependencies for a group from a stack's pyproject.toml.

    Returns:
        List of package names that should be installed in this group
    """
    with open(pyproject_path, "rb") as f:
        pyproject = tomllib.load(f)

    # Detect format (Poetry vs setuptools)
    if "tool" in pyproject and "poetry" in pyproject["tool"]:
        # Poetry format: tool.poetry.dependencies are all packages (base and optional)
        # tool.poetry.extras define which optional packages belong to each group
        poetry_config = pyproject["tool"]["poetry"]
        all_deps = poetry_config.get("dependencies", {})
        extras = poetry_config.get("extras", {})

        if group == "base":
            # Base group: only non-optional dependencies
            package_names = []
            for name, spec in all_deps.items():
                if name == "python":
                    continue
                # spec can be a string (non-optional) or dict with 'optional': true
                is_optional = isinstance(spec, dict) and spec.get("optional", False)
                if not is_optional:
                    package_names.append(name)
        else:
            # Other groups: packages listed in extras[group]
            package_names = extras.get(group, [])
    else:
        # Setuptools format
        base_deps = pyproject.get("project", {}).get("dependencies", [])

        if group == "base":
            deps = base_deps
        else:
            optional_deps = pyproject.get("project", {}).get("optional-dependencies", {})
            deps = base_deps + optional_deps.get(group, [])

        # Parse package names from version specs
        package_names = []
        for spec in deps:
            # Strip version specifiers (e.g., "torch>=2.0.0" -> "torch")
            package_name = spec.split(">")[0].split("<")[0].split("=")[0].split("!")[0].strip()
            if package_name != "python":
                package_names.append(package_name)

    return package_names


@pytest.fixture(scope="function")
def test_env(stack_path: Path, group: str, tmp_path_factory) -> Path:
    """
    Build a fresh virtual environment for a stack group using Poetry.

    This simulates how a real user would install: using 'poetry install -E group'.
    The CUDA 12.1 PyTorch index is configured in pyproject.toml via [tool.poetry.source].

    Returns:
        Path to the virtual environment
    """
    env_path = tmp_path_factory.mktemp("venv_base") / "venv"

    print(f"\n📦 Building environment for '{stack_path.name}[{group}]'...")

    # Create virtual environment
    result = subprocess.run(
        [sys.executable, "-m", "venv", str(env_path)],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(f"Failed to create venv: {result.stderr}")

    print(f"✓ Virtual environment created")

    # Determine Python executable
    if sys.platform == "win32":
        python_exe = env_path / "Scripts" / "python.exe"
    else:
        python_exe = env_path / "bin" / "python"

    # Upgrade pip first (needed for Poetry to work properly)
    result = subprocess.run(
        [str(python_exe), "-m", "pip", "install", "--upgrade", "pip"],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(f"Failed to upgrade pip: {result.stderr}")

    print(f"✓ Pip upgraded")

    # Install Poetry in the venv
    result = subprocess.run(
        [str(python_exe), "-m", "pip", "install", "poetry"],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(f"Failed to install poetry: {result.stderr}")

    print(f"✓ Poetry installed")

    # Determine Poetry executable
    if sys.platform == "win32":
        poetry_exe = env_path / "Scripts" / "poetry.exe"
    else:
        poetry_exe = env_path / "bin" / "poetry"

    # Use Poetry to install the stack with the specified group
    print(f"📥 Installing {group} group (this may take a few minutes)...")

    if group == "base":
        # Base group: just install without extras
        cmd = [str(poetry_exe), "install", "--no-root"]
    else:
        # Install with the specified extra
        cmd = [str(poetry_exe), "install", "-E", group, "--no-root"]

    # Set VIRTUAL_ENV so Poetry installs to the correct venv
    env = os.environ.copy()
    env["VIRTUAL_ENV"] = str(env_path)
    env.pop("PYTHONHOME", None)  # Remove if it exists, can interfere

    result = subprocess.run(
        cmd,
        cwd=str(stack_path),
        capture_output=True,
        text=True,
        env=env,
    )

    if result.returncode != 0:
        print(f"Installation stderr: {result.stderr}")
        raise RuntimeError(
            f"Failed to install {stack_path.name}[{group}]: {result.stderr}"
        )

    print(f"✓ {group} group installed successfully\n")

    return env_path


@pytest.fixture(scope="function")
def python_exe(test_env: Path) -> Path:
    """Return path to Python executable in test environment."""
    if sys.platform == "win32":
        exe = test_env / "Scripts" / "python.exe"
    else:
        exe = test_env / "bin" / "python"

    if not exe.exists():
        raise RuntimeError(f"Python executable not found at {exe}")

    return exe
