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
        # save code inside the project folder
        source_file = "compiler-design-c-embedded/temp.cpp"

        with open(source_file, "w") as f:
            f.write(code)

        # build compiler if not exists
        if not os.path.exists("compiler"):
            subprocess.run([
                "g++",
                "compiler-design-c-embedded/file_opener.cpp",
                "compiler-design-c-embedded/parser.cpp",
                "compiler-design-c-embedded/scanner.cpp",
                "compiler-design-c-embedded/semantics.cpp",
                "-o",
                "compiler"
            ])

        # remove old assembly file
        if os.path.exists("compiler-design-c-embedded/compile.txt"):
            os.remove("compiler-design-c-embedded/compile.txt")

        try:
            result = subprocess.run(
                ["./compiler", source_file],
                capture_output=True,
                text=True
            )

            output = result.stdout

            st.subheader("Compiler Error")
            st.code(output if output else "No Error")

            error_keywords = [
                "error","invalid","syntax","semantic",
                "lexical","brace","incompatible"
            ]

            error_detected = any(word in output.lower() for word in error_keywords)

            assembly_file = "compiler-design-c-embedded/compile.txt"

            if not error_detected and os.path.exists(assembly_file):

                with open(assembly_file, "r") as f:
                    assembly = f.read()

                st.subheader("Generated Assembly Code")
                st.code(assembly)

            elif error_detected:
                st.warning("Compilation failed. Assembly code not generated.")

            else:
                st.warning("compile.txt not generated.")

        except Exception as e:
            st.error(f"Error running compiler: {e}")
