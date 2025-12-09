#!/usr/bin/env python3

import asyncio
import os
import sys

from google import genai
from google.genai import types
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from variables import *


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
                
                Use the available tools (like gdb_command) to:
                  - run the program
                  - inspect any crash via backtrace
                  - explain the root cause and likely fix.

                Make sure to check for buffer overflows, format string issues, bypass checks
                deserialized flaws, any code tampering, or command injections
                Do not set breakpoints, if you want to test it with different value,
                go ahead and test it and then give an analyzed output on how it will
                work.
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

            print("\n=== Gemini answer ===\n")
            print(response.text)
            print("\n=====================\n")


if __name__ == "__main__":
    asyncio.run(main())

