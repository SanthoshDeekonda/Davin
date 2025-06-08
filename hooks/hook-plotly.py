from PyInstaller.utils.hooks import collect_submodules

hiddenimports = (
    collect_submodules('plotly.graph_objs') +
    collect_submodules('plotly.io') +
    collect_submodules('_plotly_utils') +
    collect_submodules('plotly.validators') 
)
