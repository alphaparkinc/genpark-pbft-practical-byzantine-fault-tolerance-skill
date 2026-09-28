import sys
import json
from client import PBFTNode

node = PBFTNode("node_0", total_nodes=4, f=1)

def handle_request(req):
    method = req.get("method")
    params = req.get("params", {})
    req_id = req.get("id")

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "pbft_consensus_step",
                        "description": "Feed PBFT message (pre-prepare, prepare, commit) and check phase advancement",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "phase": {"type": "string", "enum": ["pre_prepare", "prepare", "commit"]},
                                "view": {"type": "integer"},
                                "seq": {"type": "integer"},
                                "sender": {"type": "string"},
                                "payload": {"type": "string"}
                            },
                            "required": ["phase", "view", "seq"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {})
        if name == "pbft_consensus_step":
            ph = args["phase"]
            v = args["view"]
            s = args["seq"]
            if ph == "pre_prepare":
                ok = node.receive_pre_prepare(v, s, args.get("payload", ""))
                return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps({"phase": "pre_prepare", "accepted": ok})}]}}
            elif ph == "prepare":
                prepared = node.receive_prepare(v, s, args.get("sender", "anon"))
                return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps({"phase": "prepare", "prepared": prepared})}]}}
            elif ph == "commit":
                committed = node.receive_commit(v, s, args.get("sender", "anon"))
                return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps({"phase": "commit", "committed": committed})}]}}
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    for line in sys.stdin:
        if line.strip():
            req = json.loads(line)
            res = handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
