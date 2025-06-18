# get_requirements_2.py
# Walk through the project directory and automatically find and fill the required installations in the .txt
# For Python versions 3.10+

import os
import ast
import sys
import json
import importlib.util
import sysconfig
import pkg_resources
from pathlib import Path
from typing import Set

# Project directory
PROJECT_DIR = Path(".")  # Current directory

# Get standard libraries (Python ≥ 3.10 compatible)
def get_standard_libs() -> Set[str]:
    """Try to get standard libraries using sysconfig, fallback to common built-ins."""
    try:
        stdlib_path = Path(sysconfig.get_path("stdlib"))
        return {
            entry.name
            for entry in stdlib_path.iterdir()
            if entry.is_dir() or entry.name.endswith(".py")
        }
    except Exception:
        return {
            "sys", "os", "math", "json", "re", "time", "random", "typing", "pathlib",
            "ast", "itertools", "functools", "collections", "dataclasses"
        }

# Extract all imports from a .py file
def extract_imports_from_file(file_path: Path) -> Set[str]:
    imports = set()
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            node = ast.parse(f.read(), filename=str(file_path))
        for n in ast.walk(node):
            if isinstance(n, ast.Import):
                for alias in n.names:
                    imports.add(alias.name.split('.')[0])
            elif isinstance(n, ast.ImportFrom) and n.module:
                imports.add(n.module.split('.')[0])
    except (SyntaxError, UnicodeDecodeError):
        pass  # skip unreadable files
    return imports

# Walk through project and collect all imports
def find_all_imports(project_dir: Path) -> Set[str]:
    all_imports = set()
    for py_file in project_dir.rglob("*.py"):
        all_imports |= extract_imports_from_file(py_file)
    return all_imports

# Map imports to PyPI-installed packages
def map_to_installed_packages(imports: Set[str]) -> Set[str]:
    std_libs = get_standard_libs()
    installed = {pkg.key: pkg.version for pkg in pkg_resources.working_set}

    requirements = []
    for imp in sorted(imports):
        imp_lower = imp.lower()
        if imp in std_libs or imp_lower in std_libs:
            continue  # Skip standard libs
        if imp_lower in installed:
            requirements.append(f"{imp_lower}=={installed[imp_lower]}")
        else:
            # Best guess fallback (if not matched by name)
            for key in installed:
                if key.replace("-", "_") == imp_lower:
                    requirements.append(f"{key}=={installed[key]}")
                    break

    return requirements

# Write to requirements.txt
def generate_requirements_txt(project_dir: Path):
    all_imports = find_all_imports(project_dir)
    requirements = map_to_installed_packages(all_imports)

    with open("requirements.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(requirements) + "\n")

    print("✅ requirements.txt generated successfully!")
    print("🧾 Contents:")
    for r in requirements:
        print("  -", r)

# Run
if __name__ == "__main__":
    generate_requirements_txt(PROJECT_DIR)
