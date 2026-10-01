import pandas as pd

from backend.schemas import TestCaseResponse


def test_cases_to_dataframe(result: TestCaseResponse):
    rows = []

    for test_case in result.test_cases:
        rows.append({
            "Test Case ID": test_case.test_case_id,
            "Title": test_case.title,
            "Preconditions": "\n".join(test_case.preconditions),
            "Test Data": test_case.test_data or "",
            "Test Steps": "\n".join(test_case.test_steps),
            "Expected Result": test_case.expected_result,
            "Priority": test_case.priority,
            "Test Type": test_case.test_type,
            "Requirement Mapping": (
                test_case.requirement_mapping or ""
            ),
        })

    return pd.DataFrame(rows)


def export_to_csv(result: TestCaseResponse):
    df = test_cases_to_dataframe(result)
    return df.to_csv(index=False)


def export_to_excel(result: TestCaseResponse):
    df = test_cases_to_dataframe(result)

    output = "test_cases.xlsx"
    df.to_excel(output, index=False)

    return output
def export_to_json(result: TestCaseResponse):
    return result.model_dump_json(
        by_alias=True,
        indent=2
    )