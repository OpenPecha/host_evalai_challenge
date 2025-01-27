import json


def calculate_edit_distance(reference, hypothesis):
    """
    Compute the edit distance (Levenshtein distance) between reference and hypothesis.
    """
    m, n = len(reference), len(hypothesis)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0:
                dp[i][j] = j  # All insertions
            elif j == 0:
                dp[i][j] = i  # All deletions
            elif reference[i - 1] == hypothesis[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]  # No change
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
    return dp[m][n]


def calculate_cer(reference, hypothesis):
    """
    Calculate Character Error Rate (CER).
    """
    reference = reference.replace(" ", "")  # Remove spaces for CER
    hypothesis = hypothesis.replace(" ", "")  # Remove spaces for CER
    distance = calculate_edit_distance(reference, hypothesis)
    return distance / len(reference) if len(reference) > 0 else 0


def calculate_wer(reference, hypothesis):
    """
    Calculate Word Error Rate (WER).
    """
    ref_words = reference.split()
    hyp_words = hypothesis.split()
    distance = calculate_edit_distance(ref_words, hyp_words)
    return distance / len(ref_words) if len(ref_words) > 0 else 0


def evaluate(test_annotation_file, user_submission_file, phase_codename, **kwargs):
    print("Starting Evaluation.....")
    output = {}

    # Load test annotations and user submissions
    with open(test_annotation_file, "r") as test_file:
        test_data = json.load(test_file)

    with open(user_submission_file, "r") as submission_file:
        user_data = json.load(submission_file)

    # Ensure reference and hypothesis are available
    reference = test_data.get("reference", "")
    hypothesis = user_data.get("hypothesis", "")

    # Check phase codename (only 'test' phase is supported)
    if phase_codename == "test":
        print("Evaluating for Test Phase")

        # Calculate metrics
        cer = calculate_cer(reference, hypothesis)
        wer = calculate_wer(reference, hypothesis)

        # Output the CER and WER values
        print(f"CER (Character Error Rate): {cer}")
        print(f"WER (Word Error Rate): {wer}")

        # Prepare results
        output["result"] = [
            {
                "test_split": {
                    "CER": round(cer, 4),
                    "WER": round(wer, 4),
                }
            }
        ]
        output["submission_result"] = output["result"][0]["test_split"]

        print("Completed evaluation for Test Phase")
    else:
        print(f"Unsupported phase_codename: {phase_codename}")
        output["error"] = "Unsupported phase_codename. Only 'test' is allowed."

    return output
