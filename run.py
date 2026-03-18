import os
import sys
import subprocess
from pathlib import Path

root_dir = Path(__file__).resolve().parent
sys.path.append(str(root_dir))


def run_pipeline():
    result = subprocess.run([
        sys.executable, "-m", "data_analysis.src.pipeline"
    ])

    if result.returncode == 0:
        print("Dados processados.")
    else:
        print("Erro ao processar os dados.")


def run_app():
    print("Iniciando Interface Streamlit...")

    env = os.environ.copy()
    env["PYTHONPATH"] = str(root_dir)

    cmd = [
        sys.executable, "-m", "streamlit", "run",
        str(root_dir / "data_analysis" / "interface" / "main.py"),
        "--theme.base", "dark"  # Opcional: força o tema escuro que você está usando
    ]

    try:
        subprocess.run(cmd, env=env)
    except KeyboardInterrupt:
        print("Dashboard encerrado.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "pipeline":
        run_pipeline()
    else:
        run_app()