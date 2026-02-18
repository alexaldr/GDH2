import sys
from pathlib import Path

# Permite rodar pytest sem instalação (útil em CI simples e para onboarding).
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
