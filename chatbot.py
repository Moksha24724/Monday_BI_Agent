import pandas as pd


def answer_question(question, df):

    question = question.lower().strip()

    # =====================================================
    # TOTAL RECORDS
    # =====================================================

    if (
        "how many deals" in question
        or "total deals" in question
        or "total records" in question
        or "how many records" in question
    ):

        return f"There are {len(df)} records in the current board."

    # =====================================================
    # HIGH PRIORITY
    # =====================================================

    elif "high priority" in question:

        if "Priority" not in df.columns:
            return "Priority column not found."

        result = df[
            df["Priority"]
            .fillna("")
            .str.lower() == "high"
        ]

        if result.empty:
            return "No High Priority records found."

        return result

    # =====================================================
    # MEDIUM PRIORITY
    # =====================================================

    elif "medium priority" in question:

        if "Priority" not in df.columns:
            return "Priority column not found."

        result = df[
            df["Priority"]
            .fillna("")
            .str.lower() == "medium"
        ]

        if result.empty:
            return "No Medium Priority records found."

        return result

    # =====================================================
    # LOW PRIORITY
    # =====================================================

    elif "low priority" in question:

        if "Priority" not in df.columns:
            return "Priority column not found."

        result = df[
            df["Priority"]
            .fillna("")
            .str.lower() == "low"
        ]

        if result.empty:
            return "No Low Priority records found."

        return result

    # =====================================================
    # PRIORITY DISTRIBUTION
    # =====================================================

    elif (
        "priority distribution" in question
        or "priority chart" in question
        or question == "priority"
    ):

        if "Priority" not in df.columns:
            return "Priority column not found."

        counts = df["Priority"].value_counts()

        return {
            "text": "Priority Distribution",
            "chart": counts
        }

    # =====================================================
    # DEAL STAGE DISTRIBUTION
    # =====================================================

    elif (
        "deal stage" in question
        or "stage distribution" in question
        or "sales stage" in question
    ):

        if "Deal Stage" not in df.columns:
            return "Deal Stage column not found."

        counts = df["Deal Stage"].value_counts()

        top_stage = counts.idxmax()

        top_count = counts.max()

        return {
            "text": f'"{top_stage}" has the highest number of deals ({top_count}).',
            "chart": counts
        }

    # =====================================================
    # MOST COMMON STAGE
    # =====================================================

    elif (
        "most deals" in question
        or "highest stage" in question
        or "most common stage" in question
    ):

        if "Deal Stage" not in df.columns:
            return "Deal Stage column not found."

        counts = df["Deal Stage"].value_counts()

        return (
            f'The most common deal stage is '
            f'"{counts.idxmax()}" '
            f'with {counts.max()} records.'
        )
            # =====================================================
    # LEAST COMMON STAGE
    # =====================================================

    elif (
        "least common stage" in question
        or "fewest deals" in question
        or "lowest stage" in question
    ):

        if "Deal Stage" not in df.columns:
            return "Deal Stage column not found."

        counts = df["Deal Stage"].value_counts()

        return (
            f'The least common deal stage is '
            f'"{counts.idxmin()}" '
            f'with {counts.min()} records.'
        )

    # =====================================================
    # PROJECTS ON HOLD
    # =====================================================

    elif "hold" in question:

        if "Deal Stage" not in df.columns:
            return "Deal Stage column not found."

        result = df[
            df["Deal Stage"]
            .fillna("")
            .str.contains("hold", case=False)
        ]

        if result.empty:
            return "No projects are currently on hold."

        return result

    # =====================================================
    # LOST PROJECTS
    # =====================================================

    elif "lost" in question:

        if "Deal Stage" not in df.columns:
            return "Deal Stage column not found."

        result = df[
            df["Deal Stage"]
            .fillna("")
            .str.contains("lost", case=False)
        ]

        if result.empty:
            return "No lost projects found."

        return result

    # =====================================================
    # COMPLETED PROJECTS
    # =====================================================

    elif (
        "completed" in question
        or "closed won" in question
        or "won deals" in question
    ):

        if "Deal Stage" not in df.columns:
            return "Deal Stage column not found."

        result = df[
            df["Deal Stage"]
            .fillna("")
            .str.contains(
                "completed|closed won|won",
                case=False,
                regex=True
            )
        ]

        if result.empty:
            return "No completed projects found."

        return result

    # =====================================================
    # NEGOTIATION DEALS
    # =====================================================

    elif "negotiation" in question:

        if "Deal Stage" not in df.columns:
            return "Deal Stage column not found."

        result = df[
            df["Deal Stage"]
            .fillna("")
            .str.contains("negotiation", case=False)
        ]

        if result.empty:
            return "No negotiation deals found."

        return result

    # =====================================================
    # PROPOSAL DEALS
    # =====================================================

    elif "proposal" in question:

        if "Deal Stage" not in df.columns:
            return "Deal Stage column not found."

        result = df[
            df["Deal Stage"]
            .fillna("")
            .str.contains("proposal", case=False)
        ]

        if result.empty:
            return "No proposal deals found."

        return result

    # =====================================================
    # TOP CLIENTS
    # =====================================================

    elif "client" in question:

        if "Client Code" not in df.columns:
            return "Client information is not available."

        counts = (
            df["Client Code"]
            .value_counts()
            .head(10)
        )

        return {
            "text": "Top 10 Clients",
            "chart": counts
        }

    # =====================================================
    # BUSINESS SUMMARY
    # =====================================================

    elif (
        "summary" in question
        or "business summary" in question
        or "executive summary" in question
    ):

        total = len(df)

        if "Priority" in df.columns:
            high = len(
                df[
                    df["Priority"]
                    .fillna("")
                    .str.lower() == "high"
                ]
            )
        else:
            high = 0

        if "Deal Stage" in df.columns:

            counts = df["Deal Stage"].value_counts()

            top_stage = counts.idxmax()

        else:
            top_stage = "Not Available"

        return (
            f"""
Business Summary

📊 Total Records : {total}

🔥 High Priority : {high}

📈 Most Active Stage : {top_stage}

Recommendation:
Focus on high-priority opportunities and monitor deal stages regularly.
"""
        )

    # =====================================================
    # HELP
    # =====================================================

    else:

        return (
            """
I can answer questions like:

• How many deals?

• Total records

• High priority deals

• Medium priority deals

• Low priority deals

• Priority distribution

• Which deal stage has the most deals?

• Which deal stage has the fewest deals?

• Show projects on hold

• Show lost projects

• Show completed projects

• Show negotiation deals

• Show proposal deals

• Top clients

• Give me a business summary

• Executive summary
"""
        )