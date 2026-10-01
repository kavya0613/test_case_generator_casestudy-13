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

)





# ---------------------------------

# Session State

# ---------------------------------



if "result" not in st.session_state:

    st.session_state.result = None



if "user_story" not in st.session_state:

    st.session_state.user_story = ""





# ---------------------------------

# Helper Function

# ---------------------------------



def display_results(result, user_story):

    """

    Display validation, duplicate detection,

    coverage analysis, generated test cases,

    and export options.

    """



    validation_errors = validate_test_cases(result)



    duplicates = find_duplicate_test_cases(result)



    coverage = analyze_coverage(

        result,

        user_story,

    )



    # ---------------------------------

    # Validation Status

    # ---------------------------------



    st.subheader("Validation Status")



    if not validation_errors:

        st.success(

            "✅ All generated test cases passed validation."

        )

    else:

        st.error("❌ Validation errors found.")



        for error in validation_errors:

            st.write(f"- {error}")



    # ---------------------------------

    # Duplicate Detection

    # ---------------------------------



    st.subheader("Duplicate Detection")



    if not duplicates:

        st.success(

            "✅ No duplicate test cases found."

        )

    else:

        st.warning(

            "⚠️ Duplicate test cases found."

        )



        for duplicate in duplicates:

            st.write(f"- {duplicate}")



    # ---------------------------------

    # Coverage Analysis

    # ---------------------------------



    st.subheader("Coverage Analysis")



    col1, col2 = st.columns(2)



    with col1:

        st.metric(

            "Total Test Cases",

            coverage["total_test_cases"],

        )



    with col2:

        st.metric(

            "Coverage",

            f'{coverage["coverage_percentage"]}%',

        )



    # ---------------------------------

    # Covered Scenarios

    # ---------------------------------



    if coverage["covered_scenarios"]:

        st.write("**Covered Scenarios:**")



        for scenario in coverage["covered_scenarios"]:

            st.write(f"✅ {scenario}")



    # ---------------------------------

    # Missing Scenarios

    # ---------------------------------



    if coverage["missing_scenarios"]:

        st.write("**Missing Scenarios:**")



        for scenario in coverage["missing_scenarios"]:

            st.write(f"⚠️ {scenario}")



    # ---------------------------------

    # Generated Test Cases

    # ---------------------------------



    st.subheader("Generated Test Cases")



    if not result.test_cases:

        st.warning("No test cases were generated.")



    else:



        for test_case in result.test_cases:



            st.markdown(

                f"### {test_case.test_case_id} — "

                f"{test_case.title}"

            )



            st.write("**Preconditions:**")



            if test_case.preconditions:



                for condition in test_case.preconditions:

                    st.write(f"- {condition}")



            else:

                st.write("Not specified")



            st.write("**Test Data:**")



            st.write(

                test_case.test_data

                or "Not specified"

            )



            st.write("**Test Steps:**")



            if test_case.test_steps:



                for index, step in enumerate(

                    test_case.test_steps,

                    start=1,

                ):

                    st.write(

                        f"{index}. {step}"

                    )



            else:

                st.write("Not specified")



            st.write("**Expected Result:**")



            st.write(

                test_case.expected_result

            )



            st.write(

                "**Priority:**",

                test_case.priority,

            )



            st.write(

                "**Test Type:**",

                test_case.test_type,

            )



            st.write(

                "**Requirement Mapping:**",

                test_case.requirement_mapping

                or "Not specified",

            )



            st.divider()



    # ---------------------------------

    # Export Test Cases

    # ---------------------------------



    st.subheader("Export Test Cases")



    dataframe = test_cases_to_dataframe(result)



    # ---------------------------------

    # CSV Export

    # ---------------------------------



    csv_data = export_to_csv(result)



    st.download_button(

        label="⬇️ Download CSV",

        data=csv_data,

        file_name="test_cases.csv",

        mime="text/csv",

    )



    # ---------------------------------

    # Excel Export

    # ---------------------------------



    excel_file = export_to_excel(result)



    with open(excel_file, "rb") as file:

        excel_data = file.read()



    st.download_button(

        label="⬇️ Download Excel",

        data=excel_data,

        file_name="test_cases.xlsx",

        mime=(

            "application/vnd.openxmlformats-officedocument."

            "spreadsheetml.sheet"

        ),

    )



    # ---------------------------------

    # JSON Export

    # ---------------------------------



    json_data = export_to_json(result)



    st.download_button(

        label="⬇️ Download JSON",

        data=json_data,

        file_name="test_cases.json",

        mime="application/json",

    )



    # ---------------------------------

    # Data Table

    # ---------------------------------



    st.subheader("Test Case Table")



    st.dataframe(

        dataframe,

        use_container_width=True,

    )





# ---------------------------------

# Application Header

# ---------------------------------



st.title("🧪 AI Test Case Generator")



st.write(

    "Generate software test cases from user stories "

    "using Gemini AI."

)





# ---------------------------------

# User Story Input

# ---------------------------------



user_story = st.text_area(

    "Enter User Story",

    value=st.session_state.user_story,

    placeholder=(

        "Example: As a registered user, I want to reset "

        "my password using my registered email so that "

        "I can regain access to my account."

    ),

    height=180,

)





# ---------------------------------

# Generate Test Cases

# ---------------------------------



# ---------------------------------

# Generate Test Cases

# ---------------------------------



if st.button("Generate Test Cases"):



    if not user_story.strip():



        st.warning(

            "Please enter a user story."

        )



    else:



        story_errors = validate_user_story(

            user_story

        )



        if story_errors:



            for error in story_errors:

                st.warning(

                    f"⚠️ {error}"

                )



        else:



            st.session_state.user_story = user_story



            with st.spinner(

                "Generating test cases..."

            ):



                prompt = build_user_prompt(

                    user_story

                )



                result = generate_test_cases(

                    prompt

                )



                st.session_state.result = result



                # Save generated test cases

                # to SQLite database.

                save_test_cases(result)



            st.success(

                "Test cases generated successfully."

            )



            display_results(

                st.session_state.result,

                user_story,

            )





# ---------------------------------

# Display Previous Result

# ---------------------------------



elif st.session_state.result is not None:



    display_results(

        st.session_state.result,

        st.session_state.user_story,

    )



# ---------------------------------

# Saved Test Cases

# ---------------------------------



# ---------------------------------

# Saved Test Cases

# ---------------------------------



st.subheader("📚 Saved Test Cases")



if "delete_message" in st.session_state:



    st.success(

        st.session_state.delete_message

    )



    del st.session_state.delete_message



search_text = st.text_input(

    "🔍 Search by Test Case ID or Title",

    placeholder="Example: TC_LOGIN_001 or Login",

)



if search_text.strip():



    saved_test_cases = search_test_cases(

        search_text.strip()

    )



else:



    saved_test_cases = get_saved_test_cases()





if not saved_test_cases:



    st.info("No matching test cases found.")



else:



    st.dataframe(

        saved_test_cases,

        use_container_width=True,

    )



    st.subheader("🗑️ Delete Test Case")



    test_case_ids = [

        test_case["test_case_id"]

        for test_case in saved_test_cases

    ]



    selected_test_case = st.selectbox(

        "Select a test case to delete",

        test_case_ids,

    )



    if st.button("Delete Selected Test Case"):

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