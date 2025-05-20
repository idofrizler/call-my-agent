"""Utility for loading the initial book idea."""

import os

def load_seed() -> str:
    """Load the initial book idea from file or prompt for input.
    
    Returns:
        The book idea as a string
    """
    path = "book_seed.txt"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
    
    return input("📘 Enter your book idea:\n> ").strip()
