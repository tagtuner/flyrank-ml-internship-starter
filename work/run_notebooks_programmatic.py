import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import os

def run_notebook(nb_path):
    print(f"Executing {nb_path}...")
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
    
    # Execute relative to the project root directory
    ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
    ep.preprocess(nb, {'metadata': {'path': os.getcwd()}})
    
    with open(nb_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
    print(f"Saved executed {nb_path}")

run_notebook("notebooks/01_first_look_and_discovery.ipynb")
run_notebook("notebooks/02_your_first_readable_model.ipynb")
print("Both notebooks executed and saved successfully!")
