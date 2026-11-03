def spt(p):
    jobs = range(len(p))
    return sorted(jobs, key=lambda j: p[j])


def cout(seq, p, w):
    t, total = 0, 0

    for j in seq:
        t += p[j]
        total += w[j] * t

    return total


def main():
    n = int(input("Nombre de tâches : "))

    p = []
    w = []

    for j in range(n):
        p.append(float(input(f"p{j+1} = ")))

    for j in range(n):
        w.append(float(input(f"w{j+1} = ")))

    seq = spt(p)

    print("\nOrdre SPT :")
    print([j+1 for j in seq])

    print("\nDates de fin :")
    t = 0

    for j in seq:
        t += p[j]
        print(f"C{j+1} = {t}")

    total = cout(seq, p, w)

    print("\nCoût total pondéré SPT :")
    print(total)


if __name__ == "__main__":
    main()
