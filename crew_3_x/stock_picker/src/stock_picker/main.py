#!/usr/bin/env python
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path="../../.env", override=True)

import sys
import warnings

from datetime import datetime
from stock_picker.crew import StockPicker

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """
    Run the crew.
    """
    inputs = {
        'sector': 'Technology'
    }
    
    try:
        result = StockPicker().crew().kickoff(inputs=inputs)
        print("\n\n======THE FINAL RESULTS======\n\n")
        print(result.raw)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")
    
if __name__ == "__main__":
    run()