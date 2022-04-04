import PyInstaller.__main__

PyInstaller.__main__.run([
    'main.py',
    '--onefile',
    '--name=FastWeighTicketIntegrator',
    '--icon=icon.ico',
])
