from client import BLinkTree

def main():
    print("=== Testing B-link Tree Concurrent Index ===")
    tree = BLinkTree(max_keys=3)
    items = [(10, "alpha"), (20, "beta"), (5, "gamma"), (15, "delta"), (30, "epsilon"), (25, "zeta")]
    for k, v in items:
        tree.insert(k, v)

    for k, v in items:
        res = tree.search(k)
        print(f"Key {k} -> {res}")
        assert res == v

    scan_res = tree.range_scan(10, 25)
    print("Range scan [10, 25]:", scan_res)
    assert len(scan_res) == 4
    print("B-link Tree verified successfully!")

if __name__ == '__main__':
    main()
