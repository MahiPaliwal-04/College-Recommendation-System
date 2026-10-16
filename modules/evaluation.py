import numpy as np


def precision_at_k(recommended, relevant, k=5):

    recommended_k = recommended[:k]

    if len(recommended_k) == 0:
        return 0.0

    hits = len(
        set(recommended_k) & set(relevant)
    )

    return round(
        hits / len(recommended_k),
        4
    )


def recall_at_k(recommended, relevant, k=5):

    recommended_k = recommended[:k]

    if len(relevant) == 0:
        return 0.0

    hits = len(
        set(recommended_k) & set(relevant)
    )

    return round(
        hits / len(relevant),
        4
    )


def ndcg_at_k(recommended, relevant, k=5):

    recommended_k = recommended[:k]

    dcg = 0.0

    for i, item in enumerate(recommended_k):

        if item in relevant:

            dcg += 1 / np.log2(
                i + 2
            )

    ideal_hits = min(
        len(relevant),
        k
    )

    if ideal_hits == 0:
        return 0.0

    idcg = sum(
        1 / np.log2(i + 2)
        for i in range(ideal_hits)
    )

    return round(
        dcg / idcg,
        4
    )