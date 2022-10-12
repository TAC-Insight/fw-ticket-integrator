import PyInstaller.__main__

PyInstaller.__main__.run([
    'main.py',
    '--clean',
    '--onefile',
    '--name=FastWeighTicketIntegrator',
    '--icon=icon.ico',
    '--log-level=DEBUG'
])
