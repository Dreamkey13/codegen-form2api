#!/usr/bin/env python3
import os
import sys
import pytest
import logging
from src.config.logging import setup_logging

def main():
    """Run the test suite."""
    # Set up logging
    setup_logging(log_level=logging.INFO)
    
    # Get the directory containing this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Change to the script directory
    os.chdir(script_dir)
    
    # Run pytest with arguments
    args = [
        "--verbose",
        "--tb=short",
        "--cov=src",
        "--cov-report=term-missing",
        "--cov-report=html",
        "tests"
    ]
    
    # Add any command line arguments
    args.extend(sys.argv[1:])
    
    # Run the tests
    return pytest.main(args)

if __name__ == "__main__":
    sys.exit(main()) 