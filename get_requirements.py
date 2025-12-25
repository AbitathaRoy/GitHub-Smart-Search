# get_requirements.py
<<<<<<< HEAD
# Scans the project directory and generates a requirements.txt with necessary third-party packages.
=======
# Walk through the project directory and automatically find and fill the required installations in the .txt
# For Python versions below 3.10
>>>>>>> 05c2549dc7baa68fb7d4106dc1ef15c032a123bc

import os
import ast
import sys
import sysconfig
from collections import defaultdict

try:
    from importlib.metadata import distributions
except ImportError:
    from importlib.metadata import distributions  # for Python < 3.8 (needs `importlib-metadata` package)

PROJECT_DIR = "./"

# Get standard libraries (Python 3.10+ provides this as a built-in set)
def get_standard_libs():
    if hasattr(sys, "stdlib_module_names"):
        return sys.stdlib_module_names  # Available in Python 3.10+
    else:
        # Fallback for older Python versions
        std_lib_path = sysconfig.get_path("stdlib")
        std_modules = set()
        for root, dirs, files in os.walk(std_lib_path):
            for name in files:
                if name.endswith(".py"):
                    std_modules.add(name[:-3])
            for name in dirs:
                std_modules.add(name)
        return std_modules

# Extract top-level imports from Python files
def extract_imports(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=file_path)

    imports = {
        alias.name.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    imports |= {
        node.module.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module
    }

    return imports

# Traverse directory and find all imports
def find_requirements(project_dir):
    all_imports = set()
    standard_libs = get_standard_libs()

    # Step 1: Extract all imports from .py files
    for root, _, files in os.walk(project_dir):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                all_imports |= extract_imports(file_path)

    third_party_libs = sorted(lib for lib in all_imports if lib and lib not in standard_libs)

    # Step 2: Map top-level modules to package names and versions
    module_to_package = {}
    for dist in distributions():
        try:
            top_level = dist.read_text("top_level.txt")
            if top_level:
                for module in top_level.splitlines():
                    module_to_package[module.strip()] = (dist.metadata["Name"], dist.version)
        except Exception:
            continue

    # Step 3: Build requirements list
    requirements = []
    seen_packages = set()

    for mod in third_party_libs:
        if mod in module_to_package:
            pkg_name, pkg_version = module_to_package[mod]
            if pkg_name not in seen_packages:
                requirements.append(f"{pkg_name}=={pkg_version}")
                seen_packages.add(pkg_name)

    return sorted(requirements)

# Write to requirements.txt
def generate_requirements_txt(project_dir):
    requirements = find_requirements(project_dir)
    with open("requirements.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(requirements) + "\n")

    print("✅ requirements.txt generated successfully!")

# Run the script
if __name__ == "__main__":
    generate_requirements_txt(PROJECT_DIR)
