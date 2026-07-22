import datetime, os

LOGDIR = os.path.dirname(os.path.abspath(__file__))
LOGFILE = os.path.join(LOGDIR, "round_log.txt")


def generate_diff(old_code, new_code):
    old_set = set(old_code.strip().splitlines())
    new_set = set(new_code.strip().splitlines())
    added = [s.strip() for s in (new_set - old_set) if s.strip() and s[0] != "#"]
    removed = [s.strip() for s in (old_set - new_set) if s.strip() and s[0] != "#"]
    return added, removed


def format_remaining(stdout):
    if not stdout:
        return ["(check output empty)"]
    fails = []
    for line in stdout.splitlines():
        if "FAIL" in line:
            fails.append(line.strip())
    return fails if fails else ["(all passed)"]


def print_summary(round_num, old_code, new_code, stdout):
    added, removed = generate_diff(old_code, new_code)
    remaining = format_remaining(stdout)
    print()
    print(f"      === Round {round_num} Summary ===")
    if added:
        print(f"      [ADDED] {len(added)} lines")
        for a in sorted(added)[:8]:
            print("        + " + str(a[:70].encode("ascii","replace")))
        if len(added) > 8:
            print(f"        ... {len(added)-8} more")
    if removed:
        print(f"      [REMOVED] {len(removed)} lines")
        for r in sorted(removed)[:8]:
            print("        - " + str(r[:70].encode("ascii","replace")))
        if len(removed) > 8:
            print(f"        ... {len(removed)-8} more")
    if not added and not removed:
        print(f"      (no changes)")
    print(f"      [REMAINING] {len(remaining)} problems")
    for r in remaining[:5]:
        print(f"        {r[:80]}")
    if len(remaining) > 5:
        print(f"        ... {len(remaining)-5} more")


def write_log(round_num, passed, old_code, new_code, stdout):
    added, removed = generate_diff(old_code, new_code)
    chg = str(len(added)) + " added, " + str(len(removed)) + " removed"
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "PASS" if passed else "FAIL"
    mark = " [FIXED]" if passed else ""
    line = "{:02d} | {} | {} | {}{}".format(round_num, status, chg, ts, mark)
    with open(LOGFILE, "a", encoding="utf-8") as f:
        f.write(line + chr(10))
    if passed:
        rem = format_remaining(stdout)
        with open(LOGFILE, "a", encoding="utf-8") as f:
            f.write("  Result: " + rem[0] + chr(10))
            f.write("=" * 50 + chr(10))