from backend.schemas import TestCaseResponse as ResponseModel
from backend.duplicate_detector import find_duplicate_test_cases
from backend.coverage_analyzer import analyze_coverage


def test_generated_response_contains_test_cases():
    result = ResponseModel(
        test_cases=[
            {
                "testCaseId": "TC_001",
                "title": "Successful money transfer",
                "preconditions": [
                    "User is a registered bank customer"
                ],
                "testData": "Valid recipient account details",
                "testSteps": [
                    "Enter recipient account details",
                    "Initiate the transfer"
                ],
                "expectedResult": (
                    "Money is successfully transferred "
                    "to the recipient account."
                ),
                "priority": "High",
                "testType": "Positive",
                "requirementMapping": (
                    "Customer can transfer money "
                    "to another bank account."
                ),
            }
        ]
    )

    assert len(result.test_cases) > 0


def test_generated_test_case_has_required_fields():
    result = ResponseModel(
        test_cases=[
            {
                "testCaseId": "TC_001",
                "title": "Successful money transfer",
                "preconditions": [
                    "User is a registered bank customer"
                ],
                "testData": "Valid recipient account details",
                "testSteps": [
                    "Enter recipient account details",
                    "Initiate the transfer"
                ],
                "expectedResult": (
                    "Money is successfully transferred "
                    "to the recipient account."
                ),
                "priority": "High",
                "testType": "Positive",
                "requirementMapping": (
                    "Customer can transfer money "
                    "to another bank account."
                ),
            }
        ]
    )

    test_case = result.test_cases[0]

    assert test_case.test_case_id
    assert test_case.title
    assert test_case.preconditions
    assert test_case.test_steps
    assert test_case.expected_result
    assert test_case.priority
    assert test_case.test_type
    assert test_case.requirement_mapping


def test_duplicate_test_cases_are_detected():
    result = ResponseModel(
        test_cases=[
            {
                "testCaseId": "TC_001",
                "title": "Successful money transfer",
                "preconditions": ["User is registered"],
                "testData": "Valid recipient details",
                "testSteps": [
                    "Enter recipient details",
                    "Initiate transfer"
                ],
                "expectedResult": "Money is transferred successfully",
                "priority": "High",
                "testType": "Positive",
                "requirementMapping": "Transfer money requirement",
            },
            {
                "testCaseId": "TC_002",
                "title": "Successful money transfer",
                "preconditions": ["User is registered"],
                "testData": "Valid recipient details",
                "testSteps": [
                    "Enter recipient details",
                    "Initiate transfer"
                ],
                "expectedResult": "Money is transferred successfully",
                "priority": "High",
                "testType": "Positive",
                "requirementMapping": "Transfer money requirement",
            },
        ]
    )

    duplicates = find_duplicate_test_cases(result)

    assert duplicates == ["TC_002"]


def test_coverage_analyzer():
    result = ResponseModel(
        test_cases=[
            {
                "testCaseId": "TC_001",
                "title": "Successful money transfer",
                "preconditions": ["User is registered"],
                "testData": "Valid recipient details",
                "testSteps": [
                    "Enter recipient details",
                    "Initiate transfer"
                ],
                "expectedResult": "Money is transferred successfully",
                "priority": "High",
                "testType": "Positive",
                "requirementMapping": (
                    "Customer can transfer money "
                    "to another bank account."
                ),
            },
            {
                "testCaseId": "TC_002",
                "title": "Transfer with missing recipient details",
                "preconditions": ["User is registered"],
                "testData": "Missing recipient details",
                "testSteps": [
                    "Leave recipient details empty",
                    "Attempt transfer"
                ],
                "expectedResult": "Transfer is not initiated",
                "priority": "High",
                "testType": "Validation",
                "requirementMapping": (
                    "Recipient account details are required."
                ),
            },
        ]
    )

    coverage = analyze_coverage(
        result,
        "Customer can transfer money to another bank account."
    )

    assert coverage["total_test_cases"] == 2
    assert coverage["coverage_percentage"] > 0
    assert "Positive" in coverage["covered_scenarios"]
    assert "Validation" in coverage["covered_scenarios"]