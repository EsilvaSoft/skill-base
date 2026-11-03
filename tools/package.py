"""Build versioned Codex bundles and SHA-256 checksums."""

import argparse
from pathlib import Path

from catalog import build


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Diretório de saída (padrão: dist)")
    args = parser.parse_args()
    try:
        paths = build(output=args.output)
    except (ValueError, OSError) as error:
        parser.exit(1, f"Erro: {error}\n")
    for path in paths:
        print(path)


if __name__ == "__main__":
    main()
