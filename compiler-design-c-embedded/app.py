import streamlit as st
import subprocess
import os

st.title("Custom C++ Compiler")

st.subheader("Write C++ Code")

code = st.text_area("Code Editor", height=300)

if st.button("Run Compiler"):

    if not os.path.exists("compiler.exe"):
        st.error("compiler.exe not found. Please make sure it is in this folder.")
    
    elif code.strip() == "":
        st.warning("Please enter some code")

    else:
        with open("temp.cpp", "w") as f:
            f.write(code)

        # delete old assembly file
        if os.path.exists("compile.txt"):
            os.remove("compile.txt")

        try:
            result = subprocess.run(
                ["./compiler.exe", "temp.cpp"],
                capture_output=True,
                text=True
            )

            output = result.stdout
            errors = result.stderr

            st.subheader("Compiler Output")
            st.code(output if output else "No output")

            # detect error in compiler output
            error_keywords = ["error","invalid","syntax","semantic","lexical","brace","incompatible"]

            error_detected = any(word in output.lower() for word in error_keywords)

            # only show assembly if no error
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