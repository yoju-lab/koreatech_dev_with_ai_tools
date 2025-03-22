# Development Container for Python and Jupyter

This development container provides a pre-configured environment for Python development and Jupyter notebooks.

## Features

- Python 3.9 with essential scientific packages
- Jupyter Notebook server
- VS Code extensions for Python development
- Auto-formatting and linting

## Getting Started

### Running Python Files in the 'codes' Folder

1. Open a terminal in VS Code (Terminal > New Terminal)
2. Navigate to your Python file: `cd codes/your_subfolder`
3. Run your Python file: `python your_file.py`

### Starting Jupyter Notebook

1. Open a terminal in VS Code
2. Run: `jupyter notebook --allow-root --ip=0.0.0.0`
3. The Jupyter server will start and be accessible at `http://localhost:8888`
4. You can also use the "Jupyter" extension in VS Code to open and run notebooks directly

### Creating a New Notebook

1. In VS Code, click on the Explorer icon
2. Right-click in the explorer panel and select "New File"
3. Name your file with a `.ipynb` extension
4. VS Code will automatically open it as a Jupyter notebook

## Accessing Files

- All files in the workspace are automatically mounted in the container
- The `codes` directory is available at `/workspace/codes`
- Any Python files organized in subfolders can be executed normally
