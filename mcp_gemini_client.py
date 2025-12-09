#!/usr/bin/env python3

import asyncio
import os
import sys

from google import genai
from google.genai import types
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from variables import *

from rich.console import Console
from rich.markdown import Markdown


async def main() -> None:
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

    binary_path = sys.argv[1] if len(sys.argv) > 1 else None

    if not os.path.isfile(binary_path):
        print(f"[ERROR]: The binary path {binary_path} does not exist")
        sys.exit(1)


    server_params = StdioServerParameters(
        command="python3",
        args=["mcp_server.py"],
        env=os.environ.copy(),
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as mcp_session:
            await mcp_session.initialize()


            start_result = await mcp_session.call_tool(
                name="start_gdb",
                arguments={"binary": binary_path},
            )

            user_prompt = f"""
                I am debugging the binary at: {binary_path}.
                
                A GDB session is already running and attached to this binary via MCP tools.
                
                Use the available tools (like gdb_command, run_program, backtrace, step_in, continue) to:
                  - run the program
                  - inspect any crash via backtrace
                  - explain the root cause and likely fix.

                
                1.  Initial Run: Call the `gdb_command` tool to run the
                     attached binary. *Example: `gdb_command("run")`*

                2.  Context Gathering: If the program crashes, immediately call
                    the tool to get the necessary context. *Example: `gdb_command("bt full")`*

                3.  Diagnosis: Analyze the execution output (backtrace, register
                    state, error messages) to determine the exact vulnerability type.
                4.  Security Analysis: Prioritize checking for and diagnosing,
                    Buffer Overflows (Stack/Heap), Format String Issues, Command
                    Injection, Deserialization Flaws

                5.  Hypothesis Testing: If needed, execute one or more additional
                    additional `gdb_command` calls (e.g., `p variable_name`)
                    to test a hypothesis or inspect a different input value, but
                    do not set persistent breakpoints.

               Make sure to write the output with an Execution Summary, a Root-Cause Analysis,
               the Vulnerability Type, and a Proposed Fix
            """
            response = await client.aio.models.generate_content(
                model="gemini-2.5-flash",
                contents=user_prompt,
                config=types.GenerateContentConfig(
                    tools=[mcp_session],
                    automatic_function_calling=types.AutomaticFunctionCallingConfig(
                        maximum_remote_calls=4,
                    ),
                ),
            )

            console = Console()
            md = Markdown(response.text)
            print("\n=== Gemini answer ===\n")
            console.print(md)
            print("\n=====================\n")


if __name__ == "__main__":
    asyncio.run(main())

