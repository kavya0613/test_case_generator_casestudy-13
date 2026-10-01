from backend.schemas import TestCaseResponse


def validate_user_story(user_story: str):
    """
    Validate the user story before sending it to Gemini.
    """

    errors = []

    story = user_story.strip()

    # Empty user story
    if not story:
        errors.append(
            "User story cannot be empty."
        )
        return errors

    # Very short user story
    if len(story) < 20:
        errors.append(
            "User story is too short. "
            "Please provide a complete requirement."
        )

    return errors


def validate_test_cases(result: TestCaseResponse):
    errors = []

    if not result.test_cases:
        errors.append("No test cases were generated.")

    test_case_ids = set()

    for index, test_case in enumerate(
        result.test_cases,
        start=1,
    ):

        # Check Test Case ID
        if not test_case.test_case_id.strip():
            errors.append(
                f"Test case {index} is missing Test Case ID."
            )

        elif test_case.test_case_id in test_case_ids:
            errors.append(
                f"Duplicate Test Case ID found: "
                f"{test_case.test_case_id}"
            )

        else:
            test_case_ids.add(
                test_case.test_case_id
            )

        # Check title
        if not test_case.title.strip():
            errors.append(
                f"{test_case.test_case_id} "
                f"is missing a title."
            )

        # Preconditions are optional
        # because they may not be specified
        # in the requirement.

        # Check test steps
        if not test_case.test_steps:
            errors.append(
                f"{test_case.test_case_id} "
                f"is missing test steps."
            )

        # Check expected result
        if not test_case.expected_result.strip():
            errors.append(
                f"{test_case.test_case_id} "
                f"is missing expected result."
            )

        # Check priority
        if test_case.priority not in [
            "High",
            "Medium",
            "Low",
        ]:
            errors.append(
                f"{test_case.test_case_id} "
                f"has invalid priority."
            )

        # Check test type
        if not test_case.test_type.strip():
            errors.append(
                f"{test_case.test_case_id} "
                f"is missing test type."
            )

        # Check requirement mapping
        if not test_case.requirement_mapping:
            errors.append(
                f"{test_case.test_case_id} "
                f"is missing requirement mapping."
            )

    return errors