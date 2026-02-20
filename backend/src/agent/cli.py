#!/usr/bin/env python3
"""CLI interface for AI Agent interactive testing.

Provides a simple command-line interface for testing the AI Agent.
"""

import asyncio
import sys
import logging

from .executor import AgentExecutor
from .logging_config import setup_agent_logging

# Setup logging
logger = setup_agent_logging(level=logging.INFO)


async def interactive_mode():
    """Run the agent in interactive CLI mode."""
    executor = AgentExecutor()
    
    print("=" * 60)
    print("AI Agent - Natural Language Task Management")
    print("=" * 60)
    print()
    print("I can help you manage your tasks. Try commands like:")
    print("  - 'Add a task to buy groceries'")
    print("  - 'Show me my tasks'")
    print("  - 'Mark task 1 complete'")
    print("  - 'Delete task 2'")
    print()
    print("Type 'quit' or 'exit' to stop.")
    print()
    
    try:
        while True:
            try:
                # Get user input
                user_input = input("You: ").strip()
                
                # Check for exit commands
                if user_input.lower() in ["quit", "exit", "q"]:
                    print("AI Agent: Goodbye!")
                    break
                
                if not user_input:
                    continue
                
                # Execute the instruction
                print("AI Agent: ", end="", flush=True)
                response = await executor.execute(user_input)
                print(response)
                print()
                
            except KeyboardInterrupt:
                print("\n\nAI Agent: Goodbye!")
                break
            except EOFError:
                print("\nAI Agent: Goodbye!")
                break
                
    finally:
        await executor.close()


async def run_command(instruction: str):
    """Execute a single instruction and return the response.
    
    Args:
        instruction: Natural language instruction
        
    Returns:
        Response string
    """
    executor = AgentExecutor()
    try:
        return await executor.execute(instruction)
    finally:
        await executor.close()


def main():
    """Main entry point for the CLI."""
    if len(sys.argv) > 1:
        # Single command mode
        instruction = " ".join(sys.argv[1:])
        response = asyncio.run(run_command(instruction))
        print(response)
    else:
        # Interactive mode
        asyncio.run(interactive_mode())


if __name__ == "__main__":
    main()
