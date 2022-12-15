from distutils.core import setup
setup(name='dap',
      version='0.1',
      description='Manage bioinformatics projects',
      packages=['dap'],
      entry_points={
        'console_scripts': [
            'dap=dap:run_dap'
        ]
      },
      include_package_data=True,
      package_data={'dap': [
        'model/_footer.mk',
        'model/_header.mk',
        'model/.envrc',
        'model/.gitignore',
        'model/makefile',
        'model/Snakefile',
        'model/dapdefault.yml'
        ]}
      )