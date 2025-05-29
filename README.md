# marimo WebAssembly + GitHub Pages
Exports [marimo](https://marimo.io) notebooks to WebAssembly and deploys them to GitHub Pages.

## 📚 Currently Included

- `rocket_generator.py`: Data analysis and visualization for a linear rocket motor generator

### Example Notebooks

- `apps/charts.py`: Interactive data visualization with Altair
- `notebooks/fibonacci.py`: Interactive Fibonacci sequence calculator
- `notebooks/penguins.py`: Interactive data analysis with Polars and marimo

## Including data or assets

Data or assets for these notebooks are in the `public/` directory.

## 🧪 Local Testing

To test the export process, run `scripts/build.py` from the root directory.

```bash
python scripts/build.py
```

This will export all notebooks in a folder called `_site/` in the root directory. Then to serve the site, run:

```bash
python -m http.server -d _site
```

This will serve the site at `http://localhost:8000`.
