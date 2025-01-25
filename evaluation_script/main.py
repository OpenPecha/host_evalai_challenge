import json
import jiwer

def validate_submission_format(ground_truth, user_submission):
    """
    Validates if the user submission follows the required format.
    - Checks if all keys in ground_truth are present in user_submission.
    - Ensures all values in user_submission are strings.
    """
    missing_keys = [key for key in ground_truth if key not in user_submission]
    invalid_values = [key for key, value in user_submission.items() if not isinstance(value, str)]

    errors = []
    if missing_keys:
        errors.append(f"Missing keys in submission: {missing_keys}")
    if invalid_values:
        errors.append(f"Invalid values (non-strings) for keys: {invalid_values}")

    return errors

def evaluate(test_annotation_file, user_submission_file, phase_codename, **kwargs):
    print("Starting Evaluation.....")
    output = {}

    if phase_codename == "test":
        print("Evaluating for Test Phase")

        # Load ground truth and user submission JSON files
        with open(test_annotation_file, "r", encoding="utf-8") as gt_file:
            ground_truth = json.load(gt_file)

        with open(user_submission_file, "r", encoding="utf-8") as submission_file:
            user_submission = json.load(submission_file)

        # Validate submission format
        validation_errors = validate_submission_format(ground_truth, user_submission)
        if validation_errors:
            output["error"] = validation_errors
            print("Submission format validation failed.")
            return output

        # Initialize metrics
        total_wer = 0
        total_cer = 0
        total_samples = len(ground_truth)

        # Calculate metrics
        for key, reference_text in ground_truth.items():
            hypothesis_text = user_submission.get(key, "")
            wer = jiwer.wer(reference_text, hypothesis_text)
            cer = jiwer.cer(reference_text, hypothesis_text)

            total_wer += wer
            total_cer += cer

        # Average metrics
        avg_wer = total_wer / total_samples
        avg_cer = total_cer / total_samples

        # Prepare output
        output["result"] = [
            {
                "test_split": {
                    "Average WER": round(avg_wer, 4),
                    "Average CER": round(avg_cer, 4),
                }
            }
        ]
        output["submission_result"] = output["result"][0]["test_split"]

        print("Evaluation completed successfully for Test Phase.")
    else:
        print("Invalid phase codename provided. Please use 'test'.")

    return output
