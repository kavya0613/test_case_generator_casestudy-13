import streamlit as st

from backend.database import (
    save_test_cases,
    get_saved_test_cases,
    search_test_cases,
    delete_test_case,
)

from backend.gemini_service import generate_test_cases
from backend.prompt import build_user_prompt

from backend.validator import (
    validate_user_story,
    validate_test_cases,
)

from backend.duplicate_detector import find_duplicate_test_cases
from backend.coverage_analyzer import analyze_coverage

from backend.export_service import (
    test_cases_to_dataframe,
    export_to_csv,
    export_to_excel,
    export_to_json,
)


# ---------------------------------
# Page Configuration
# ---------------------------------

st.set_page_config(
    page_title="AI Test Case Generator",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------
# Professional UI Styling
# ---------------------------------

st.markdown(
    """
    <style>

    .stApp {
        background: #f5f7fb;
    }

    [data-testid="stAppViewContainer"] > .main {
        background: #f5f7fb;
    }

    .main .block-container {
        max-width: 1500px;
        padding: 1.4rem 2.2rem 3rem 2.2rem;
    }

    [data-testid="stSidebar"] {
        background: #111827;
        border-right: 1px solid #1f2937;
    }

    [data-testid="stSidebar"] * {
        color: #e5e7eb;
    }

    [data-testid="stSidebar"] .stRadio label {
        padding: 0.35rem 0;
    }

    .brand {
        padding: 0.4rem 0.2rem 1.2rem 0.2rem;
    }

    .brand-title {
        font-size: 1.15rem;
        font-weight: 750;
        color: white;
        letter-spacing: -0.02em;
    }

    .brand-subtitle {
        font-size: 0.78rem;
        color: #9ca3af;
        margin-top: 0.25rem;
        line-height: 1.4;
    }

    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        background: #ecfdf5;
        color: #047857;
        border: 1px solid #a7f3d0;
        border-radius: 999px;
        padding: 0.28rem 0.65rem;
        font-size: 0.76rem;
        font-weight: 650;
    }

    .hero {
        background: linear-gradient(135deg, #111827 0%, #1e3a8a 100%);
        border-radius: 20px;
        padding: 1.6rem 1.8rem;
        color: white;
        margin-bottom: 1.2rem;
        box-shadow: 0 10px 28px rgba(15, 23, 42, 0.13);
    }

    .hero h1 {
        color: white;
        font-size: 2rem;
        margin: 0;
        letter-spacing: -0.03em;
    }

    .hero p {
        color: #dbeafe;
        margin: 0.45rem 0 0 0;
        font-size: 0.96rem;
    }

    .section-title {
        color: #111827;
        font-size: 1.18rem;
        font-weight: 750;
        margin: 0.3rem 0 0.8rem 0;
    }

    .metric-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        padding: 1rem 1.1rem;
        min-height: 100px;
        box-shadow: 0 5px 18px rgba(15, 23, 42, 0.045);
    }

    .metric-label {
        color: #6b7280;
        font-size: 0.78rem;
        font-weight: 600;
    }

    .metric-value {
        color: #111827;
        font-size: 1.55rem;
        font-weight: 800;
        margin-top: 0.25rem;
    }

    .metric-note {
        color: #6b7280;
        font-size: 0.73rem;
        margin-top: 0.15rem;
    }

    .panel {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        padding: 1.15rem 1.25rem;
        box-shadow: 0 5px 18px rgba(15, 23, 42, 0.035);
        margin-bottom: 1rem;
    }

    .case-header {
        background: #f8fafc;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 0.8rem 1rem;
        margin-bottom: 0.8rem;
    }

    .case-id {
        color: #2563eb;
        font-size: 0.78rem;
        font-weight: 750;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .case-title {
        color: #111827;
        font-size: 1.05rem;
        font-weight: 750;
        margin-top: 0.2rem;
    }

    .small-muted {
        color: #6b7280;
        font-size: 0.82rem;
    }

    .tag {
        display: inline-block;
        padding: 0.2rem 0.55rem;
        border-radius: 999px;
        background: #eff6ff;
        color: #1d4ed8;
        font-size: 0.72rem;
        font-weight: 650;
        margin-right: 0.35rem;
    }

    textarea {
        border-radius: 14px !important;
        border: 1px solid #d1d5db !important;
        background: white !important;
        font-size: 0.96rem !important;
        padding: 0.85rem !important;
    }

    textarea:focus {
        border-color: #2563eb !important;
        box-shadow: 0 0 0 1px #2563eb !important;
    }

    .stButton > button,
    .stDownloadButton > button {
        border-radius: 10px !important;
        font-weight: 700 !important;
        min-height: 2.55rem !important;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover {
        border-color: #2563eb !important;
    }

    [data-testid="stDataFrame"] {
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        overflow: hidden;
    }

    [data-testid="stMetric"] {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        padding: 0.9rem;
    }

    [data-testid="stAlert"] {
        border-radius: 11px;
    }

    .footer {
        text-align: center;
        color: #9ca3af;
        font-size: 0.74rem;
        padding: 1.5rem 0 0.5rem 0;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------
# Session State
# ---------------------------------

if "result" not in st.session_state:
    st.session_state.result = None

if "user_story" not in st.session_state:
    st.session_state.user_story = ""

if "page" not in st.session_state:
    st.session_state.page = "Generate"

if "delete_message" not in st.session_state:
    st.session_state.delete_message = None


# ---------------------------------
# Sidebar Navigation
# ---------------------------------

with st.sidebar:
    st.markdown(
        """
        <div class="brand">
            <div class="brand-title">🧪 AI QA Studio</div>
            <div class="brand-subtitle">Intelligent test case generation and quality analysis</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    page = st.radio(
        "Navigation",
        ["Generate", "Results", "Saved Cases", "Manage Test Case", "About"],
        index=[
            "Generate",
            "Results",
            "Saved Cases",
            "Manage Test Case",
            "About",
        ].index(
            st.session_state.page
        ),
        label_visibility="collapsed",
    )

    st.session_state.page = page

    st.markdown("---")

    st.markdown(
        '<span class="status-pill">● Gemini AI connected</span>',
        unsafe_allow_html=True,
    )

    st.caption("AI-powered QA assistant")


# ---------------------------------
# Helper Functions
# ---------------------------------

def metric_card(label, value, note=""):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def display_case(test_case):
    st.markdown(
        f"""
        <div class="case-header">
            <div class="case-id">{test_case.test_case_id}</div>
            <div class="case-title">{test_case.title}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    info1, info2, info3 = st.columns(3)

    with info1:
        st.markdown("**Priority**")
        st.write(test_case.priority)

    with info2:
        st.markdown("**Test Type**")
        st.write(test_case.test_type)

    with info3:
        st.markdown("**Requirement Mapping**")
        st.write(test_case.requirement_mapping or "Not specified")

    details_left, details_right = st.columns(2)

    with details_left:
        st.markdown("**Preconditions**")

        if test_case.preconditions:
            for condition in test_case.preconditions:
                st.write(f"• {condition}")
        else:
            st.write("Not specified")

        st.markdown("**Test Data**")
        st.write(test_case.test_data or "Not specified by the requirement")

    with details_right:
        st.markdown("**Test Steps**")

        if test_case.test_steps:
            for index, step in enumerate(test_case.test_steps, start=1):
                st.write(f"{index}. {step}")
        else:
            st.write("Not specified")

        st.markdown("**Expected Result**")
        st.write(test_case.expected_result)


def display_results(result, user_story):
    if result is None:
        st.info("No generated results yet. Go to Generate and enter a user story.")
        return

    validation_errors = validate_test_cases(result)
    duplicates = find_duplicate_test_cases(result)
    coverage = analyze_coverage(result, user_story)

    # Summary cards
    total = coverage["total_test_cases"]
    coverage_percent = coverage["coverage_percentage"]
    validation_status = "Passed" if not validation_errors else "Issues"
    duplicate_status = "None" if not duplicates else str(len(duplicates))

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        metric_card("Test Cases", total, "Generated from user story")

    with c2:
        metric_card("Coverage", f"{coverage_percent}%", "Applicable scenarios")

    with c3:
        metric_card("Validation", validation_status, "Schema and quality checks")

    with c4:
        metric_card("Duplicates", duplicate_status, "Duplicate cases detected")

    st.markdown(
        "<div style='height: 0.8rem'></div>",
        unsafe_allow_html=True,
    )

    tabs = st.tabs(["Test Cases", "Coverage & Quality", "Export"])

    with tabs[0]:
        if not result.test_cases:
            st.warning("No test cases were generated.")
        else:
            for test_case in result.test_cases:
                with st.container(border=True):
                    display_case(test_case)

    with tabs[1]:
        left, right = st.columns(2)

        with left:
            st.markdown(
                '<div class="section-title">Validation</div>',
                unsafe_allow_html=True,
            )

            if not validation_errors:
                st.success("All generated test cases passed validation.")
            else:
                st.error("Validation errors found.")
                for error in validation_errors:
                    st.write(f"• {error}")

            st.markdown(
                '<div class="section-title">Duplicate Detection</div>',
                unsafe_allow_html=True,
            )

            if not duplicates:
                st.success("No duplicate test cases found.")
            else:
                st.warning("Duplicate test cases found.")
                for duplicate in duplicates:
                    st.write(f"• {duplicate}")

        with right:
            st.markdown(
                '<div class="section-title">Scenario Coverage</div>',
                unsafe_allow_html=True,
            )

            if coverage["covered_scenarios"]:
                st.markdown("**Covered**")

                for scenario in coverage["covered_scenarios"]:
                    st.write(f"✓ {scenario}")

            if coverage["missing_scenarios"]:
                st.markdown("**Missing**")

                for scenario in coverage["missing_scenarios"]:
                    st.write(f"⚠ {scenario}")
            else:
                st.success("All applicable scenarios are covered.")

        st.markdown("**User Story**")
        st.info(user_story)

    with tabs[2]:
        dataframe = test_cases_to_dataframe(result)
        csv_data = export_to_csv(result)
        json_data = export_to_json(result)

        excel_file = export_to_excel(result)

        with open(excel_file, "rb") as file:
            excel_data = file.read()

        e1, e2, e3 = st.columns(3)

        with e1:
            st.download_button(
                "⬇️ CSV",
                data=csv_data,
                file_name="test_cases.csv",
                mime="text/csv",
                use_container_width=True,
            )

        with e2:
            st.download_button(
                "⬇️ Excel",
                data=excel_data,
                file_name="test_cases.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )

        with e3:
            st.download_button(
                "⬇️ JSON",
                data=json_data,
                file_name="test_cases.json",
                mime="application/json",
                use_container_width=True,
            )

        st.markdown("**Structured Test Case Data**")
        st.dataframe(
            dataframe,
            use_container_width=True,
            hide_index=True,
        )


# ---------------------------------
# Generate Page
# ---------------------------------

def render_generate_page():
    st.markdown(
        """
        <div class="hero">
            <h1>AI Test Case Generator</h1>
            <p>Transform natural-language user stories into structured, traceable software test cases.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns([2.2, 1], gap="large")

    with left:
        st.markdown(
            '<div class="section-title">Describe your user story</div>',
            unsafe_allow_html=True,
        )

        user_story = st.text_area(
            "User Story",
            value=st.session_state.user_story,
            placeholder=(
                "Example: As a registered user, I want to reset my password "
                "using my registered email so that I can regain access to my account."
            ),
            height=190,
            label_visibility="collapsed",
        )

        generate_clicked = st.button(
            "✨ Generate Test Cases",
            type="primary",
            use_container_width=True,
        )

        if generate_clicked:
            if not user_story.strip():
                st.warning("Please enter a user story.")
            else:
                story_errors = validate_user_story(user_story)

                if story_errors:
                    for error in story_errors:
                        st.warning(f"⚠️ {error}")
                else:
                    st.session_state.user_story = user_story

                    with st.spinner("Generating test cases with Gemini AI..."):
                        prompt = build_user_prompt(user_story)
                        result = generate_test_cases(prompt)
                        st.session_state.result = result
                        save_test_cases(result)

                    st.success("Test cases generated and saved successfully.")

                    st.session_state.page = "Results"
                    st.rerun()

    with right:
        st.markdown(
            '<div class="section-title">What the system checks</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="panel">
                <div class="tag">Positive</div>
                <div class="tag">Negative</div>
                <div class="tag">Validation</div>
                <div class="tag">Boundary</div>
                <div class="tag">Edge</div>
                <br><br>
                <div class="small-muted">
                    Generates meaningful scenarios while validating structure,
                    duplicate cases and requirement coverage.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="panel">
                <strong>Output includes</strong>
                <div class="small-muted" style="margin-top:0.5rem; line-height:1.8;">
                    Test Case ID<br>
                    Preconditions & Test Data<br>
                    Test Steps & Expected Result<br>
                    Priority & Test Type<br>
                    Requirement Mapping
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if st.session_state.result is not None:
        st.markdown(
            "<div style='height: 0.4rem'></div>",
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="section-title">Latest generation</div>',
            unsafe_allow_html=True,
        )

        result = st.session_state.result
        coverage = analyze_coverage(result, st.session_state.user_story)

        a, b, c = st.columns(3)

        with a:
            metric_card(
                "Latest Cases",
                len(result.test_cases),
                "Generated successfully",
            )

        with b:
            metric_card(
                "Coverage",
                f"{coverage['coverage_percentage']}%",
                "Requirement scenarios",
            )

        with c:
            metric_card(
                "Status",
                "Ready",
                "Open Results from the sidebar",
            )


# ---------------------------------
# Results Page
# ---------------------------------

def render_results_page():
    st.markdown(
        """
        <div class="hero">
            <h1>Generation Results</h1>
            <p>Review test cases, quality checks, coverage and export options.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state.result is None:
        st.info(
            "No results available yet. Go to Generate and create test cases first."
        )
        return

    display_results(
        st.session_state.result,
        st.session_state.user_story,
    )


# ---------------------------------
# Saved Cases Page
# ---------------------------------

def render_saved_cases_page():
    st.markdown(
        """
        <div class="hero">
            <h1>Saved Test Cases</h1>
            <p>Search and review generated test cases stored in SQLite.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state.delete_message:
        st.success(st.session_state.delete_message)
        st.session_state.delete_message = None

    search_text = st.text_input(
        "Search",
        placeholder="Search by Test Case ID or title, e.g. TC021 or Login",
    )

    if search_text.strip():
        saved_test_cases = search_test_cases(search_text.strip())
    else:
        saved_test_cases = get_saved_test_cases()

    if not saved_test_cases:
        st.info("No matching test cases found.")
        return

    st.markdown(
        f"<div class='small-muted'>{len(saved_test_cases)} saved test case(s)</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "<div style='height:0.5rem'></div>",
        unsafe_allow_html=True,
    )

    dataframe = test_cases_to_dataframe_from_saved(saved_test_cases)

    st.dataframe(
        dataframe,
        use_container_width=True,
        hide_index=True,
    )
# ---------------------------------
# Manage Test Case Page
# ---------------------------------

def render_manage_test_case_page():

    st.markdown(
        """
        <div class="hero">
            <h1>Manage a Test Case</h1>
            <p>
                Select a saved test case to review or remove it from the database.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state.delete_message:
        st.success(st.session_state.delete_message)
        st.session_state.delete_message = None

    search_text = st.text_input(
        "Search Test Cases",
        placeholder="Search by Test Case ID or title",
    )

    if search_text.strip():
        saved_test_cases = search_test_cases(search_text.strip())
    else:
        saved_test_cases = get_saved_test_cases()

    if not saved_test_cases:
        st.info("No saved test cases found.")
        return

    test_case_ids = [
        case["test_case_id"]
        for case in saved_test_cases
    ]

    selected_test_case = st.selectbox(
        "Select a test case",
        test_case_ids,
    )

    selected_case = next(
        case
        for case in saved_test_cases
        if case["test_case_id"] == selected_test_case
    )

    left, right = st.columns(2)

    # -------------------------
    # LEFT - TEST CASE DETAILS
    # -------------------------
    with left:

        st.markdown(
            '<div class="section-title">Test Case Details</div>',
            unsafe_allow_html=True,
        )

        with st.container(border=True):

            st.markdown(
                f"**Test Case ID:** {selected_case['test_case_id']}"
            )

            st.markdown(
                f"**Title:** {selected_case['title']}"
            )

            st.markdown(
                f"**Priority:** {selected_case['priority']}"
            )

            st.markdown(
                f"**Test Type:** {selected_case['test_type']}"
            )

            st.markdown(
                f"**Created At:** {selected_case['created_at']}"
            )

    # -------------------------
    # RIGHT - EXPECTED RESULT
    # -------------------------
    with right:

        st.markdown(
            '<div class="section-title">Expected Result</div>',
            unsafe_allow_html=True,
        )

        with st.container(border=True):

            st.write(
                selected_case["expected_result"]
            )

    # -------------------------
    # MANAGE
    # -------------------------
    st.markdown(
        '<div class="section-title">Manage</div>',
        unsafe_allow_html=True,
    )

    if st.button(
        "Delete Selected Test Case",
        type="secondary",
    ):

        deleted_count = delete_test_case(
            selected_test_case
        )

        if deleted_count > 0:

            st.session_state.delete_message = (
                f"{selected_test_case} deleted successfully."
            )

            st.rerun()

        else:

            st.error(
                "Test case could not be deleted."
            )

def test_cases_to_dataframe_from_saved(saved_test_cases):
    import pandas as pd

    rows = []

    for test_case in saved_test_cases:
        rows.append(
            {
                "Test Case ID": test_case["test_case_id"],
                "Title": test_case["title"],
                "Priority": test_case["priority"],
                "Test Type": test_case["test_type"],
                "Test Data": test_case["test_data"] or "",
                "Expected Result": test_case["expected_result"],
                "Created At": test_case["created_at"],
            }
        )

    return pd.DataFrame(rows)


# ---------------------------------
# About Page
# ---------------------------------

def render_about_page():
    st.markdown(
        """
        <div class="hero">
            <h1>About AI QA Studio</h1>
            <p>An AI-assisted platform for generating structured software test cases from user requirements.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)

    with c1:
        st.markdown(
            """
            <div class="panel">
                <div class="section-title">Technology Stack</div>
                <div class="small-muted" style="line-height:2;">
                    <b>Frontend:</b> Streamlit<br>
                    <b>Backend:</b> Python / FastAPI components<br>
                    <b>AI:</b> Google Gemini<br>
                    <b>Validation:</b> Pydantic + rule-based checks<br>
                    <b>Database:</b> SQLite<br>
                    <b>Exports:</b> CSV, Excel, JSON
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            """
            <div class="panel">
                <div class="section-title">Quality Controls</div>
                <div class="small-muted" style="line-height:2;">
                    ✓ Structured output validation<br>
                    ✓ Duplicate test detection<br>
                    ✓ Requirement coverage analysis<br>
                    ✓ Positive and negative scenarios<br>
                    ✓ Boundary and validation scenarios<br>
                    ✓ Requirement traceability
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ---------------------------------
# Render Selected Page
# ---------------------------------

if page == "Generate":
    render_generate_page()

elif page == "Results":
    render_results_page()

elif page == "Saved Cases":
    render_saved_cases_page()

elif page == "Manage Test Case":
    render_manage_test_case_page()

else:
    render_about_page()


st.markdown(
    '<div class="footer">AI QA Studio • AI Test Case Generator • Gemini-powered quality engineering assistant</div>',
    unsafe_allow_html=True,
)