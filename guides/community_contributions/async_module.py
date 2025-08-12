#!/usr/bin/env python3
"""
Async Python Module Example
This module demonstrates async/await patterns and can be run independently.
"""

import asyncio

async def do_some_work():
    """Simulate some async work with a delay."""
    print("Starting work")
    await asyncio.sleep(1)
    print("Work complete")

async def do_a_lot_of_work():
    """Run multiple work tasks sequentially."""
    await do_some_work()
    await do_some_work()
    await do_some_work()

async def do_a_lot_of_work_in_parallel():
    """Run multiple work tasks in parallel using asyncio.gather()."""
    await asyncio.gather(do_some_work(), do_some_work(), do_some_work())

def main():
    """Main function to run the async examples."""
    print("Running async examples...")
    
    # Run the parallel version
    print("\n--- Running work in parallel ---")
    asyncio.run(do_a_lot_of_work_in_parallel())
    
    # You can also run the sequential version for comparison
    print("\n--- Running work sequentially ---")
    asyncio.run(do_a_lot_of_work())

if __name__ == "__main__":
    main()
