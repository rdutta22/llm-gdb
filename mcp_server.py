#!/usr/bin/env python3

import subprocess
import threading
import queue
import re
from typing import Optional, List, Dict, Any

from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
        "gdb-mcp",
        json_response=True,
        stateless_http=True,
        )


class GdbSession:
    def __init__(self, binary: str):
        self.proc = subprocess.Popen(
            ["gdb", "-q", "--interpreter=mi2", binary],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )
        self._q: "queue.Queue[str]" = queue.Queue()
        self._reader = threading.Thread(target=self._read_stdout, daemon=True)
        self._reader.start()

    def _read_stdout(self) -> None:
        assert self.proc.stdout is not None
        for line in self.proc.stdout:
            self._q.put(line)

    def _drain(self, timeout: float = 0.1) -> str:
        lines = []
        try:
            while True:
                lines.append(self._q.get(timeout=timeout))
        except queue.Empty:
            pass
        return "".join(lines)

    def run(self) -> str:
        return self.command("-exec-run")

    def run_with_args(self, args: List[str]) -> str:
        arg_string = " ".join(args)
        self.command(f'-gdb-set args {arg_string!r}')

        return self.command('-exec-run')

    def command(self, mi_command: str) -> str:
        if self.proc.poll() is not None:
            return "[GDB] Process already exited."

        assert self.proc.stdin is not None
        self.proc.stdin.write(mi_command + "\n")
        self.proc.stdin.flush()
        return self._drain()

    def step_in(self) -> str:
        return self.command("-exec-step")

    def backtrace(self, max_frames: int = 32) -> str:
        return self.command(f"-stack-list-frames 0 {max_frames}")

    def cont(self) -> str:
        return self.command("-exec-continue")


gdb_session: Optional[GdbSession] = None

"""
Start a GDB session on the given binary.
"""
@mcp.tool()
def start_gdb(binary: str) -> str:
    global gdb_session
    gdb_session = GdbSession(binary)
    return f"Started GDB session for {binary}"


"""
Run an active GDB session with/without arguments.
"""
@mcp.tool()
def run_program(args: List[str] = None) -> Dict[str, Any]:
    if gdb_session is None:
        return {"error": "No GDB session. Call start_gdb(binary) first."}

    if args:
        raw = gdb_session.run_with_args(args)
    else:
        raw = gdb_session.run()

    return {"raw_mi": raw}

"""
Send a raw GDB command to the session and return its output.
"""
@mcp.tool()
def gdb_command(command: str) -> str:
    if gdb_session is None:
        return "No GDB session. Call start_gdb(binary) first."
    output = gdb_session.command(command)
    # You can later parse MI and return structured JSON instead of a string.
    return output


"""
Return a backtrace using -stack-list-frames, with a parsed frames list.
"""
@mcp.tool()
def get_backtrace(max_frames: int = 32) -> Dict[str, Any]:
    if gdb_session is None:
        return {"error": "No GDB session. Call start_gdb(binary) first."}
    raw = gdb_session.backtrace(max_frames=max_frames)
    frames = _parse_frames_from_mi(raw)
    return {"raw_mi": raw, "frames": frames}

"""
Single-step into (-exec-step).
"""
@mcp.tool()
def step_into() -> Dict[str, Any]:
    if gdb_session is None:
        return {"error": "No GDB session. Call start_gdb(binary) first."}
    raw = gdb_session.step_in()
    return {"raw_mi": raw}

"""
Continue processing till next breakpoint (-exec-continue_execution).
"""
@mcp.tool()
def continue_execution() -> Dict[str, Any]:
    if gdb_session is None:
        return {"error": "No GDB session. Call start_gdb(binary) first."}
    raw = gdb_session.cont()
    return {"raw_mi": raw}

if __name__ == "__main__":
    # For testing curl command response
    # mcp.run("streamable-http")
    mcp.run()

