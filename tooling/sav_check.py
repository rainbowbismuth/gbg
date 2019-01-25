def sav_check(c, OUT, name):
    # The protocol is that
    #  first byte = $FA
    #  second byte = $CE
    #  third byte is number of tests planned
    #  fourth byte is number of tests run
    # Followed by a byte per test where
    #  $00 = failure
    #  $01 = success
    # All other values should be $FF
    project_sav = (OUT / name / name).with_suffix('.sav')
    results = project_sav.read_bytes()

    if results[0] != 0xFA and results[1] != 0xCE:
        print(f"{project_sav} is not a test framework .sav")
        return

    planned = results[2]
    ran = results[3]

    print(f"{planned} tests planned")
    print(f"{ran} tests ran")

    if ran > planned:
        print("more tests run then planned!")

    successes = 0
    failures = []
    unexpected = []
    unplanned = []
    for idx in range(4, len(results)):
        byte = results[idx]
        if ran and byte == 0:
            failures.append(idx - 3)
            planned -= 1
        if ran and byte == 1:
            successes += 1
            planned -= 1
        if ran and byte > 1:
            unexpected.append((idx, byte))
        if not ran and byte != 0xFF:
            unexpected.append((idx, byte))
        ran = max(0, ran - 1)

    print(f'{successes} successes')
    if planned > 0:
        print(f"{planned} tests planned, but not executed!")
    if failures:
        print(f"{len(failures)} failures")
        print(f"caused by tests: {', '.join(map(str, failures))}")
    if unexpected:
        # TODO: Print unexpected values instead of hexdump
        print(f"{len(unexpected)} unexpected values")
        c.run(f'hexdump {project_sav}')
