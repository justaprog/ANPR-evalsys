def normalize_plate(text: str) -> str:
    text = text.upper()
    text = text.replace(" ", "")
    text = text.replace("-", "")
    return text

def edit_distance(a: str, b: str) -> int:
    """
    Simple Levenshtein distance.
    """
    m, n = len(a), len(b)

    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i

    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1

            dp[i][j] = min(
                dp[i - 1][j] + 1,       # deletion
                dp[i][j - 1] + 1,       # insertion
                dp[i - 1][j - 1] + cost # substitution
            )

    return dp[m][n]


def character_accuracy(predicted: str, ground_truth: str) -> float:
    predicted = normalize_plate(predicted)
    ground_truth = normalize_plate(ground_truth)

    if len(ground_truth) == 0:
        return 0.0

    distance = edit_distance(predicted, ground_truth)
    accuracy = 1 - distance / max(len(predicted), len(ground_truth))

    return max(0.0, accuracy)