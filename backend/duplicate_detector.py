from backend.schemas import TestCaseResponse


def normalize_text(text: str) -> str:
    return " ".join(
        text.lower().strip().split()
    )


def find_duplicate_test_cases(
    result: TestCaseResponse
):
    duplicates = []

    seen_cases = []

    for test_case in result.test_cases:

        current_title = normalize_text(
            test_case.title
        )

        current_steps = " ".join(
            normalize_text(step)
            for step in test_case.test_steps
        )

        current_expected = normalize_text(
            test_case.expected_result
        )

        current_test_data = normalize_text(
            test_case.test_data or ""
        )

        is_duplicate = False

        for previous_case in seen_cases:

            title_match = (
                current_title
                == previous_case["title"]
            )

            steps_match = (
                current_steps
                == previous_case["steps"]
            )

            expected_match = (
                current_expected
                == previous_case["expected"]
            )

            test_data_match = (
                current_test_data
                == previous_case["test_data"]
            )

            # A duplicate must match all important
            # scenario-defining information.
            if (
                title_match
                and steps_match
                and expected_match
                and test_data_match
            ):
                is_duplicate = True
                break

        if is_duplicate:
            duplicates.append(
                test_case.test_case_id
            )

        seen_cases.append({
            "title": current_title,
            "steps": current_steps,
            "expected": current_expected,
            "test_data": current_test_data,
        })

    return duplicates