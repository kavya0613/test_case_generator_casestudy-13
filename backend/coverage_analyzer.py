from backend.schemas import TestCaseResponse


def _detect_applicable_scenarios(user_story: str):
    """
    Determine which scenario types are explicitly supported
    by the user story.
    """

    story = user_story.lower().strip()

    applicable = set()

    # ---------------------------------
    # Positive scenarios
    # ---------------------------------

    positive_phrases = [
        "want to",
        "wants to",
        "should be able to",
        "must be able to",
        "can ",
        "is able to",
        "allow the user to",
        "allows the user to",
        "so that i can",
        "so that the user can",
    ]

    if any(
        phrase in story
        for phrase in positive_phrases
    ):
        applicable.add("Positive")

    # ---------------------------------
    # Negative scenarios
    # ---------------------------------

    negative_keywords = [
        "cannot",
        "can't",
        "unable",
        "fails",
        "failure",
        "invalid",
        "wrong",
        "incorrect",
        "denied",
        "reject",
        "rejected",
        "not allowed",
        "should not",
    ]

    is_error_condition = any(
        phrase in story
        for phrase in [
            "cannot be completed",
            "unable to complete",
            "failure condition",
            "appropriate error",
            "error if",
            "error when",
        ]
    )

    if (
        any(
            keyword in story
            for keyword in negative_keywords
        )
        and not is_error_condition
    ):
        applicable.add("Negative")

    # ---------------------------------
    # Validation scenarios
    # ---------------------------------

    validation_keywords = [
        "required",
        "mandatory",
        "validation",
        "validate",
        "missing",
        "empty",
        "cannot be empty",
    ]

    if any(
        keyword in story
        for keyword in validation_keywords
    ):
        applicable.add("Validation")

    # ---------------------------------
    # Boundary scenarios
    # ---------------------------------

    boundary_keywords = [
        "minimum",
        "maximum",
        "limit",
        "threshold",
        "range",
        "at least",
        "at most",
        "between",
        "shorter than",
        "longer than",
        "exactly",
    ]

    if any(
        keyword in story
        for keyword in boundary_keywords
    ):
        applicable.add("Boundary")

    # ---------------------------------
    # Edge scenarios
    # ---------------------------------

    edge_keywords = [
        "edge case",
        "edge cases",
        "special case",
        "exceptional case",
        "unusual condition",
    ]

    if any(
        keyword in story
        for keyword in edge_keywords
    ):
        applicable.add("Edge")

    # ---------------------------------
    # Error Handling scenarios
    # ---------------------------------

    error_keywords = [
        "error",
        "error handling",
        "failure message",
        "failure condition",
        "exception",
        "unable to complete",
        "operation cannot be completed",
    ]

    if any(
        keyword in story
        for keyword in error_keywords
    ):
        applicable.add("Error Handling")

    return applicable


def _detect_test_case_scenarios(test_case):
    """
    Determine scenario types represented by an individual test case.
    """

    scenarios = set()

    test_type = test_case.test_type.strip().lower()

    title = test_case.title.lower()

    test_data = (
        test_case.test_data or ""
    ).lower()

    test_steps = " ".join(
        test_case.test_steps
    ).lower()

    combined_text = " ".join(
        [
            test_type,
            title,
            test_data,
            test_steps,
        ]
    )

    # ---------------------------------
    # Test Type
    # ---------------------------------

    if (
        "positive" in test_type
        or "functional" in test_type
    ):
        scenarios.add("Positive")

    if "negative" in test_type:
        scenarios.add("Negative")

    if "validation" in test_type:
        scenarios.add("Validation")

    if "boundary" in test_type:
        scenarios.add("Boundary")

    if "edge" in test_type:
        scenarios.add("Edge")

    if "error" in test_type:
        scenarios.add("Error Handling")

    # ---------------------------------
    # Boundary detection
    # ---------------------------------

    boundary_indicators = [
        "minimum",
        "maximum",
        "min",
        "max",
        "boundary",
        "exactly",
        "between",
        "at least",
        "at most",
        "shorter than",
        "longer than",
        "length of",
    ]

    if any(
        indicator in combined_text
        for indicator in boundary_indicators
    ):
        scenarios.add("Boundary")

    return scenarios


def analyze_coverage(
    result: TestCaseResponse,
    user_story: str,
):
    """
    Analyze scenario coverage for generated test cases.
    """

    total_test_cases = len(
        result.test_cases
    )

    covered_scenarios = set()

    for test_case in result.test_cases:

        test_case_scenarios = (
            _detect_test_case_scenarios(
                test_case
            )
        )

        covered_scenarios.update(
            test_case_scenarios
        )

    applicable_scenarios = (
        _detect_applicable_scenarios(
            user_story
        )
    )

    missing_scenarios = (
        applicable_scenarios
        - covered_scenarios
    )

    if not applicable_scenarios:

        coverage_percentage = 0

    else:

        coverage_percentage = round(
            (
                len(
                    covered_scenarios
                    & applicable_scenarios
                )
                / len(applicable_scenarios)
            )
            * 100
        )

    return {
        "total_test_cases": total_test_cases,
        "coverage_percentage": coverage_percentage,
        "covered_scenarios": sorted(
            covered_scenarios
        ),
        "missing_scenarios": sorted(
            missing_scenarios
        ),
    }