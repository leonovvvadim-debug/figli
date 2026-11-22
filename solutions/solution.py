#!/usr/bin/env python3
"""Greedy valid scheduler for contest problem B. Happiness."""

import sys


def solve() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    p = 0
    T, S, U, C, H, G = data[p:p + 6]
    p += 6
    home_limit = data[p:p + H]
    p += H

    device_home = [0] * S
    device_limit = [0] * S
    weights = [[0] * C for _ in range(S)]
    for i in range(S):
        row = data[p:p + C + 2]
        p += C + 2
        device_home[i], device_limit[i] = row[0], row[1]
        weights[i] = row[2:]

    upd_class = [0] * U
    upd_size = [0] * U
    upd_happy = [0] * U
    upd_release = [0] * U
    for k in range(U):
        c, size, happy, release = data[p:p + 4]
        p += 4
        upd_class[k], upd_size[k], upd_happy[k], upd_release[k] = c, size, happy, release

    candidates = []
    for i in range(S):
        for k in range(U):
            c = upd_class[k]
            size = upd_size[k]
            happy = upd_happy[k]
            release = upd_release[k]
            if weights[i][c] <= 0 or happy <= 0 or size <= 0 or release >= T:
                continue
            potential = weights[i][c] * happy * (T - release)
            candidates.append((potential / size, potential, -release, i, k))
    candidates.sort(reverse=True)

    server_used = [0] * T
    home_used = [[0] * H for _ in range(T)]
    events = [[[] for _ in range(C)] for _ in range(S)]
    used_updates = [set() for _ in range(S)]
    deployment_count = [0] * S
    answer = []

    for _, _, _, i, k in candidates:
        if deployment_count[i] >= device_limit[i] or k in used_updates[i]:
            continue
        c, size, happy, release = upd_class[k], upd_size[k], upd_happy[k], upd_release[k]
        w = weights[i][c]
        home = device_home[i]
        if size > G or size > home_limit[home]:
            continue

        seq = events[i][c]
        chosen = -1
        for day in range(release, T):
            if server_used[day] + size > G or home_used[day][home] + size > home_limit[home]:
                continue
            pos = 0
            while pos < len(seq) and seq[pos][0] < day:
                pos += 1
            if pos < len(seq) and seq[pos][0] == day:
                continue
            prev_happy = seq[pos - 1][1] if pos else 0
            next_happy = seq[pos][1] if pos < len(seq) else None
            if prev_happy > happy or (next_happy is not None and happy > next_happy):
                continue
            next_day = seq[pos][0] if pos < len(seq) else T
            if w * (happy - prev_happy) * (next_day - day) <= 0:
                continue
            chosen = day
            break

        if chosen < 0:
            continue
        pos = 0
        while pos < len(seq) and seq[pos][0] < chosen:
            pos += 1
        seq.insert(pos, (chosen, happy, k))
        server_used[chosen] += size
        home_used[chosen][home] += size
        used_updates[i].add(k)
        deployment_count[i] += 1
        answer.append((chosen, i, k))

    print(len(answer))
    for day, device, update in answer:
        print(day, device, update)


if __name__ == "__main__":
    solve()
