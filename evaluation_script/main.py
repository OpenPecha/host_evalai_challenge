import json
# from evaluate import load

# cer_metric = load("cer")
# wer_metric = load("wer")

# def calculate_cer(true_text, inference_text):
#     try:
#         cer = cer_metric.compute(references=true_text, predictions=inference_text)
#         cer = min(cer, 1.0)
#         return cer
#     except:
#         return 0.0
    

# def calculate_wer(true_text, inference_text):
#     try:
#         wer = wer_metric.compute(references=true_text, predictions=inference_text)
#         wer = min(wer, 1.0)
#         return wer
#     except:
#         return 0.0


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
    with open(test_annotation_file, "r", encoding="utf-8") as test_file:
        test_data = json.load(test_file)

    with open(user_submission_file, "r", encoding="utf-8") as submission_file:
        user_data = json.load(submission_file)

    if phase_codename != "test":
        print(f"Unsupported phase_codename: {phase_codename}")
        return {"error": "Unsupported phase_codename. Only 'test' is allowed."}

    print("Evaluating for Test Phase")

    total_cer = 0
    total_wer = 0
    count = 0

    for key, reference in test_data.items():
        hypothesis = user_data.get(key, "")  # Get user's prediction or empty string
        cer = calculate_cer(reference, hypothesis)
        wer = calculate_wer(reference, hypothesis)
        total_cer += cer
        total_wer += wer
        count += 1

    avg_cer = total_cer / count if count > 0 else 0
    avg_wer = total_wer / count if count > 0 else 0

    output["result"] = [{"test_split": {"CER": round(avg_cer, 4), "WER": round(avg_wer, 4)}}]
    output["submission_result"] = output["result"][0]["test_split"]

    print(f"Evaluation Complete!\nCER: {avg_cer:.4f}, WER: {avg_wer:.4f}")
    return output
