#!/usr/bin/env python
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path="../../.env", override=True)

import warnings

from x_financial_researcher.crew import XFinancialResearcher

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """
    Run the financial researcher crew.
    """
    inputs = {
        'company': 'LPL Financial'
    }
    
    try:
        result = XFinancialResearcher().crew().kickoff(inputs=inputs)
        print(result.raw)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")