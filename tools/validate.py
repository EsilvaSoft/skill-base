"""Validate the skills catalog."""

import argparse
import sys

from catalog import validate


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    try:
        skills = validate()
    except (ValueError, OSError) as error:
        parser.exit(1, f"Erro: {error}\n")
    print(f"VERIFICADO: {len(skills)} skills válidas")


if __name__ == "__main__":
    sys.exit(main())
