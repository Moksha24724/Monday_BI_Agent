import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

from monday_api import (
    get_board_data,
    DEALS_BOARD_ID,
    WORK_ORDERS_BOARD_ID
)

from data_cleaner import clean_board
from chatbot import answer_question


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Monday BI Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =====================================================
# HEADER
# =====================================================

st.markdown("""
<div style="
background:linear-gradient(90deg,#1f77b4,#4facfe);
padding:25px;
border-radius:15px;
color:white;">

<h1>🤖 Monday Business Intelligence Agent</h1>

<h4>Real-Time Business Dashboard using Monday.com API</h4>

<p>
📊 Analytics &nbsp;&nbsp;|&nbsp;&nbsp;
🤖 AI Insights &nbsp;&nbsp;|&nbsp;&nbsp;
📈 Business Intelligence
</p>

</div>
""", unsafe_allow_html=True)

st.caption(
    f"🕒 Last Updated : {datetime.now().strftime('%d %b %Y %I:%M %p')}"
)


# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("⚙ Dashboard Settings")

board_choice = st.sidebar.selectbox(
    "Select Board",
    [
        "Deals",
        "Work Orders"
    ]
)

if st.sidebar.button("🔄 Refresh Dashboard"):
    st.rerun()

theme = st.sidebar.selectbox(
    "🎨 Theme",
    [
        "Light",
        "Dark"
    ]
)


# =====================================================
# LOAD DATA
# =====================================================

if board_choice == "Deals":

    board_data = get_board_data(
        DEALS_BOARD_ID
    )

else:

    board_data = get_board_data(
        WORK_ORDERS_BOARD_ID
    )

rows = clean_board(board_data)

df = pd.DataFrame(rows)


# =====================================================
# FILTERS
# =====================================================

st.sidebar.markdown("---")
st.sidebar.subheader("🔍 Filters")

if "Deal Stage" in df.columns:

    stages = st.sidebar.multiselect(
        "Deal Stage",
        sorted(df["Deal Stage"].dropna().unique())
    )

    if stages:

        df = df[
            df["Deal Stage"].isin(stages)
        ]

if "Priority" in df.columns:

    priorities = st.sidebar.multiselect(
        "Priority",
        sorted(df["Priority"].dropna().unique())
    )

    if priorities:

        df = df[
            df["Priority"].isin(priorities)
        ]


# =====================================================
# KPI CALCULATIONS
# =====================================================

high_priority = 0
on_hold = 0

if "Priority" in df.columns:

    high_priority = len(
        df[
            df["Priority"] == "High"
        ]
    )

if "Deal Stage" in df.columns:

    on_hold = len(
        df[
            df["Deal Stage"]
            .fillna("")
            .str.contains(
                "Hold",
                case=False
            )
        ]
    )


# =====================================================
# TABS
# =====================================================

tab1, tab2, tab3 = st.tabs(
    [
        "📊 Dashboard",
        "📈 Analytics",
        "🤖 AI Assistant"
    ]
)

# =====================================================
# DASHBOARD TAB
# =====================================================

with tab1:

    st.subheader("📊 Dashboard Overview")

    # ----------------------------------------
    # SEARCH
    # ----------------------------------------

    search = st.text_input(
        "🔍 Search Records",
        placeholder="Search by any value..."
    )

    filtered_df = df.copy()

    if search:

        filtered_df = filtered_df[
            filtered_df.astype(str)
            .apply(
                lambda x: x.str.contains(
                    search,
                    case=False,
                    na=False
                )
            )
            .any(axis=1)
        ]

    st.write("")

# ----------------------------------------
# KPI CARDS
# ----------------------------------------

# Calculate KPI values
if "Priority" in filtered_df.columns:
    high = len(
        filtered_df[
            filtered_df["Priority"]
            .fillna("")
            .str.lower() == "high"
        ]
    )
else:
    high = 0

if "Deal Stage" in filtered_df.columns:
    hold = len(
        filtered_df[
            filtered_df["Deal Stage"]
            .fillna("")
            .str.contains("hold", case=False)
        ]
    )
