"""
Sistema CM - Launcher Principal
Ponto de entrada alternativo do sistema
"""

import sys
from pathlib import Path

# Adicionar diretório src ao path para imports
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from app import main

if __name__ == "__main__":
    main()


