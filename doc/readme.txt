- build html:
make html

- extensions: add to conf.py
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.imgmath',
    'sphinx.ext.autosummary',
]

- autosummary: generate files.
  * Add (at the end) conf.py: autosummary_generate = True
  * delete file beginning with TBS in TBS directory

- make coverage: see undocumented methods.