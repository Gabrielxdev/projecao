from __future__ import annotations

"""Utility to plot projection metrics by week.

This script loads a dataset with columns ``FILIAL``, ``SKU``, ``Semana``,
``Venda``, ``Alvo``, ``Reposicao`` and ``Estoque``—the same structure
produced by the ``projecao.ipynb`` notebook. It aggregates the values for
cada semana and creates four line charts: projected sales, target,
replenishment and stock. The figure is saved to a PNG file.

Usage
-----
```
python plot_projection.py dados.csv --output grafico.png
```
The input can be in CSV or Excel format. The output defaults to
``outputs/projecoes.png``.
"""

from pathlib import Path
import argparse
import pandas as pd
import matplotlib.pyplot as plt


METRICS = ["Venda", "Alvo", "Reposicao", "Estoque"]
TITLES = ["Venda proj", "Alvo proj", "Reposição proj", "Estoque proj"]


def load_dataset(path: Path) -> pd.DataFrame:
    """Load dataset in CSV or Excel format.

    Parameters
    ----------
    path: Path
        Path to the input file. ``.csv`` and ``.xlsx`` are supported.
    """
    if path.suffix.lower() == ".csv":
        return pd.read_csv(path)
    return pd.read_excel(path)


def plot_projections(df: pd.DataFrame, output: Path) -> None:
    """Create projection charts and save to ``output``.

    The function groups the input DataFrame by ``Semana`` and sums the
    metrics. Each metric is drawn as a line chart in a 2x2 grid.
    """
    weekly = (
        df.groupby("Semana")[METRICS]
        .sum()
        .sort_index()
    )

    fig, axes = plt.subplots(2, 2, figsize=(12, 8), sharex=True)
    for ax, metric, title in zip(axes.flat, METRICS, TITLES):
        ax.plot(weekly.index, weekly[metric], marker="o")
        ax.set_title(title)
        ax.set_xlabel("Semana")
        ax.set_ylabel("Quantidade")

    fig.tight_layout()
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output)


def main() -> None:
    parser = argparse.ArgumentParser(description="Plota projeções semanais")
    parser.add_argument(
        "input_file",
        type=Path,
        help="Arquivo CSV ou XLSX contendo as colunas FILIAL, SKU, Semana, Venda, Alvo, Reposicao e Estoque",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("outputs/projecoes.png"),
        help="Arquivo PNG de saída (default: outputs/projecoes.png)",
    )
    args = parser.parse_args()

    df = load_dataset(args.input_file)
    plot_projections(df, args.output)
    print(f"Gráfico salvo em: {args.output.resolve()}")


if __name__ == "__main__":
    main()
