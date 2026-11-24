
import itertools
import matplotlib.pyplot as plt


# ============================================================
# FONCTIONS GENERALES
# ============================================================

def aff(sequence):
    """Affichage des sequences sous la forme J1, J2, ..."""
    return " -> ".join(f"J{j+1}" for j in sequence)


def evaluer(sequence, p, w):
    """Calcul des dates d'achevement et du critere somme(wj*Cj)."""
    temps = 0
    C = [0] * len(p)

    for j in sequence:
        temps += p[j]
        C[j] = temps

    total = sum(w[j] * C[j] for j in range(len(p)))
    return C, total


def gantt_machine(segments, titre):
    """Construction du diagramme de Gantt."""
    fig, ax = plt.subplots(figsize=(11, 3))

    for debut, duree, j in segments:
        ax.barh(
            y=0,
            width=duree,
            left=debut,
            height=0.5,
            edgecolor="black"
        )

        ax.text(
            debut + duree / 2,
            0,
            f"J{j+1}",
            ha="center",
            va="center",
            fontsize=10
        )

    ax.set_title(titre)
    ax.set_xlabel("Temps")
    ax.set_yticks([])
    ax.grid(axis="x", linestyle="--", alpha=0.5)

    plt.tight_layout()
    plt.show()


# ============================================================
# Q5 : INSTANCE A2 - CONTRAINTES DE PRECEDENCE
# ============================================================

A2_p = [3, 6, 2, 5, 4, 7, 8, 1]
A2_w = [2, 15, 3, 4, 14, 6, 12, 4]

CHAINES = [
    [0, 1, 2],  # J1 -> J2 -> J3
    [3, 4, 5],  # J4 -> J5 -> J6
    [6, 7]      # J7 -> J8
]


def calcul_rho(chaine, p, w):
    """Calcul du rho maximal des prefixes d'une chaine."""

    somme_p = 0
    somme_w = 0
    rho_max = -1
    indice_critique = 0

    for k, j in enumerate(chaine):
        somme_p += p[j]
        somme_w += w[j]

        rho = somme_w / somme_p

        if rho > rho_max:
            rho_max = rho
            indice_critique = k + 1

    return rho_max, indice_critique


def methode_rho(chaines, p, w):
    """Construction d'une sequence respectant les precedences."""

    restantes = [list(c) for c in chaines]
    sequence = []

    while any(restantes):

        meilleur_rho = -1
        meilleure_chaine = None
        meilleur_indice = 0

        for i, chaine in enumerate(restantes):

            if chaine:
                rho, indice = calcul_rho(chaine, p, w)

                if rho > meilleur_rho:
                    meilleur_rho = rho
                    meilleure_chaine = i
                    meilleur_indice = indice

        prefixe = restantes[meilleure_chaine][:meilleur_indice]

        sequence.extend(prefixe)

        restantes[meilleure_chaine] = (
            restantes[meilleure_chaine][meilleur_indice:]
        )

    return sequence


def enumeration_precedence(p, w, chaines):
    """Enumeration des sequences admissibles."""

    meilleure_valeur = float("inf")
    sequences_optimales = []

    for seq in itertools.permutations(range(len(p))):

        positions = {j: i for i, j in enumerate(seq)}

        admissible = all(
            positions[chaine[k]] < positions[chaine[k + 1]]
            for chaine in chaines
            for k in range(len(chaine) - 1)
        )

        if admissible:

            C, total = evaluer(seq, p, w)

            if total < meilleure_valeur:
                meilleure_valeur = total
                sequences_optimales = [seq]

            elif total == meilleure_valeur:
                sequences_optimales.append(seq)

    return meilleure_valeur, sequences_optimales


# ============================================================
# Q6 : INSTANCE A3 - DATES DE DISPONIBILITE
# ============================================================

A3_p = [7, 3, 3, 8, 2, 3]
A3_r = [0, 1, 2, 4, 8, 10]


def srpt(p, r):
    """Algorithme SRPT avec preemption."""

    n = len(p)
    restant = p.copy()
    C = [0] * n

    segments = []
    temps = 0
    termines = 0

    while termines < n:

        disponibles = [
            j for j in range(n)
            if r[j] <= temps and restant[j] > 0
        ]

        if not disponibles:
            temps = min(
                r[j] for j in range(n)
                if restant[j] > 0
            )
            continue

        j = min(disponibles, key=lambda x: (restant[x], x))

        prochaines_arrivees = [
            r[k] for k in range(n)
            if r[k] > temps
        ]

        prochaine_arrivee = (
            min(prochaines_arrivees)
            if prochaines_arrivees
            else float("inf")
        )

        duree = min(
            restant[j],
            prochaine_arrivee - temps
        )

        if duree == float("inf"):
            duree = restant[j]

        segments.append((temps, duree, j))

        temps += duree
        restant[j] -= duree

        if restant[j] == 0:
            C[j] = temps
            termines += 1

    return C, segments


