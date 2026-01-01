import os
import nbformat

# Path to the Python folder
python_folder = "Python"

# Initialize a new notebook
combined_notebook = nbformat.v4.new_notebook()

# Iterate through all files in the Python folder
for file_name in sorted(os.listdir(python_folder)):
    if file_name.endswith(".ipynb"):
        file_path = os.path.join(python_folder, file_name)
        with open(file_path, "r", encoding="utf-8") as f:
            notebook = nbformat.read(f, as_version=4)
            combined_notebook.cells.extend(notebook.cells)

# Save the combined notebook
output_path = os.path.join(python_folder, "Combined_Notebook.ipynb")
with open(output_path, "w", encoding="utf-8") as f:
    nbformat.write(combined_notebook, f)

print(f"Combined notebook saved to {output_path}")