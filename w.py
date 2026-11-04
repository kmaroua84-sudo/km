def regle_w(w):
    jobs = range(len(w))
    return sorted(jobs, key=lambda j: -w[j])


def cout(seq, p, w):
    t = 0
    total = 0

    for j in seq:
        t += p[j]
        total += w[j] * t

    return total


def main():
    n = int(input("Nombre de tâches : "))

    p = []
    w = []

    print("Donner les durées de traitement :")
    for j in range(n):
        p.append(float(input(f"p{j+1} = ")))

    print("Donner les poids :")
    for j in range(n):
        w.append(float(input(f"w{j+1} = ")))

    seq = regle_w(w)

    print("\nOrdre W :")
    print([j+1 for j in seq])

    print("\nDates de fin :")
    t = 0

    for j in seq:
        t += p[j]
        print(f"C{j+1} = {t}")

    total = cout(seq, p, w)
    print("\nCoût total pondéré W :")
    print(total)


if __name__ == "__main__":
    main()
