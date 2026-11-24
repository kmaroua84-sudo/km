
"""
TP N°1 -- Machine unique et temps d'achevement
Ordonnancement d'Atelier (2026/2027)
USDB1 -- Master RO/MSS

Partie A1 : Q1, Q2, Q3 et Q4
"""

import itertools
import math

import numpy as np
import matplotlib.pyplot as plt


# -----------------------------------------------------------------
# DONNEES A1

A1_p = [4, 7, 2, 9, 5, 3]
A1_w = [3, 6, 5, 4, 8, 2]


# -----------------------------------------------------------------
# OUTILS FOURNIS PAR LE PROFESSEUR

def aff(seq):
    """Affiche une sequence avec des jobs numerotes a partir de 1."""
    return "(" + ", ".join(str(j + 1) for j in seq) + ")"


def instance_aleatoire(n, graine, alpha=0.0):
    """Genere une instance aleatoire."""
    rng = np.random.default_rng(graine)
    p = rng.integers(1, 21, size=n).tolist()
    w = rng.integers(1, 11, size=n).tolist()
    r = rng.integers(0, int(alpha * sum(p)) + 1, size=n).tolist()
    return p, w, r


def gantt_machine(segments, titre="", fichier=None):
    """Diagramme de Gantt d'une machine."""
    fig, ax = plt.subplots(figsize=(9, 1.8))
    cmap = plt.get_cmap("tab10")

    for (debut, duree, j) in segments:
        ax.barh(0, duree, left=debut,
                color=cmap(j % 10), edgecolor="black")
        ax.text(debut + duree / 2, 0, "J%d" % (j + 1),
                ha="center", va="center", fontsize=8)

    ax.set_yticks([])
    ax.set_xlabel("temps")
    ax.set_title(titre)
    ax.grid(axis="x", alpha=0.3)
    fig.tight_layout()

    if fichier:
        fig.savefig(fichier, dpi=150)

    plt.show()


# =================================================================
# Q1 : EVALUER UNE SEQUENCE

def evaluer(seq, p, w):
    C = [0] * len(p)
    temps = 0
    total = 0

    for j in seq:
        temps += p[j]
        C[j] = temps
        total += w[j] * C[j]

    return C, total


# =================================================================
# Q2 : REGLE WSPT

def wspt(p, w):
    return sorted(
        range(len(p)),
        key=lambda j: (-w[j] / p[j], j)
    )


# Q2 : REGLE SPT

def spt(p):
    return sorted(
        range(len(p)),
        key=lambda j: (p[j], j)
    )


# =================================================================
# Q3 : VERIFICATION PAR ENUMERATION

def enumeration(p, w):
    meilleure_valeur = float("inf")
    sequences_optimales = []

    for seq in itertools.permutations(range(len(p))):
        C, total = evaluer(seq, p, w)

        if total < meilleure_valeur:
            meilleure_valeur = total
            sequences_optimales = [seq]

        elif total == meilleure_valeur:
            sequences_optimales.append(seq)

    return meilleure_valeur, sequences_optimales


# =================================================================
# Q4 : DISTRIBUTION DU CRITERE

def statistiques(p, w):
    couts = []

    for seq in itertools.permutations(range(len(p))):
        C, total = evaluer(seq, p, w)
        couts.append(total)

    minimum = min(couts)
    maximum = max(couts)
    moyenne = np.mean(couts)

    return minimum, maximum, moyenne, couts


# Q4(b) : PIRE SEQUENCE SANS ENUMERATION

def pire_sequence(p, w):
    return sorted(
        range(len(p)),
        key=lambda j: (w[j] / p[j], j)
    )


# Q4(a) : HISTOGRAMME DES COUTS

def histogramme(couts, cout_wspt, cout_spt, cout_naturel):

    plt.figure(figsize=(9, 5))

    plt.hist(couts, bins=20, edgecolor="black")

    plt.axvline(cout_wspt, color="green",
                linestyle="--", label="WSPT")

    plt.axvline(cout_spt, color="red",
                linestyle="--", label="SPT")

    plt.axvline(cout_naturel, color="orange",
                linestyle="--", label="Ordre naturel")

    plt.xlabel("Cout total")
    plt.ylabel("Frequence")
    plt.title("Histogramme des couts des sequences")
    plt.legend()
    plt.grid(axis="y", alpha=0.3)

    plt.tight_layout()
    plt.show()


# =================================================================
# EXECUTION

if __name__ == "__main__":

    # ---------------- Q1 ----------------

    naturel = list(range(len(A1_p)))

    C, total = evaluer(naturel, A1_p, A1_w)

    print("========== Q1 ==========")
    print("Ordre naturel :", aff(naturel))
    print("Dates d'achevement :", C)
    print("Cout total :", total)

    sequence_donnee = [1, 3, 5, 0, 2, 4]

    C, total = evaluer(sequence_donnee, A1_p, A1_w)

    print("\nSequence donnee :", aff(sequence_donnee))
    print("Dates d'achevement :", C)
    print("Cout total :", total)


    # ---------------- Q2 : WSPT ----------------

    sequence_wspt = wspt(A1_p, A1_w)

    C_wspt, total_wspt = evaluer(
        sequence_wspt, A1_p, A1_w
    )

    print("\n========== Q2 : WSPT ==========")
    print("Sequence WSPT :", aff(sequence_wspt))
    print("Dates d'achevement :", C_wspt)
    print("Cout WSPT :", total_wspt)

    # Diagramme de Gantt WSPT

    segments = []
    temps = 0

    for j in sequence_wspt:
        segments.append((temps, A1_p[j], j))
        temps += A1_p[j]

    gantt_machine(
        segments,
        titre="Diagramme de Gantt - WSPT"
    )


    # ---------------- Q2 : SPT ----------------

    sequence_spt = spt(A1_p)

    C_spt, total_spt = evaluer(
        sequence_spt, A1_p, A1_w
    )

    print("\n========== Q2 : SPT ==========")
    print("Sequence SPT :", aff(sequence_spt))
    print("Dates d'achevement :", C_spt)
    print("Cout SPT :", total_spt)

    print("Somme des Cj pour SPT :", sum(C_spt))
    print("Somme des Cj pour WSPT :", sum(C_wspt))


    # ---------------- Q3 : ENUMERATION ----------------

    meilleure_valeur, sequences = enumeration(
        A1_p, A1_w
    )

    print("\n========== Q3 : ENUMERATION ==========")
    print("Valeur optimale :", meilleure_valeur)
    print("Sequences optimales :")

    for seq in sequences:
        print(aff(seq))

    gain = (507 - meilleure_valeur) / 507 * 100

    print("Gain par rapport a l'ordre naturel :",
          round(gain, 1), "%")


    # ---------------- Q4 : STATISTIQUES ----------------

    minimum, maximum, moyenne, couts = statistiques(
        A1_p, A1_w
    )

    print("\n========== Q4 : STATISTIQUES ==========")
    print("Minimum :", minimum)
    print("Maximum :", maximum)
    print("Moyenne :", moyenne)

    # Pire sequence sans enumeration

    sequence_pire = pire_sequence(A1_p, A1_w)

    C_pire, cout_pire = evaluer(
        sequence_pire, A1_p, A1_w
    )

    print("Pire sequence :", aff(sequence_pire))
    print("Cout de la pire sequence :", cout_pire)


    # Histogramme avec reperage des trois sequences

    histogramme(
        couts,
        total_wspt,
        total_spt,
        507
    )
