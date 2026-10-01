from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any


class TestCase(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    test_case_id: str = Field(alias="testCaseId")
    title: str

    preconditions: List[str] = Field(default_factory=list)

    test_data: Optional[str] = Field(
        default=None,
        alias="testData"
    )

    test_steps: List[str] = Field(
        default_factory=list,
        alias="testSteps"
    )

    expected_result: str = Field(alias="expectedResult")

    priority: str = "Medium"

    test_type: str = Field(
        default="Functional",
        alias="testType"
    )

    requirement_mapping: Optional[str] = Field(
        default=None,
        alias="requirementMapping"
    )


class TestCaseResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    test_cases: List[TestCase] = Field(alias="testCases")