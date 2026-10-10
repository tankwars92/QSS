
from math import isqrt
from statistics import median, geometric_mean
from time import perf_counter


def G_direct(n):
    total = 0
    for k in range(1, n + 1):
        total += (n // k) * (n // (2 * k + 1))
    return total


def G_group_a(n):
    total = 0
    k = 1

    while k <= n:
        a = n // k
        r = n // a

        for j in range(k, r + 1):
            total += a * (n // (2 * j + 1))

        k = r + 1

    return total


def G_joint(n):
    total = 0
    k = 1

    while True:
        a = n // k
        b = n // (2 * k + 1)

        if b == 0:
            break

        end_a = n // a
        end_b = (n // b - 1) // 2
        r = min(end_a, end_b)

        total += (r - k + 1) * a * b
        k = r + 1

    return total


def G_swapped(n):
    total = 0
    k = 1

    while True:
        b = n // (2 * k + 1)

        if b == 0:
            break

        end_b = (n // b - 1) // 2
        j = k

        while j <= end_b:
            a = n // j
            end_a = n // a
            r = min(end_a, end_b)

            total += (r - j + 1) * a * b
            j = r + 1

        k = end_b + 1

    return total


def G_qss(n):
    if n <= 0:
        return 0

    total = 0
    s = isqrt(n)

    for k in range(1, s + 1):
        b = n // (2 * k + 1)
        if b == 0:
            break
        total += (n // k) * b

    a_start = n // (s + 1)
    if a_start == 0:
        return total

    k = n // (a_start + 1) + 1

    for a in range(a_start, 0, -1):
        r = n // a
        b = n // (2 * k + 1)

        if b == 0:
            break

        br = n // (2 * r + 1)

        if b == br:
            total += (r - k + 1) * a * b
        else:
            split = (n // b - 1) // 2
            total += a * (
                (split - k + 1) * b
                + (r - split) * br
            )

        k = r + 1

    return total


def measure(fn, n, repeats=7):
    fn(n)
    samples = []

    for _ in range(repeats):
        start = perf_counter()
        fn(n)
        samples.append(perf_counter() - start)

    return median(samples)



def main():
    methods = [
        ("Direct", G_direct),
        ("Group-A", G_group_a),
        ("Joint", G_joint),
        ("Swapped", G_swapped),
        ("QSS (ours)", G_qss),
    ]

    sizes = [
        10_000,
        100_000,
        1_000_000,
        10_000_000,
        100_000_000,
    ]

    print("Exactness check: N=1..5000")

    for n in range(1, 5001):
        expected = G_qss(n)
        for name, fn in methods:
            assert fn(n) == expected, (name, n)

    print("PASS")
    print()

    results = {}

    for n in sizes:
        print(f"Calculating N={n:,}...")
        row = {}

        for name, fn in methods:
            elapsed = measure(fn, n)
            row[name] = elapsed
            print(f"  {name}: {elapsed * 1000:.4f} ms")

        results[n] = row

    headers = ["Method"] + [f"N={n:,}" for n in sizes]
    widths = [16] + [15] * len(sizes)

    print()
    print("Cell values show how many times faster QSS is.")
    print()

    print("".join(
        h.ljust(w) for h, w in zip(headers, widths)
    ))
    print("-" * sum(widths))

    names = [
        "Direct",
        "Group-A",
        "Joint",
        "Swapped",
        "QSS (ours)",
    ]

    all_speedups = []

    for name in names:
        cells = [name]

        for n in sizes:
            row = results[n]

            if name == "QSS (ours)":
                value = "1.00x"
            else:
                speedup = row[name] / row["QSS (ours)"]
                value = f"{speedup:.2f}x"
                all_speedups.append(speedup)

            cells.append(value)

        print("".join(
            cell.ljust(w) for cell, w in zip(cells, widths)
        ))

    print()
    print(
        "Geometric mean speedup across measured comparisons: "
        f"{geometric_mean(all_speedups):.2f}x"
    )
    print("Exact integer results verified.")



if __name__ == "__main__":
    main()
