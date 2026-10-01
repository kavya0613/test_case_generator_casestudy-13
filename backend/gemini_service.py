import os
import json

from dotenv import load_dotenv
from google import genai
from google.genai import types

from backend.schemas import TestCaseResponse


load_dotenv()


api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set in the .env file")


client = genai.Client(api_key=api_key)


def generate_test_cases(user_prompt: str):

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=user_prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema={
                "type": "OBJECT",
                "properties": {
                    "test_cases": {
                        "type": "ARRAY",
                        "items": {
                            "type": "OBJECT",
                            "properties": {
                                "test_case_id": {
                                    "type": "STRING"
                                },
                                "title": {
                                    "type": "STRING"
                                },
                                "preconditions": {
                                    "type": "ARRAY",
                                    "items": {
                                        "type": "STRING"
                                    }
                                },
                                "test_data": {
                                    "type": "STRING"
                                },
                                "test_steps": {
                                    "type": "ARRAY",
                                    "items": {
                                        "type": "STRING"
                                    }
                                },
                                "expected_result": {
                                    "type": "STRING"
                                },
                                "priority": {
                                    "type": "STRING"
                                },
                                "test_type": {
                                    "type": "STRING"
                                },
                                "requirement_mapping": {
                                    "type": "STRING"
                                }
                            },
                            "required": [
                                "test_case_id",
                                "title",
                                "preconditions",
                                "test_data",
                                "test_steps",
                                "expected_result",
                                "priority",
                                "test_type",
                                "requirement_mapping"
                            ]
                        }
                    }
                },
                "required": [
                    "test_cases"
                ]
            }
        )
    )

    response_text = response.text.strip()

    data = json.loads(response_text)

    validated_data = TestCaseResponse.model_validate(data)

    return validated_data