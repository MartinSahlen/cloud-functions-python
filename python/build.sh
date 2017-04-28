./venv/bin/pyinstaller test.py -y -n func --clean --onedir --additional-hooks-dir hooks --hidden-import htmlentitydefs --hidden-import HTMLParser --hidden-import Cookie
