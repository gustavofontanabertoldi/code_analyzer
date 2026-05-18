import os

def analyze_coverage(repo_path):

    test_files = 0

    for root, _, files in os.walk(repo_path):

        for file in files:

            if (
                file.endswith("Test.java")
                or "test" in root.lower()
            ):
                test_files += 1

    return {
        "test_files": test_files,
        "coverage": "unknown"
    }