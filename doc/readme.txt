- build html:
make html

- generate all doc
    * manually :
        * delete file beginning with TBS in TBS directory
        * make clean
        * make html (or any other supported format)
    * ./clean.sh; make html



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