import sqlite3
from pathlib import Path


DATABASE_PATH = Path("data/test_cases.db")


def get_connection():
    DATABASE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    connection.row_factory = sqlite3.Row

    return connection


def create_tables():
    connection = get_connection()

    cursor = connection.cursor()

    # ---------------------------------
    # Test Cases Table
    # ---------------------------------

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS test_cases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            test_case_id TEXT NOT NULL,
            title TEXT NOT NULL,
            preconditions TEXT,
            test_data TEXT,
            test_steps TEXT,
            expected_result TEXT NOT NULL,
            priority TEXT,
            test_type TEXT,
            requirement_mapping TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    # ---------------------------------
    # Permanent Test Case ID Counter
    # ---------------------------------

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS test_case_counter (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            last_number INTEGER NOT NULL
        )
        """
    )

    # Current database already contains
    # test cases up to TC018.
    #
    # The counter must NOT decrease when
    # a test case is deleted.

    cursor.execute(
        """
        INSERT OR IGNORE INTO test_case_counter (
            id,
            last_number
        )
        VALUES (1, 18)
        """
    )

    # ---------------------------------
    # Fix Old Test Case Priorities
    # ---------------------------------
    #
    # Older test cases may contain:
    # "Not specified by the requirement"
    #
    # New rule:
    # Unspecified priority = Medium

    cursor.execute(
        """
        UPDATE test_cases
        SET priority = 'Medium'
        WHERE priority IS NULL
           OR TRIM(priority) = ''
           OR priority = 'Not specified by the requirement'
        """
    )

    connection.commit()

    connection.close()


# ---------------------------------
# Save Test Cases
# ---------------------------------

def save_test_cases(result):

    connection = get_connection()
    cursor = connection.cursor()

    # Get the permanent counter value
    cursor.execute(
        """
        SELECT last_number
        FROM test_case_counter
        WHERE id = 1
        """
    )

    row = cursor.fetchone()

    if row is None:

        last_number = 0

        cursor.execute(
            """
            INSERT INTO test_case_counter (
                id,
                last_number
            )
            VALUES (1, 0)
            """
        )

    else:

        last_number = row["last_number"]

    # ---------------------------------
    # Generate new unique IDs
    # ---------------------------------

    for test_case in result.test_cases:

        last_number += 1

        test_case.test_case_id = (
            f"TC{last_number:03d}"
        )

        cursor.execute(
            """
            INSERT INTO test_cases (
                test_case_id,
                title,
                preconditions,
                test_data,
                test_steps,
                expected_result,
                priority,
                test_type,
                requirement_mapping
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                test_case.test_case_id,
                test_case.title,
                "\n".join(
                    test_case.preconditions
                ),
                test_case.test_data or "",
                "\n".join(
                    test_case.test_steps
                ),
                test_case.expected_result,
                test_case.priority,
                test_case.test_type,
                test_case.requirement_mapping or "",
            )
        )

    # ---------------------------------
    # Save the latest counter value
    # ---------------------------------

    cursor.execute(
        """
        UPDATE test_case_counter
        SET last_number = ?
        WHERE id = 1
        """,
        (last_number,)
    )

    connection.commit()

    connection.close()


# ---------------------------------
# Get Saved Test Cases
# ---------------------------------

def get_saved_test_cases():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            test_case_id,
            title,
            preconditions,
            test_data,
            test_steps,
            expected_result,
            priority,
            test_type,
            requirement_mapping,
            created_at
        FROM test_cases
        ORDER BY id DESC
        """
    )

    rows = cursor.fetchall()

    connection.close()

    return [
        dict(row)
        for row in rows
    ]


# ---------------------------------
# Search Test Cases
# ---------------------------------

def search_test_cases(search_text):

    connection = get_connection()
    cursor = connection.cursor()

    search_pattern = f"%{search_text}%"

    cursor.execute(
        """
        SELECT
            test_case_id,
            title,
            preconditions,
            test_data,
            test_steps,
            expected_result,
            priority,
            test_type,
            requirement_mapping,
            created_at
        FROM test_cases
        WHERE test_case_id LIKE ?
           OR title LIKE ?
        ORDER BY id DESC
        """,
        (
            search_pattern,
            search_pattern,
        )
    )

    rows = cursor.fetchall()

    connection.close()

    return [
        dict(row)
        for row in rows
    ]


# ---------------------------------
# Delete Test Case
# ---------------------------------

def delete_test_case(test_case_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM test_cases
        WHERE test_case_id = ?
        """,
        (test_case_id,)
    )

    deleted_count = cursor.rowcount

    connection.commit()

    connection.close()

    return deleted_count


# ---------------------------------
# Fix Existing Test Case IDs
# ---------------------------------

def fix_existing_test_case_ids():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, test_case_id
        FROM test_cases
        ORDER BY id ASC
        """
    )

    rows = cursor.fetchall()

    for number, row in enumerate(
        rows,
        start=1
    ):

        new_id = f"TC{number:03d}"

        cursor.execute(
            """
            UPDATE test_cases
            SET test_case_id = ?
            WHERE id = ?
            """,
            (
                new_id,
                row["id"]
            )
        )

    # Make sure the permanent counter is
    # at least as high as the existing IDs.

    highest_number = len(rows)

    cursor.execute(
        """
        UPDATE test_case_counter
        SET last_number = ?
        WHERE id = 1
        AND last_number < ?
        """,
        (
            highest_number,
            highest_number
        )
    )

    connection.commit()

    connection.close()


# ---------------------------------
# Create Tables Automatically
# ---------------------------------

create_tables()