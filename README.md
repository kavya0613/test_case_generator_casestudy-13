Great. Let's make the README professional and suitable for your GitHub case study.

### Step 17

Open your README file:

```cmd
notepad README.md
```

Delete everything currently inside it and paste this complete content:

```markdown
# AI Test Case Generator from User Stories

## Overview

AI Test Case Generator is a GenAI-based application that automatically generates structured software test cases from natural-language user stories.

The application helps QA teams reduce the manual effort involved in creating test cases and improves consistency, requirement coverage, and test-case quality.

The system accepts a user story as input and generates test cases covering applicable scenarios such as:

- Positive scenarios
- Negative scenarios
- Validation scenarios
- Boundary scenarios
- Edge cases
- Error-handling scenarios

Each generated test case contains structured information including:

- Test Case ID
- Title
- Preconditions
- Test Data
- Test Steps
- Expected Result
- Priority
- Test Type
- Requirement Mapping

## Problem Statement

Creating test cases manually from requirements can be time-consuming and may result in:

- Missing test scenarios
- Inconsistent test-case formats
- Duplicate test cases
- Incomplete requirement coverage
- Missing validation and boundary scenarios
- Increased manual effort
- Delays in the testing process

## Proposed Solution

This project uses Generative AI to convert natural-language user stories into structured software test cases.

The application combines AI-based test-case generation with rule-based validation, duplicate detection, and coverage analysis.

## Key Features

### 1. AI-Based Test Case Generation

Generates structured test cases from a natural-language user story using Google Gemini.

### 2. Scenario Coverage

Generates applicable scenarios including:

- Positive
- Negative
- Validation
- Boundary
- Edge
- Error Handling

### 3. Rule-Based Validation

Validates:

- Empty user stories
- Very short requirements
- Missing Test Case IDs
- Missing titles
- Missing test steps
- Missing expected results
- Invalid priorities
- Missing test types
- Missing requirement mapping

### 4. Duplicate Detection

Identifies duplicate test cases based on normalized:

- Titles
- Test steps
- Expected results
- Test data

### 5. Coverage Analysis

Analyzes whether the generated test cases cover the scenario types applicable to the user story.

### 6. Test Case Management

Generated test cases can be saved in a SQLite database and searched using:

- Test Case ID
- Test Case Title

### 7. Export

Test cases can be exported to:

- JSON
- CSV
- Excel

### 8. Web Interface

The application provides a Streamlit interface with pages for:

- Generate
- Results
- Saved Cases
- Manage Test Case
- About

## Example User Story

```text
As a registered user, I want to reset my password using my registered email address.
```

The application analyzes the requirement and generates relevant test cases based on the supported scenarios.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application development |
| Streamlit | Web user interface |
| Google Gemini | Generative AI |
| Pydantic | Data validation and structured schemas |
| SQLite | Test-case persistence |
| Pandas | Data processing and exports |
| OpenPyXL | Excel export |
| FastAPI | Backend API |
| Uvicorn | API server |
| python-dotenv | Environment variable management |
| Pytest | Testing |

## Project Architecture

```text
User Story
    |
    v
Streamlit UI
    |
    v
Input Validation
    |
    v
Prompt Builder
    |
    v
Google Gemini
    |
    v
Structured Test Cases
    |
    +----------------------+
    |                      |
    v                      v
Validation           Duplicate Detection
    |                      |
    +----------+-----------+
               |
               v
       Coverage Analysis
               |
               v
        Results / Storage
          |           |
          v           v
       SQLite      Export
                  JSON/CSV/Excel
```

## Project Structure

```text
test_case_generator/
│
├── app.py
├── app_backup.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env
│
├── .streamlit/
│   └── config.toml
│
├── backend/
│   ├── main.py
│   ├── schemas.py
│   ├── gemini_service.py
│   ├── prompt.py
│   ├── validator.py
│   ├── duplicate_detector.py
│   ├── coverage_analyzer.py
│   ├── database.py
│   └── export_service.py
│
├── data/
│   └── test_cases.db
│
└── tests/
    ├── test_validation.py
    └── test_generation.py
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/kavya0613/test_case_generator_casestudy-13.git
```

### 2. Navigate to the project

```bash
cd test_case_generator_casestudy-13
```

### 3. Create a virtual environment

Windows:

```cmd
python -m venv venv
```

Activate it:

```cmd
venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

The `.env` file is excluded from Git using `.gitignore`.

## Run the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will open in your browser.

## Run Tests

Run the test suite using:

```bash
python -m pytest -q
```

## API

The project also includes a FastAPI backend.

Start the API using:

```bash
uvicorn backend.main:app --reload
```

The API provides:

```text
GET  /
POST /generate
```

The `/generate` endpoint accepts a user story and returns:

- Generated test cases
- Validation results
- Duplicate information
- Coverage information

## Quality Controls

The application includes several controls to improve generated test-case quality:

- Input validation
- Structured output validation
- Duplicate detection
- Requirement mapping
- Coverage analysis
- Priority validation
- Scenario detection
- Output schema validation

## Safety Considerations

The system is designed as a test-case generation assistant rather than an automatic test executor.

Important considerations include:

- No automatic execution of generated test steps
- API keys stored using environment variables
- Input length restrictions
- Structured output validation
- Human review of generated test cases
- Protection against unsupported business-rule assumptions

## Future Enhancements

Planned improvements include:

- Jira integration
- Azure DevOps integration
- TestRail integration
- ServiceNow integration
- PDF and Word requirement uploads
- Automated Selenium script generation
- API test-script generation
- Risk-based test prioritization
- Domain-specific QA knowledge bases
- Historical defect-data integration
- Requirement change detection
- Multilingual test-case generation
- Human feedback-based improvement
- Multi-agent QA workflows

## Author

**Kavya Adepu**

B.Tech - Computer Science and Engineering

## GitHub Repository

https://github.com/kavya0613/test_case_generator_casestudy-13
```



