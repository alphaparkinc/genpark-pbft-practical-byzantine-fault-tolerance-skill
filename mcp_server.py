"""MCP Server for PBFT Consensus Skill."""
import json
import sys
from client import PBFTCluster

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            req_id = req.get("id")
            method = req.get("method")
            params = req.get("params", {})

            if method == "tools/list":
                res = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "tools": [{
                            "name": "run_pbft_consensus",
                            "description": "Execute PBFT 3-phase consensus round with Byzantine tolerance",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "num_nodes": {"type": "integer"},
                                    "request": {"type": "string"},
                                    "faulty_nodes": {"type": "array", "items": {"type": "integer"}}
                                },
                                "required": ["num_nodes", "request"]
                            }
                        }]
                    }
                }
            elif method == "tools/call":
                args = params.get("arguments", {})
                cluster = PBFTCluster(args["num_nodes"])
                out = cluster.consensus_round(args["request"], args.get("faulty_nodes"))
                res = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {"content": [{"type": "text", "text": json.dumps(out)}]}
                }
            else:
                res = {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}
            print(json.dumps(res), flush=True)
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32000, "message": str(e)}}
            print(json.dumps(err), flush=True)

if __name__ == "__main__":
    main()
