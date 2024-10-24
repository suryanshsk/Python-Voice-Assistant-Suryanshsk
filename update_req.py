import os
import ast
import subprocess
import pkg_resources

# Dictionary to map common import names to pip package names (expandable)
PACKAGE_MAPPING = {
    'PIL': 'pillow',
    'cv2': 'opencv-python',
    'sklearn': 'scikit-learn',
    'dateutil': 'python-dateutil',
    'yaml': 'pyyaml',
    # Add more known mappings here
}

# Function to extract imports from a Python file
def extract_imports(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        tree = ast.parse(file.read(), filename=file_path)
    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name.split('.')[0])
        elif isinstance(node, ast.ImportFrom):
            imports.add(node.module.split('.')[0])
    return imports

# Function to scan all Python files in a directory
def scan_python_files(directory):
    imported_modules = set()
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                imported_modules.update(extract_imports(file_path))
    return imported_modules

# Read existing requirements.txt
def read_requirements(file_path):
    if not os.path.exists(file_path):
        return set()
    with open(file_path, 'r', encoding='utf-8') as file:
        return set(line.strip() for line in file if line.strip())

# Function to check if a module is available in pip
def is_module_available(module_name):
    try:
        subprocess.check_output([f"pip show {module_name}"], shell=True, stderr=subprocess.STDOUT)
        return True
    except subprocess.CalledProcessError:
        return False

# Function to map import names to pip package names
def get_pip_package_name(module_name):
    # Check if the module has a mapped pip package name
    if module_name in PACKAGE_MAPPING:
        return PACKAGE_MAPPING[module_name]
    
    # Fallback: Try to use installed distributions to map to pip names
    for dist in pkg_resources.working_set:
        try:
            mod_list = dist.get_metadata('top_level.txt').splitlines()
            if module_name in mod_list:
                return dist.project_name
        except FileNotFoundError:
            continue
    
    # If no mapping found, assume module_name is the correct pip package
    return module_name

# Update requirements.txt with missing modules that are available in pip
def update_requirements_txt(directory, requirements_file):
    existing_requirements = read_requirements(requirements_file)
    imported_modules = scan_python_files(directory)
    
    missing_modules = imported_modules - existing_requirements
    available_modules = set()

    for module in missing_modules:
        pip_name = get_pip_package_name(module)
        if is_module_available(pip_name):
            available_modules.add(pip_name)

    if available_modules:
        with open(requirements_file, 'a', encoding='utf-8') as file:
            for module in available_modules:
                file.write(module + '\n')
        print(f"Added missing and available modules: {available_modules}")
    else:
        print("No missing or available modules found.")

# Example usage:
project_directory = '.'  # current directory
requirements_file = 'requirements.txt'
update_requirements_txt(project_directory, requirements_file)
