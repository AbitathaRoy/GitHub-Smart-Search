# get_requirements.py
# Walk through the project directory and automatically find and fill the required installations in the .txt

import os
import ast
import sys
import pkg_resources
import sysconfig

# Define your root project directory
PROJECT_DIR = "./"

# Get built-in Python modules (to exclude them)
def get_standard_libs():
    """Retrieve standard libraries manually for Python versions below 3.10"""
    try:
        std_lib_path = sysconfig.get_path("stdlib")
        return {name for name in os.listdir(std_lib_path) if os.path.isdir(os.path.join(std_lib_path, name))}
    except Exception:
        print("⚠️ Could not determine standard library path, falling back to predefined built-ins.")
        return {"sys", "os", "json", "time", "re", "math", "random"}  # Common built-in modules

# Extract import statements from Python files
def extract_imports(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=file_path)

    imports = {alias.name.split(".")[0] for node in ast.walk(tree) if isinstance(node, ast.Import) for alias in node.names}
    imports |= {node.module.split(".")[0] for node in ast.walk(tree) if isinstance(node, ast.ImportFrom) and node.module}

    return imports

# Scan files recursively using os.walk()
def find_requirements(project_dir):
    all_imports = set()
    standard_libs = get_standard_libs()

    for root, _, files in os.walk(project_dir):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                all_imports |= extract_imports(file_path)

    # Remove standard libraries
    third_party_libs = sorted(lib for lib in all_imports if lib and lib not in standard_libs)

    # Match with installed packages to get correct versions
    installed_packages = {pkg.key: pkg.version for pkg in pkg_resources.working_set}
    requirements = [f"{lib}=={installed_packages.get(lib, '')}" for lib in third_party_libs if
                    lib in installed_packages]

    return requirements

# Generate requirements.txt
def generate_requirements_txt(project_dir):
    requirements = find_requirements(project_dir)
    with open("requirements.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(requirements) + "\n")

    print("✅ requirements.txt generated successfully!")

# Run the script
generate_requirements_txt(PROJECT_DIR)