else:
    hold = 0


# Create three KPI columns
kpi1, kpi2, kpi3 = st.columns(3)


# Total Records
with kpi1:
    st.markdown(f"""
    <div style="
        background:#E8F4FD;
        padding:20px;
        border-radius:12px;
        text-align:center;
        border-left:8px solid #2196F3;">
        <h4>📊 Total Records</h4>
        <h1>{len(filtered_df)}</h1>
        <p>Business Data Loaded</p>
    </div>
    """, unsafe_allow_html=True)


# High Priority
with kpi2:
    st.markdown(f"""
    <div style="
        background:#FFF4E5;
        padding:20px;
        border-radius:12px;
        text-align:center;
        border-left:8px solid orange;">
        <h4>🔥 High Priority</h4>
        <h1>{high}</h1>
        <p>Needs Attention</p>
    </div>
    """, unsafe_allow_html=True)


# On Hold
with kpi3:
    st.markdown(f"""
    <div style="
        background:#FDECEC;
        padding:20px;
        border-radius:12px;
        text-align:center;
        border-left:8px solid red;">
        <h4>⏳ Projects On Hold</h4>
        <h1>{hold}</h1>
        <p>Pending Review</p>
    </div>
    """, unsafe_allow_html=True)
    # ----------------------------------------
    # QUICK SUMMARY
    # ----------------------------------------

    st.divider()

left, right = st.columns([3, 1])

# ==========================
# LEFT SIDE - DATA TABLE
# ==========================

with left:

    st.subheader(f"📋 {board_choice} Board")

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )

    st.info(f"Displaying **{len(filtered_df)}** records.")

# ==========================
# RIGHT SIDE - SUMMARY
# ==========================

with right:

    # ==========================
    # CURRENT BOARD
    # ==========================

    st.info(f"""
### 📁 Current Board

**Board:** {board_choice}

**Records:** {len(filtered_df)}

**🔥 High Priority:** {high}
""")

    st.write("")

    # ==========================
    # BUSINESS HEALTH
    # ==========================

    active_records = len(filtered_df) - hold

    if active_records >= hold:
        status = "🟢 Healthy"
    else:
        status = "🟠 Needs Attention"

    st.success(f"""
### 📈 Business Health

{status}

✅ **Active Records:** {active_records}

⏳ **On Hold:** {hold}
""")
    # ----------------------------------------
    # DATA TABLE
    # ----------------------------------------

    
    # =====================================================
# ANALYTICS TAB
# =====================================================

with tab2:

    st.subheader("📈 Business Analytics Dashboard")

    chart_col1, chart_col2 = st.columns(2)

    # -----------------------------------------
    # DEAL STAGE DISTRIBUTION
    # -----------------------------------------

    with chart_col1:

        if "Deal Stage" in df.columns:

            stage_counts = (
                df["Deal Stage"]
                .fillna("Unknown")
                .value_counts()
                .reset_index()
            )

            stage_counts.columns = [
                "Stage",
                "Count"
            ]

            fig_stage = px.bar(
                stage_counts,
                x="Stage",
                y="Count",
                color="Count",
                text="Count",
                title="Deal Stage Distribution"
            )

            st.plotly_chart(
                fig_stage,
                use_container_width=True,
                key="stage_chart"
            )

    # -----------------------------------------
    # PRIORITY DISTRIBUTION
    # -----------------------------------------

    with chart_col2:

        if "Priority" in df.columns:

            priority_counts = (
                df["Priority"]
                .fillna("Unknown")
                .value_counts()
                .reset_index()
            )

            priority_counts.columns = [
                "Priority",
                "Count"
            ]

            fig_priority = px.pie(
                priority_counts,
                names="Priority",
                values="Count",
                hole=0.45,
                title="Priority Distribution"
            )

            st.plotly_chart(
                fig_priority,
                use_container_width=True,
                key="priority_chart"
            )

    st.divider()

    # -----------------------------------------
    # HORIZONTAL BAR CHART
    # -----------------------------------------

    if "Deal Stage" in df.columns:

        fig_horizontal = px.bar(
            stage_counts,
            x="Count",
            y="Stage",
            orientation="h",
            color="Count",
            title="Deals by Stage"
        )

        st.plotly_chart(
            fig_horizontal,
            use_container_width=True,
            key="horizontal_chart"
        )

    st.divider()

    # -----------------------------------------
    # AI BUSINESS INSIGHTS
    # -----------------------------------------

    st.subheader("🧠 AI Business Insights")

    left, right = st.columns(2)

    with left:

        st.success(f"📊 Total Records : {len(df)}")

        st.warning(f"🔥 High Priority : {high_priority}")

    with right:

        st.info(f"⏳ Projects On Hold : {on_hold}")

        if "Deal Stage" in df.columns:

            top_stage = df["Deal Stage"].value_counts().idxmax()

            st.success(
                f"📈 Most Active Stage : {top_stage}"
            )

    st.divider()

    # -----------------------------------------
    # TOP 5 RECORDS
    # -----------------------------------------

    st.subheader("🏆 Top 5 Records")

    st.dataframe(
        df.head(),
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # -----------------------------------------
    # BOARD STATISTICS
    # -----------------------------------------

    st.subheader("📈 Board Statistics")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Rows",
        len(df)
    )

    c2.metric(
        "Columns",
        len(df.columns)
    )

    c3.metric(
        "Missing Values",
        int(df.isna().sum().sum())
    )
    # =====================================================
