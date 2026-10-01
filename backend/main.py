from fastapi import FastAPI
from pydantic import BaseModel

from backend.gemini_service import generate_test_cases
from backend.prompt import build_user_prompt
from backend.validator import validate_test_cases
from backend.duplicate_detector import find_duplicate_test_cases
from backend.coverage_analyzer import analyze_coverage


app = FastAPI(
    title="AI Test Case Generator API",
    version="1.0.0"
)


class UserStoryRequest(BaseModel):
    user_story: str


@app.get("/")
def home():
    return {
        "message": "AI Test Case Generator API is running"
    }


@app.post("/generate")
def generate(request: UserStoryRequest):

    user_story = request.user_story.strip()

    if not user_story:
        return {
            "success": False,
            "errors": ["User story cannot be empty."]
        }

    prompt = build_user_prompt(user_story)

    result = generate_test_cases(prompt)

    validation_errors = validate_test_cases(result)

    duplicates = find_duplicate_test_cases(result)

    coverage = analyze_coverage(
        result,
        user_story
    )

    return {
        "success": len(validation_errors) == 0,
        "test_cases": result.model_dump(
            by_alias=True
        )["testCases"],
        "validation_errors": validation_errors,
        "duplicates": duplicates,
        "coverage": coverage
    }