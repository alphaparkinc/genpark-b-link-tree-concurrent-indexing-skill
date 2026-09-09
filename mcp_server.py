import sys
import json
from client import BLinkTree

def handle_request(req):
    method = req.get("method")
    params = req.get("params", {})
    if method == "range_scan":
        tree = BLinkTree()
        for k, v in params.get("items", []):
            tree.insert(k, v)
        return {"results": tree.range_scan(params.get("min", 0), params.get("max", 100))}
    return {"error": "Unknown method"}

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        req = json.loads(line)
        res = handle_request(req)
        print(json.dumps(res))
        sys.stdout.flush()

if __name__ == '__main__':
    main()
