"""
PyInstaller hook for NudeNet package
Ensures the ONNX model file is included in the build
"""
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Collect all data files from nudenet (including 320n.onnx model)
datas = collect_data_files('nudenet', include_py_files=False)

# Collect all submodules
hiddenimports = collect_submodules('nudenet')

# Ensure ONNX runtime is included
hiddenimports += [
    'onnxruntime',
    'onnxruntime.capi',
    'onnxruntime.capi._pybind_state',
]
