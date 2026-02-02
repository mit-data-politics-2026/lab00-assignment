import marimo

__generated_with = "0.19.7"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    import polars as pl
    import altair as alt
    return alt, pl


@app.cell
def _(mo):
    mo.md("""
    # Lab 0: Environment Check

    Welcome to **17.831 Data and Politics**! This notebook verifies that your computing
    environment is set up correctly—whether you're running locally or on GitHub Codespaces.

    **What you'll do:**

    1. Confirm that required packages are installed
    2. Enter some basic information about yourself
    3. See a personalized welcome visualization

    This should take about **15 minutes** to complete.
    """)
    return


@app.cell
def _(alt, mo, pl):
    # Environment checks - test that required packages are available
    checks = []

    # Check Marimo
    try:
        marimo_version = mo.__version__
        checks.append(("Marimo", marimo_version, True))
    except Exception:
        checks.append(("Marimo", "Not found", False))

    # Check Polars
    try:
        polars_version = pl.__version__
        checks.append(("Polars", polars_version, True))
    except Exception:
        checks.append(("Polars", "Not found", False))

    # Check Altair
    try:
        altair_version = alt.__version__
        checks.append(("Altair", altair_version, True))
    except Exception:
        checks.append(("Altair", "Not found", False))

    # Build status display
    check_rows = []
    for name, version, passed in checks:
        status = "✅" if passed else "❌"
        check_rows.append(f"| {name} | {version} | {status} |")

    all_passed = all(passed for _, _, passed in checks)
    status_kind = "success" if all_passed else "warn"
    status_msg = "All packages installed!" if all_passed else "Some packages missing"

    mo.vstack(
        [
            mo.md("## Environment Check"),
            mo.md(
                f"""
    | Package | Version | Status |
    |---------|---------|--------|
    {chr(10).join(check_rows)}
    """
            ),
            mo.callout(mo.md(f"**{status_msg}**"), kind=status_kind),
        ]
    )
    return


@app.cell
def _(mo):
    mo.md("""
    ## About You

    Please fill out the form below so we can get to know you better.
    Your responses will be saved when you commit this notebook.
    """)
    return


@app.cell
def _(mo):
    # Student information form
    name_input = mo.ui.text(label="Your name", placeholder="Enter your full name")

    year_dropdown = mo.ui.dropdown(
        options=["Freshman", "Sophomore", "Junior", "Senior", "Graduate", "Other"],
        label="Year",
        value="Graduate",
    )

    major_input = mo.ui.text(
        label="Major or field of study", placeholder="e.g., Political Science, Computer Science"
    )

    python_experience = mo.ui.radio(
        options={
            "None": "none",
            "Beginner (some tutorials)": "beginner",
            "Intermediate (completed projects)": "intermediate",
            "Advanced (professional experience)": "advanced",
        },
        label="Python experience level",
        value="None",
    )

    politics_interest = mo.ui.dropdown(
        options=[
            "Interested in politics",
            "Interested in data science/programming",
            "Required for my major",
            "Curious about data and politics intersection",
            "Other",
        ],
        label="Why are you taking this course?",
        value="Curious about data and politics intersection",
    )

    excitement_input = mo.ui.text_area(
        label="What excites you about this course?",
        placeholder="Tell us what you're hoping to learn or explore...",
    )

    mo.vstack(
        [
            mo.hstack([name_input, year_dropdown], justify="start", gap=2),
            major_input,
            python_experience,
            politics_interest,
            excitement_input,
        ],
        gap=1,
    )
    return (
        excitement_input,
        major_input,
        name_input,
        politics_interest,
        python_experience,
        year_dropdown,
    )


@app.cell
def _(
    excitement_input,
    major_input,
    mo,
    name_input,
    politics_interest,
    python_experience,
    year_dropdown,
):
    # Summary card showing entered information
    # Check if required fields are filled
    has_name = name_input.value and len(name_input.value.strip()) > 0
    has_major = major_input.value and len(major_input.value.strip()) > 0

    summary_table = f"""
    | Field | Your Response |
    |-------|---------------|
    | **Name** | {name_input.value} |
    | **Year** | {year_dropdown.value} |
    | **Major/Field** | {major_input.value or "Not specified"} |
    | **Python Experience** | {python_experience.value} |
    | **Why taking this course** | {politics_interest.value} |
    | **What excites you** | {excitement_input.value or "Not specified"} |
    """

    summary_content = (
        mo.callout(mo.md(summary_table), kind="info")
        if has_name
        else mo.callout(mo.md("*Please enter your name above to see your summary.*"), kind="warn")
    )

    mo.vstack([mo.md("## Your Information"), summary_content])
    return has_major, has_name


@app.cell
def _(alt, mo, name_input):
    # Personalized welcome visualization
    mo.md("## Welcome Card")

    display_name = name_input.value.strip() if name_input.value else "Student"

    # Create a simple welcome card visualization using Altair
    welcome_data = {"x": [0], "y": [0], "text": [f"Welcome, {display_name}!"]}

    welcome_chart = (
        alt.Chart(alt.Data(values=[{"x": 0, "y": 0}]))
        .mark_text(
            fontSize=32,
            fontWeight="bold",
            color="#2166ac",
        )
        .encode(
            x=alt.X("x:Q", axis=None, scale=alt.Scale(domain=[-1, 1])),
            y=alt.Y("y:Q", axis=None, scale=alt.Scale(domain=[-1, 1])),
            text=alt.value(f"Welcome, {display_name}!"),
        )
        .properties(width=500, height=150, title="17.831 Data and Politics")
        .configure_view(strokeWidth=0)
        .configure_title(fontSize=16, color="#666666")
    )

    welcome_chart
    return


@app.cell
def _(has_major, has_name, mo):
    # Completion status and submission instructions
    is_complete = has_name and has_major

    # Build the missing fields message
    missing = []
    if not has_name:
        missing.append("name")
    if not has_major:
        missing.append("major/field")

    complete_content = mo.vstack(
        [
            mo.callout(
                mo.md("""
    **✅ Environment check complete!**

    Your setup is working correctly and your information has been entered.
    """
                ),
                kind="success",
            ),
            mo.md("""
    ### Submission Instructions

    To submit this lab, commit and push your changes using Git:

    ```bash
    git add notebooks/lab00/lab00.py
    git commit -m "Complete Lab 0 environment check"
    git push
    ```

    Or use the Git integration in your editor (VS Code, GitHub Codespaces, etc.).
    """
            ),
        ]
    )

    incomplete_content = mo.callout(
        mo.md(f"""
    **⏳ Almost there!**

    Please fill in the following to complete this lab: {", ".join(missing)}
    """
        ),
        kind="warn",
    )

    status_content = complete_content if is_complete else incomplete_content

    mo.vstack([mo.md("## Completion Status"), status_content])
    return


if __name__ == "__main__":
    app.run()
