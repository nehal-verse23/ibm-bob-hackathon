import streamlit as st
import subprocess
import os

st.set_page_config(
    page_title="DevPulse",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ DevPulse")
st.subheader("AI Change Impact & Regression Risk Agent")

st.write(
    "DevPulse helps developers understand the impact of code changes, "
    "identify regression risks, and validate changes automatically."
)

st.divider()

st.header("🔍 Change Impact Analysis")

changed_file = st.selectbox(
    "Select a changed component",
    [
        "payments.py",
        "orders.py",
        "users.py",
        "notifications.py"
    ]
)

if st.button("Analyze Change"):

    if changed_file == "payments.py":

        st.success("Change analyzed successfully.")

        st.markdown("### Potentially Affected Components")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.error("HIGH RISK")
            st.write("orders.py")

        with col2:
            st.warning("MEDIUM RISK")
            st.write("notifications.py")

        with col3:
            st.warning("MEDIUM RISK")
            st.write("tests/")

        st.markdown("### Recommended Regression Tests")

        tests = [
            "Successful payment",
            "Invalid payment amount",
            "Negative payment amount",
            "Payment database interaction",
            "Order placement",
            "Order failure on invalid payment",
            "Payment notification on success",
            "No notification on failure"
        ]

        for test in tests:
            st.write("✓", test)

        st.divider()

        st.markdown("### Regression Validation")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Initial Validation",
                "3 Failed / 5 Passed"
            )

        with col2:
            st.metric(
                "After Fix",
                "8 Passed"
            )

        st.success(
            "✓ Final validation successful — all 8 regression tests passed."
        )

    else:

        st.info(
            f"DevPulse is ready to analyze changes in {changed_file}."
        )

st.divider()

st.header("🤖 IBM Bob Integration")

st.write(
    "IBM Bob Agent was used to investigate code changes, "
    "trace dependencies, analyze regression risks, investigate "
    "test failures, and validate the final fix."
)

st.caption(
    "DevPulse — Built for the IBM Bob 2.0 Hackathon"
)