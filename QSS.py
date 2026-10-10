from math import isqrt


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


if __name__ == "__main__":
    n = int(input("N = "))
    print(G_qss(n))
