from backend.schemas import TestCaseResponse as ResponseModel
from backend.validator import validate_test_cases


def test_missing_test_case_id():
    result = ResponseModel(
        test_cases=[
            {
                "testCaseId": "",
                "title": "Test transfer",
                "preconditions": ["User is registered"],
                "testData": "Valid recipient details",
                "testSteps": ["Initiate transfer"],
                "expectedResult": "Transfer is completed",
                "priority": "High",
                "testType": "Positive",
                "requirementMapping": "Transfer requirement",
            }
        ]
    )

    errors = validate_test_cases(result)

    assert any(
        "missing Test Case ID" in error
        for error in errors
    )


def test_missing_expected_result():
    result = ResponseModel(
        test_cases=[
            {
                "testCaseId": "TC_001",
                "title": "Test transfer",
                "preconditions": ["User is registered"],
                "testData": "Valid recipient details",
                "testSteps": ["Initiate transfer"],
                "expectedResult": "",
                "priority": "High",
                "testType": "Positive",
                "requirementMapping": "Transfer requirement",
            }
        ]
    )

    errors = validate_test_cases(result)

    assert any(
        "missing expected result" in error
        for error in errors
    )


def test_invalid_priority():
    result = ResponseModel(
        test_cases=[
            {
                "testCaseId": "TC_001",
                "title": "Test transfer",
                "preconditions": ["User is registered"],
                "testData": "Valid recipient details",
                "testSteps": ["Initiate transfer"],
                "expectedResult": "Transfer is completed",
                "priority": "Critical",
                "testType": "Positive",
                "requirementMapping": "Transfer requirement",
            }
        ]
    )

    errors = validate_test_cases(result)

    assert any(
        "invalid priority" in error
        for error in errors
    )