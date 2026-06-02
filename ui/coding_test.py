# Coding Test Component - Simplified Version
import streamlit as st
import json
import re
import html

def render_coding_test(topic: str, difficulty: str, ask_groq_fn, session_id=None, save_message_fn=None):
    """Render coding test interface"""
    
    st.markdown("### 💻 Coding Test")
    
    # Initialize coding test state
    if "coding_problem" not in st.session_state:
        st.session_state.coding_problem = None
    if "coding_language" not in st.session_state:
        st.session_state.coding_language = "python"
    if "user_code" not in st.session_state:
        st.session_state.user_code = ""
    if "test_results" not in st.session_state:
        st.session_state.test_results = None
    if "coding_score" not in st.session_state:
        st.session_state.coding_score = 0
    if "coding_total" not in st.session_state:
        st.session_state.coding_total = 0
    
    # Language selector
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"**Topic:** {topic} | **Difficulty:** {difficulty}")
    with col2:
        lang_options = ["Python"]
        selected_lang = st.selectbox(
            "Language",
            lang_options,
            index=0,
            label_visibility="collapsed",
            key="lang_selector"
        )
        st.session_state.coding_language = selected_lang.lower()
    
    st.info("ℹ️ Currently only Python is supported for code execution and testing.")
    
    st.markdown("---")
    
    # Generate problem if not exists
    if not st.session_state.coding_problem:
        with st.spinner("🤖 Generating coding problem..."):
            try:
                prompt = f"""Generate a {difficulty} level {topic} coding problem for {selected_lang}.

Format your response EXACTLY as:

**Problem Title:** [Title]

**Description:**
[Clear problem description]

**Input Format:**
[Describe input format]

**Output Format:**
[Describe expected output]

**Example:**
Input: [example input]
Output: [example output]

**Constraints:**
[List constraints]

**Test Cases (JSON format):**
```json
[
  {{"input": "test input 1", "expected_output": "expected output 1"}},
  {{"input": "test input 2", "expected_output": "expected output 2"}},
  {{"input": "test input 3", "expected_output": "expected output 3"}}
]
```

Make it a practical {topic} problem suitable for {selected_lang}."""
                
                response = ask_groq_fn(
                    "You are an expert coding interview problem generator.",
                    [{"role": "user", "content": prompt}]
                )
                
                st.session_state.coding_problem = response
            except Exception as e:
                st.error(f"Error generating problem: {str(e)}")
                st.session_state.coding_problem = "Error generating problem. Please try again."
    
    # Display problem
    if st.session_state.coding_problem:
        with st.expander("📋 Problem Statement", expanded=True):
            st.markdown(st.session_state.coding_problem)
    
    st.markdown("### ✍️ Your Solution")
    
    # Default code templates
    default_code = {
        "python": "# Write your Python code here\n\ndef solution():\n    # Your code here\n    pass\n\nif __name__ == '__main__':\n    solution()",
        "java": "// Write your Java code here\n\npublic class Solution {\n    public static void main(String[] args) {\n        // Your code here\n    }\n}",
        "javascript": "// Write your JavaScript code here\n\nfunction solution() {\n    // Your code here\n}\n\nsolution();",
        "c++": "// Write your C++ code here\n\n#include <iostream>\nusing namespace std;\n\nint main() {\n    // Your code here\n    return 0;\n}",
        "sql": "-- Write your SQL query here\n\nSELECT * FROM table_name;"
    }
    
    # Code editor (simple text area)
    if not st.session_state.user_code:
        st.session_state.user_code = default_code.get(st.session_state.coding_language, "")
    
    user_code = st.text_area(
        "Code Editor",
        value=st.session_state.user_code,
        height=400,
        key="code_editor_area",
        label_visibility="collapsed"
    )
    
    # Decode HTML entities if present
    st.session_state.user_code = html.unescape(user_code)
    
    # Action buttons
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        if st.button("▶️ Run Code", use_container_width=True, key="run_btn"):
            if not st.session_state.user_code or st.session_state.user_code.strip() == "":
                st.error("❌ Please write some code first!")
            elif st.session_state.coding_language != "python":
                st.warning(f"⚠️ Only Python is supported for execution. {selected_lang} execution is not available.")
            else:
                with st.spinner("🔄 Running your code..."):
                    try:
                        from bot.code_executor import CodeExecutor
                        executor = CodeExecutor()
                        
                        result = executor.execute_code(
                            code=st.session_state.user_code,
                            language=st.session_state.coding_language,
                            stdin=""
                        )
                        
                        if result["success"]:
                            st.success("✅ Code executed successfully!")
                            if result["output"]:
                                st.code(result["output"], language="text")
                            else:
                                st.info("ℹ️ No output produced. Make sure your code prints something.")
                        else:
                            st.error("❌ Execution failed!")
                            st.code(result["error"], language="text")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
    
    with col2:
        if st.button("✅ Submit & Test", use_container_width=True, key="submit_btn"):
            if not st.session_state.user_code or st.session_state.user_code.strip() == "":
                st.error("❌ Please write some code first!")
            elif st.session_state.coding_language != "python":
                st.warning(f"⚠️ Only Python is supported for testing. {selected_lang} execution is not available.")
            else:
                with st.spinner("🧪 Running test cases..."):
                    try:
                        # Extract test cases from problem
                        json_match = re.search(r'```json\s*(\[.*?\])\s*```', st.session_state.coding_problem, re.DOTALL)
                        
                        if json_match:
                            test_cases = json.loads(json_match.group(1))
                        else:
                            test_cases = [{"input": "", "expected_output": ""}]
                        
                        from bot.code_executor import CodeExecutor
                        executor = CodeExecutor()
                        
                        results = executor.run_test_cases(
                            code=st.session_state.user_code,
                            language=st.session_state.coding_language,
                            test_cases=test_cases
                        )
                        
                        st.session_state.test_results = results
                        st.session_state.coding_total += 1
                        
                        # Save to database
                        if session_id and save_message_fn:
                            save_message_fn(session_id, "user", f"[CODE SUBMISSION]\n```python\n{st.session_state.user_code}\n```")
                            result_msg = f"Test Results: {results['passed']}/{results['total']} passed"
                            save_message_fn(session_id, "assistant", result_msg)
                        
                        if results["passed"] == results["total"]:
                            st.session_state.coding_score += 1
                            st.success(f"🎉 All test cases passed! ({results['passed']}/{results['total']})")
                        else:
                            st.warning(f"⚠️ Some test cases failed ({results['passed']}/{results['total']})")
                        
                        # Show results
                        for test_result in results["test_results"]:
                            if test_result["passed"]:
                                st.success(f"✅ Test Case {test_result['test_case']}: Passed")
                            else:
                                with st.expander(f"❌ Test Case {test_result['test_case']}: Failed", expanded=True):
                                    st.write(f"**Input:** `{test_result['input']}`")
                                    st.write(f"**Expected:** `{test_result['expected']}`")
                                    st.write(f"**Got:** `{test_result['actual']}`")
                                    if test_result["error"]:
                                        st.error(f"**Error:** {test_result['error']}")
                        
                    except Exception as e:
                        st.error(f"❌ Testing error: {str(e)}")
                        st.info("💡 Tip: Make sure your code prints the output correctly.")
    
    with col3:
        if st.button("🔄 New", use_container_width=True, key="new_btn"):
            st.session_state.coding_problem = None
            st.session_state.user_code = ""
            st.session_state.test_results = None
            st.rerun()
    
    # Show score
    if st.session_state.coding_total > 0:
        # Update session score
        if session_id:
            from database.db_manager import end_session
            end_session(session_id, st.session_state.coding_score, st.session_state.coding_total)
        
        st.markdown("---")
        accuracy = (st.session_state.coding_score / st.session_state.coding_total) * 100
        st.markdown(
            f"<div style='text-align:center; padding:1rem; background:linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius:10px;'>"
            f"<div style='color:#ffffff; font-size:0.9rem;'>Problems Solved</div>"
            f"<div style='color:#ffffff; font-size:2rem; font-weight:700;'>{st.session_state.coding_score}/{st.session_state.coding_total}</div>"
            f"<div style='color:rgba(255,255,255,0.8); font-size:0.85rem;'>Success Rate: {accuracy:.0f}%</div>"
            f"</div>",
            unsafe_allow_html=True
        )
