import streamlit as st

from src.agents.fdd_product import run_fdd


st.set_page_config(
    page_title="AI-FDD Intelligence",
    page_icon="📊",
    layout="wide",
)


st.title("AI-FDD Intelligence")
st.caption(
    "Evidence-backed AI platform for Financial Due Diligence"
)

st.divider()


# =========================================================
# GENERATE FULL FDD REPORT
# =========================================================

st.subheader("Generate Full FDD Report")

st.write(
    "Run the complete FDD workflow across the specialist "
    "financial analysis agents."
)

if st.button(
    "Generate Full FDD Report",
    type="primary",
    use_container_width=True,
):

    with st.spinner("Running FDD analysis..."):

        try:
            result = run_fdd(mode="generate")

            st.success("FDD report generated successfully.")

            # -------------------------------------------------
            # Execution Summary
            # -------------------------------------------------

            execution = result["execution"]

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Agents Executed",
                    execution["agent_count"],
                )

            with col2:
                st.write("**Specialist Agents**")

                for agent in execution["agents_executed"]:
                    st.write(f"✓ {agent}")

            # -------------------------------------------------
            # Executive Summary
            # -------------------------------------------------

            st.subheader("Executive Summary")

            summary = result["report"]["executive_summary"]

            if isinstance(summary, dict):

                for key, value in summary.items():

                    label = key.replace("_", " ").title()

                    if isinstance(value, (dict, list)):
                        st.write(f"**{label}:**")
                        st.write(value)
                    else:
                        st.write(
                            f"**{label}:** {value}"
                        )

            else:
                st.write(summary)

            # -------------------------------------------------
            # Download Report
            # -------------------------------------------------

            st.subheader("Generated Report")

            pdf_path = result["pdf_path"]

            st.write(
                "Your FDD report has been generated successfully."
            )

            with open(pdf_path, "rb") as pdf_file:
                pdf_bytes = pdf_file.read()

            st.download_button(
                label="Download FDD Report (PDF)",
                data=pdf_bytes,
                file_name="AI-FDD_Report.pdf",
                mime="application/pdf",
                use_container_width=True,
            )

        except Exception as exc:

            st.error(
                f"Unable to generate the FDD report: {exc}"
            )


st.divider()


# =========================================================
# ASK FDD QUESTION
# =========================================================

st.subheader("Ask a Due Diligence Question")

question = st.text_input(
    "Question",
    placeholder=(
        "e.g. What is the main customer concentration risk?"
    ),
)

if st.button(
    "Ask Question",
    use_container_width=True,
):

    if not question.strip():

        st.warning("Please enter a question.")

    else:

        with st.spinner("Analysing the question..."):

            try:

                result = run_fdd(
                    mode="query",
                    question=question,
                )

                st.success("Analysis complete.")

                # -------------------------------------------------
                # Agent Execution
                # -------------------------------------------------

                execution = result.get(
                    "execution",
                    {},
                )

                st.subheader("Agent Execution")

                agents = execution.get(
                    "agents_executed",
                    [],
                )

                if agents:

                    for agent in agents:
                        st.write(f"✓ {agent}")

                # -------------------------------------------------
                # Findings
                # -------------------------------------------------

                st.subheader("Findings")

                for finding in result.get(
                    "results",
                    [],
                ):

                    st.markdown(
                        f"### {finding.get('agent', 'Finding')}"
                    )

                    st.write(
                        finding.get(
                            "finding",
                            "",
                        )
                    )

                    risk = finding.get(
                        "risk_level"
                    )

                    if risk:
                        st.write(
                            f"**Risk Level:** {risk}"
                        )

                    # Evidence
                    evidence = finding.get("evidence")

                    if evidence:

                        st.write("**Evidence**")

                        if isinstance(evidence, list):

                            for item in evidence:

                                if isinstance(item, dict):

                                    st.write(
                                        item.get(
                                            "text",
                                            item,
                                        )
                                    )

                                else:
                                    st.write(item)

                        else:
                            st.write(evidence)

                # -------------------------------------------------
                # Executive Summary
                # -------------------------------------------------

                executive_summary = result.get(
                    "executive_summary"
                )

                if executive_summary:

                    st.subheader(
                        "Executive Summary"
                    )

                    st.write(
                        executive_summary
                    )

            except Exception as exc:

                st.error(
                    f"Unable to answer the question: {exc}"
                )


st.divider()


# =========================================================
# FOOTER
# =========================================================

st.caption(
    "Prototype using synthetic financial data. "
    "AI outputs require appropriate human review."
)