def enumeration_non_preemptive(p, r):
    """Enumeration des sequences non preemptives."""

    n = len(p)

    meilleure_valeur = float("inf")
    meilleures_sequences = []

    meilleur_C = None
    meilleurs_segments = None

    for seq in itertools.permutations(range(n)):

        temps = 0
        C = [0] * n
        segments = []

        for j in seq:

            debut = max(temps, r[j])
            fin = debut + p[j]

            segments.append((debut, p[j], j))

            C[j] = fin
            temps = fin

        total = sum(C)

        if total < meilleure_valeur:

            meilleure_valeur = total
            meilleures_sequences = [seq]
            meilleur_C = C
            meilleurs_segments = segments

        elif total == meilleure_valeur:

            meilleures_sequences.append(seq)

    return (
        meilleure_valeur,
        meilleures_sequences,
        meilleur_C,
        meilleurs_segments
    )


# ============================================================
# EXECUTION DES QUESTIONS Q5 ET Q6
# ============================================================

if __name__ == "__main__":

    # --------------------------------------------------------
    # Q5 : INSTANCE A2
    # --------------------------------------------------------

    print("\n========== Q5 : INSTANCE A2 ==========")

    print("\nCalcul des rho des chaines :")

    for i, chaine in enumerate(CHAINES):

        rho, indice = calcul_rho(chaine, A2_p, A2_w)

        print(
            f"Chaine C{i+1} : rho = {rho:.4f}, "
            f"prefixe critique = {aff(chaine[:indice])}"
        )

    sequence_A2 = methode_rho(CHAINES, A2_p, A2_w)

    C_A2, cout_A2 = evaluer(
        sequence_A2, A2_p, A2_w
    )

    print("\nSequence obtenue par la methode rho :")
    print(aff(sequence_A2))

    print("Dates d'achevement :", C_A2)
    print("Cout total :", cout_A2)

    # Verification par enumeration

    valeur_enum, sequences_enum = enumeration_precedence(
        A2_p, A2_w, CHAINES
    )

    print("\nVerification par enumeration :")
    print("Nombre de sequences optimales :", len(sequences_enum))
    print("Valeur optimale :", valeur_enum)

    for seq in sequences_enum:
        print("Sequence optimale :", aff(seq))

    # Diagramme de Gantt A2

    segments_A2 = []
    temps = 0

    for j in sequence_A2:

        segments_A2.append((temps, A2_p[j], j))
        temps += A2_p[j]

    gantt_machine(
        segments_A2,
        "Diagramme de Gantt - A2 avec precedences"
    )


    # --------------------------------------------------------
    # Q6 : INSTANCE A3 - SRPT
    # --------------------------------------------------------

    print("\n========== Q6 : INSTANCE A3 ==========")

    C_SRPT, segments_SRPT = srpt(A3_p, A3_r)

    print("\nMethode SRPT :")
    print("Dates d'achevement :", C_SRPT)
    print("Somme des Cj :", sum(C_SRPT))

    print("\nSegments d'execution SRPT :")

    for debut, duree, j in segments_SRPT:

        print(
            f"J{j+1} : [{debut}, {debut + duree}]"
        )

    gantt_machine(
        segments_SRPT,
        "Diagramme de Gantt - SRPT"
    )


    # --------------------------------------------------------
    # Q6 : OPTIMISATION NON PREEMPTIVE
    # --------------------------------------------------------

    print("\nMethode non preemptive :")

    valeur_np, sequences_np, C_np, segments_np = (
        enumeration_non_preemptive(A3_p, A3_r)
    )

    print("Sequence optimale :", aff(sequences_np[0]))
    print("Dates d'achevement :", C_np)
    print("Somme des Cj :", valeur_np)

    print("\nSequences optimales :")

    for seq in sequences_np:
        print(aff(seq))

    gantt_machine(
        segments_np,
        "Diagramme de Gantt - Optimum non preemptif"
    )


    # --------------------------------------------------------
    # COMPARAISON FINALE Q6
    # --------------------------------------------------------

    print("\n========== COMPARAISON Q6 ==========")

    print("SRPT :", sum(C_SRPT))
    print("Optimum non preemptif :", valeur_np)

    print("\nFin de l'execution.")