# AI ASSISTANT TAB
# =====================================================

with tab3:

    st.subheader("🤖 AI Business Assistant")

    # -----------------------------------------
    # EXECUTIVE SUMMARY
    # -----------------------------------------

    if st.button(
        "📄 Generate Executive Summary",
        key="summary_button"
    ):

        st.info(f"""
### 📄 Executive Summary

**Current Board:** {board_choice}

📊 Total Records : **{len(df)}**

🔥 High Priority : **{high_priority}**

⏳ Projects On Hold : **{on_hold}**

### 📌 Recommendation

• Focus on High Priority records.

• Monitor projects currently On Hold.

• Review Deal Stage progress regularly.

• Use dashboard analytics to identify trends.
""")

    st.divider()

    # -----------------------------------------
    # ASK AI
    # -----------------------------------------

    question = st.text_input(
        "💬 Ask AI",
        placeholder="Example: How many high priority deals?",
        key="question_box"
    )

    if st.button(
        "🤖 Ask AI",
        key="ask_ai_button"
    ):

        if question.strip() == "":

            st.warning("Please enter a question.")

        else:

            with st.spinner("Analyzing business data..."):

                answer = answer_question(
                    question,
                    df
                )

            st.subheader("📌 AI Response")

            if isinstance(answer, dict):

                st.success(answer["text"])

                if "chart" in answer:

                    chart = answer["chart"]

                    if isinstance(chart, pd.Series):

                        st.bar_chart(chart)

                    elif isinstance(chart, pd.DataFrame):

                        st.dataframe(
                            chart,
                            use_container_width=True
                        )

            elif isinstance(answer, pd.DataFrame):

                st.dataframe(
                    answer,
                    use_container_width=True,
                    hide_index=True
                )

            elif isinstance(answer, pd.Series):

                st.bar_chart(answer)

            else:

                st.success(answer)

    st.divider()

    # -----------------------------------------
    # DOWNLOAD CSV
    # -----------------------------------------

    st.subheader("📥 Export Data")

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📄 Download CSV",
        data=csv,
        file_name=f"{board_choice.lower().replace(' ','_')}.csv",
        mime="text/csv",
        key="download_csv"
    )


# =====================================================
# FOOTER
# =====================================================

st.divider()

st.markdown(
"""
---
<center>

### 🚀 Built by Mokshitha N.V.

Artificial Intelligence & Machine Learning Engineer

**Powered by**

Python 🐍 | Streamlit 📊 | Monday.com API 🤖

© 2026 Monday BI Agent

</center>
""",
unsafe_allow_html=True
)