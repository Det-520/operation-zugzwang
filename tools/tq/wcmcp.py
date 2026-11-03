"""Minimal MCP client for the WordCraft MCP server (`wordcraft-cli mcp`, stdio).

    with WordCraft(read_root, write_root) as wc:
        wc.call("open_document", path="...")
        wc.run("select.all")                      # one WordCraft command
        wc.call("type_text", text="Hello")
"""
import json
import os
import shutil
import subprocess


def wordcraft_cli():
    exe = os.environ.get("WORDCRAFT_CLI") or shutil.which("wordcraft-cli")
    if not exe:
        app = shutil.which("wordcraft")
        cand = os.path.join(os.path.dirname(os.path.realpath(app)), "wordcraft-cli") if app else ""
        exe = cand if cand and os.path.exists(cand) else None
    if not exe:
        raise SystemExit("wordcraft-cli not found. Install WordCraft or set WORDCRAFT_CLI.")
    return exe


class WordCraftError(RuntimeError):
    pass


class WordCraft:
    def __init__(self, read_root, write_root, author="Operation Zugzwang"):
        self.args = [wordcraft_cli(), "mcp", "--author", author,
                     "--automation-read-root", read_root, "--automation-write-root", write_root]
        self.n = 0

    def __enter__(self):
        self.p = subprocess.Popen(self.args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, bufsize=1)
        self._rpc("initialize", {"protocolVersion": "2025-06-18", "capabilities": {},
                                 "clientInfo": {"name": "zugzwang-build", "version": "1"}})
        self._send({"jsonrpc": "2.0", "method": "notifications/initialized"})
        return self

    def __exit__(self, *exc):
        self.p.stdin.close()
        try:
            self.p.wait(timeout=10)
        except subprocess.TimeoutExpired:
            self.p.kill()

    def _send(self, msg):
        self.p.stdin.write(json.dumps(msg) + "\n")
        self.p.stdin.flush()

    def _rpc(self, method, params):
        self.n += 1
        self._send({"jsonrpc": "2.0", "id": self.n, "method": method, "params": params})
        while True:
            line = self.p.stdout.readline()
            if not line:
                raise WordCraftError("WordCraft MCP server exited")
            msg = json.loads(line)
            if msg.get("id") == self.n:
                if "error" in msg:
                    raise WordCraftError(f"{method}: {msg['error']}")
                return msg["result"]

    def call(self, tool, **arguments):
        res = self._rpc("tools/call", {"name": tool, "arguments": arguments})
        text = "".join(c.get("text", "") for c in res.get("content", []) if c.get("type") == "text")
        if res.get("isError"):
            shown = {k: (v[:80] + "…" if isinstance(v, str) and len(v) > 80 else v) for k, v in arguments.items()}
            raise WordCraftError(f"{tool} {shown}: {text[:500]}")
        return text

    def run(self, command, **params):
        return self.call("execute", command=command, params=params)

    def batch(self, commands):
        """commands: list of (command_id, params) pairs, run in order."""
        return self.call("batch", commands=[{"command": c, "params": p} for c, p in commands])
