"""Validate the catalog and optional release tag."""

import argparse
import sys

from catalog import validate


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tag", help="Tag exata vX.Y.Z a conferir contra VERSION")
    args = parser.parse_args()
    try:
        skills = validate(tag=args.tag)
    except (ValueError, OSError) as error:
        parser.exit(1, f"Erro: {error}\n")
    print(f"VERIFICADO: {len(skills)} skills válidas")


if __name__ == "__main__":
    sys.exit(main())
