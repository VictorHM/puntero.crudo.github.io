#!/usr/bin/env python3
"""Entry point for blog generation."""
import sys
from src.generator import generate_all


def main():
    try:
        generate_all()
        sys.exit(0)
    except Exception as e:
        print(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
