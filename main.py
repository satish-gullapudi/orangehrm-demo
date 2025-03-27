import streamlit as st
import os
import subprocess
import re
from threading import Thread
import time

# Global flag for cancellation
execution_flag = {"cancel": False}

def discover_test_functions(folder_path):
    """Discover all test functions within test files in the specified folder."""
    test_list = []  # List of test cases in the format "file_name::function_name"
    
    for file in os.listdir(folder_path):
        if file.startswith("test_") and file.endswith(".py"):
            filepath = os.path.join(folder_path, file)
            with open(filepath, "r") as f:
                content = f.read()
            
            # Use regex to find all test functions in the file
            test_functions = re.findall(r"def (test_\w+)", content)
            for func in test_functions:
                test_list.append(f"{file}::{func}")
    
    return test_list

def run_selected_tests(selected_tests):
    """Run selected test functions and check for cancellation."""
    for test in selected_tests:
        if execution_flag["cancel"]:
            st.warning("Execution canceled!")
            return
        command = ["pytest", "-v", "-s", f"TestCases/{test}"]
        result = subprocess.run(command, capture_output=True, text=True)
        st.text(f"Running {test}...\n{result.stdout}")
        time.sleep(0.5)  # Simulate delay to make cancellation observable

# def execute_tests(selected_tests):
#     """Threaded function to execute tests."""
#     execution_flag["cancel"] = False  # Reset cancel flag
#     run_selected_tests(selected_tests)

def execute_tests(selected_tests):
    """Executes the selected tests and signals completion."""
    try:
        # Simulate running tests (replace with your actual test execution logic)
        # for test in selected_tests:
        #     st.write(f"Running test: {test}")  # Display each test being run
        #     time.sleep(1)  # Simulate test execution time
        run_selected_tests(selected_tests)

        st.session_state.test_execution_complete = True # Signal completion using session state
    except Exception as e:
        st.error(f"An error occurred during test execution: {e}")
        st.session_state.test_execution_complete = True # Still set to true to avoid indefinite hang

if "test_execution_complete" not in st.session_state:
    st.session_state.test_execution_complete = False

# Streamlit UI
st.title("Test Automation Runner")
st.write("Select the specific test cases you want to run:")

# Discover test functions
test_folder = "TestCases"
test_cases = discover_test_functions(test_folder)

# Create checkboxes for each test case
selected_tests = []
if test_cases:
    for test in test_cases:
        if st.checkbox(test):
            selected_tests.append(test)

# Add buttons
col1, col2 = st.columns(2)

# Start Execution Button
if col1.button("Run Selected Tests"):
    if selected_tests:
        st.write(f"Running {len(selected_tests)} test(s)...")
        st.session_state.test_execution_complete = False # Reset before starting new tests
        # Run tests in a separate thread
        Thread(target=execute_tests, args=(selected_tests,), daemon=True).start()
    else:
        st.warning("No tests selected!")

# Check for test completion periodically (using a placeholder for demonstration)
if st.session_state.test_execution_complete:
    st.success("Test execution complete!")
    del st.session_state.test_execution_complete # Clean up to allow running again

# Cancel Execution Button
if col2.button("Cancel Execution"):
    execution_flag["cancel"] = True
    st.warning("Test execution will stop shortly.")

