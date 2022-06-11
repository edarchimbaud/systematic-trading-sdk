# Systematic Trading Package

This is a simple systematic trading package.


## Install

```bash
pip install systematic-trading
```

## Package and distribute

Generating distribution archives

```bash
python3 -m pip install --upgrade build twine

python3 -m build
python3 -m twine upload --repository testpypi dist/*
python3 -m twine upload dist/*
```