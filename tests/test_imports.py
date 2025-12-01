"""Test that all packages in each stack group can be imported in fresh environments."""
import subprocess
from pathlib import Path

import pytest


class TestImports:
    """Test imports of all packages in a stack group."""

    def test_all_imports(
        self, python_exe: Path, dependencies: list[str], stack_path: Path, group: str
    ):
        """
        Test that all packages can be imported in the test environment.

        This test runs in the isolated environment created by the test_env fixture.
        It iterates through all dependencies for the group and attempts to
        import each one, collecting failures and reporting them at the end.

        Args:
            python_exe: Path to Python executable in test environment
            dependencies: List of package names that should be installed
            stack_path: Path to the stack being tested
            group: The dependency group being tested
        """
        failed_imports = []

        # Map package names to their actual import statements (case-insensitive)
        package_to_import = {
            "pyyaml": "import yaml",
            "python-dotenv": "from dotenv import load_dotenv",
            "pillow": "from PIL import Image",
            "opencv-python": "import cv2",
            "opencv-contrib-python": "import cv2",
            "scikit-learn": "import sklearn",
            "scikit-image": "import skimage",
            "pytorch-lightning": "import pytorch_lightning",
            "rouge-score": "from rouge_score import rouge_scorer",
        }

        for package_name in dependencies:
            # Get import statement for this package
            # Use lowercase for lookup since package names are case-insensitive in most registries
            lookup_name = package_name.lower()
            if lookup_name in package_to_import:
                import_stmt = package_to_import[lookup_name]
            else:
                # Default: convert hyphens to underscores
                import_name = package_name.replace("-", "_")
                import_stmt = f"import {import_name}"

            try:
                result = subprocess.run(
                    [str(python_exe), "-c", import_stmt],
                    capture_output=True,
                    text=True,
                    timeout=30,
                )

                if result.returncode != 0:
                    failed_imports.append(
                        {
                            "package": package_name,
                            "error": result.stderr.strip(),
                        }
                    )
            except subprocess.TimeoutExpired:
                failed_imports.append(
                    {
                        "package": package_name,
                        "error": "Import timeout (>30s)",
                    }
                )

        # Report results
        if failed_imports:
            error_msg = f"Failed to import packages in '{stack_path.name}[{group}]':\n\n"
            for failure in failed_imports:
                error_msg += f"  ❌ {failure['package']}\n"
                if failure["error"]:
                    error_msg += f"     {failure['error']}\n"
            pytest.fail(error_msg)

        # If we got here, all imports succeeded
        assert len(dependencies) > 0, f"No dependencies found to test in '{stack_path.name}[{group}]'"


class TestPyTorchCUDA:
    """Test PyTorch CUDA availability (if torch is in the stack)."""

    def test_torch_cuda(self, python_exe: Path, dependencies: list[str]):
        """Test that torch is installed and can use CUDA if available."""
        if "torch" not in dependencies:
            pytest.skip("torch not in this stack")

        code = """
import torch
# Just test that CUDA functions work, don't require it to be available
is_available = torch.cuda.is_available()
print(f"CUDA available: {is_available}")
if is_available:
    print(f"Device: {torch.cuda.get_device_name(0)}")
"""
        result = subprocess.run(
            [str(python_exe), "-c", code],
            capture_output=True,
            text=True,
        )

        # Test passes if torch can be imported and CUDA functions don't error
        # (whether CUDA is actually available depends on system hardware)
        assert result.returncode == 0, f"torch CUDA test failed: {result.stderr}"


class TestFrameworkVersions:
    """Test that major frameworks are present with reasonable versions."""

    def test_framework_versions(self, python_exe: Path, dependencies: list[str]):
        """
        Test that major frameworks installed have accessible versions.

        Only tests frameworks that are actually in the installed dependencies.
        """
        # Map package names to their Python module names and how to get version
        frameworks = {
            "torch": ("torch", "import torch; print(torch.__version__)"),
            "transformers": ("transformers", "import transformers; print(transformers.__version__)"),
            "pytorch-lightning": ("pytorch_lightning", "import pytorch_lightning; print(pytorch_lightning.__version__)"),
            "ultralytics": ("ultralytics", "import ultralytics; print(ultralytics.__version__)"),
            "mmdet": ("mmdet", "import mmdet; print(mmdet.__version__)"),
        }

        tested_any = False
        for package_name, (module_name, version_code) in frameworks.items():
            if package_name not in dependencies:
                continue

            tested_any = True
            result = subprocess.run(
                [str(python_exe), "-c", version_code],
                capture_output=True,
                text=True,
                timeout=10,
            )

            assert (
                result.returncode == 0
            ), f"Failed to get version for {package_name}: {result.stderr}"
            version = result.stdout.strip()
            assert version, f"Could not get version for {package_name}"

        # It's OK if none of these frameworks are in the dependencies
        if not tested_any:
            pytest.skip("No major frameworks in this group's dependencies")
