import streamlit as st
import subprocess
import os

st.title("Custom C++ Compiler")

st.subheader("Write C++ Code")

code = st.text_area("Code Editor", height=300)

if st.button("Run Compiler"):

    if code.strip() == "":
        st.warning("Please enter some code")

    else:
        # Build compiler if it does not exist
        if not os.path.exists("compiler"):
            build = subprocess.run(
                ["g++", "file_opener.cpp", "parser.cpp", "scanner.cpp", "semantics.cpp", "-o", "compiler"],
                capture_output=True,
                text=True
            )

            if build.returncode != 0:
                st.error("Failed to build compiler")
                st.code(build.stderr)
                st.stop()

        # Save user code
        with open("temp.cpp", "w") as f:
            f.write(code)

        # Remove old assembly output
        if os.path.exists("compile.txt"):
            os.remove("compile.txt")

        try:
            # Run compiler
            result = subprocess.run(
                ["compiler", "temp.cpp"],
                capture_output=True,
                text=True
            )

            output = result.stdout
            errors = result.stderr

            st.subheader("Compiler Error")
            st.code(output if output else "No Error")

            if errors:
                st.subheader("Errors")
                st.code(errors)

            # Detect compiler errors from output
            error_keywords = [
                "error", "invalid", "syntax", "semantic",
                "lexical", "brace", "incompatible"
            ]

            error_detected = any(word in output.lower() for word in error_keywords)

            # Show assembly only if no error
            if not error_detected and os.path.exists("compile.txt"):

                with open("compile.txt", "r") as f:
                    assembly = f.read()

                st.subheader("Generated Assembly Code")
                st.code(assembly)

            elif error_detected:
                st.warning("Compilation failed. Assembly code not generated.")

            else:
                st.warning("compile.txt not generated.")

        except Exception as e:
            st.error(f"Error running compiler: {e}")
