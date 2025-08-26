#!/usr/bin/env python
import os
import sys
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from financial_researcher.crew import FinancialResearcher

def debug_config():
    """Debug the CrewAI configuration loading"""
    try:
        # Create the crew instance
        crew_instance = FinancialResearcher()
        
        # Check what's in the configs
        print("=== DEBUG INFO ===")
        print(f"Current working directory: {os.getcwd()}")
        print(f"Config directory: {Path(__file__).parent / 'src' / 'financial_researcher' / 'config'}")
        
        # Try to access the configs directly
        if hasattr(crew_instance, 'agents_config'):
            print(f"Agents config keys: {list(crew_instance.agents_config.keys())}")
            print(f"Analyst config exists: {'analyst' in crew_instance.agents_config}")
        else:
            print("No agents_config attribute found")
            
        if hasattr(crew_instance, 'tasks_config'):
            print(f"Tasks config keys: {list(crew_instance.tasks_config.keys())}")
        else:
            print("No tasks_config attribute found")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_config()
