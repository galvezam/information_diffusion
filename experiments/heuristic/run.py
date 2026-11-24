"""Execute the editable notebook and export a standalone, offline HTML report."""
import os
import argparse
import sys
from pathlib import Path

# Set before numerical packages start; do not overwhelm an eight-core laptop.
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
EXPERIMENT = Path(__file__).resolve().parent
ROOT = EXPERIMENT.parents[1]
sys.path.insert(0, str(ROOT))
os.chdir(ROOT)
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / ".cache" / "matplotlib"))
os.environ.setdefault("IPYTHONDIR", str(ROOT / ".cache" / "ipython"))
os.environ.setdefault("XDG_CACHE_HOME", str(ROOT / ".cache"))

import nbformat
from nbconvert import HTMLExporter
from IPython.core.interactiveshell import InteractiveShell
from IPython.utils.capture import capture_output
import matplotlib
from matplotlib_inline.backend_inline import configure_inline_support


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--export", action="store_true", help="Also save figures, CSVs, and simulation draws to experiments/heuristic/results/")
    args = parser.parse_args()
    os.environ["HIGGS_EXPORT"] = "1" if args.export else "0"
    notebook = nbformat.read(EXPERIMENT / "analysis.ipynb", as_version=4)
    # Execute locally in IPython: no Jupyter server, kernel subprocess, or sockets.
    shell = InteractiveShell.instance()
    matplotlib.use("module://matplotlib_inline.backend_inline")
    configure_inline_support(shell, "inline")
    print("Building experiments/heuristic/heuristic_models.html (one process; first run loads the social network)...", flush=True)
    count = 0
    for cell in notebook.cells:
        if cell.cell_type != "code":
            continue
        count += 1
        with capture_output() as captured:
            execution = shell.run_cell(cell.source, store_history=True)
        error = execution.error_before_exec or execution.error_in_exec
        if error:
            raise RuntimeError(f"Notebook code cell {count} failed") from error
        cell.execution_count = count
        cell.outputs = []
        for stream in ("stdout", "stderr"):
            value = getattr(captured, stream)
            if value:
                cell.outputs.append(nbformat.v4.new_output("stream", name=stream, text=value))
        for output in captured.outputs:
            cell.outputs.append(nbformat.v4.new_output("display_data", data=output.data,
                                                       metadata=output.metadata))
        print(f"  Cell {count} complete", flush=True)
    html, _ = HTMLExporter(template_name="lab", embed_images=True,
                           exclude_input=True).from_notebook_node(notebook)
    report = EXPERIMENT / "heuristic_models.html"
    report.write_text(html)
    print(f"Ready: {report.relative_to(ROOT)}" + (" and experiments/heuristic/results/ exports" if args.export else ""), flush=True)


if __name__ == "__main__":
    main()
