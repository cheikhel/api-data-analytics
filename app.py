import requests
import pandas as pd
import streamlit as st
import plotly.express as px


# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="JSONPlaceholder Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==================================================
# CUSTOM CSS
# ==================================================

st.html("""
<style>

/* ------------------------------------------------
   GENERAL
------------------------------------------------ */

.stApp {
    background: #F4F7FC;
}

.block-container {
    max-width: 1500px;
    padding-top: 1.3rem;
    padding-left: 2rem;
    padding-right: 2rem;
    padding-bottom: 2rem;
}

header[data-testid="stHeader"] {
    display: none;
}

div[data-testid="stVerticalBlock"] {
    gap: 0.85rem;
}


/* ------------------------------------------------
   SIDEBAR
------------------------------------------------ */

section[data-testid="stSidebar"] {
    background: #FFFFFF;
    border-right: 1px solid #E5EAF2;
}

section[data-testid="stSidebar"] > div {
    padding-top: 1.4rem;
}

.brand {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 28px;
}

.brand-icon {
    width: 38px;
    height: 38px;
    border-radius: 10px;
    background: linear-gradient(
        135deg,
        #4F7CFF,
        #7655F5
    );
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 19px;
}

.brand-name {
    font-size: 18px;
    font-weight: 700;
    color: #182235;
}

.sidebar-section {
    color: #A6AFC0;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    margin-top: 22px;
    margin-bottom: 8px;
}

.sidebar-item {
    padding: 10px 12px;
    border-radius: 9px;
    color: #637083;
    font-size: 13px;
    margin-bottom: 3px;
}

.sidebar-active {
    padding: 10px 12px;
    border-radius: 9px;
    background: #EAF2FF;
    color: #3478F6;
    font-size: 13px;
    font-weight: 600;
    margin-bottom: 3px;
}

.sidebar-footer {
    color: #919BAD;
    font-size: 11px;
    line-height: 1.8;
    margin-top: 22px;
}


/* ------------------------------------------------
   HEADER
------------------------------------------------ */

.top-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}

.dashboard-title {
    color: #172033;
    font-size: 28px;
    font-weight: 700;
    line-height: 1.2;
}

.dashboard-subtitle {
    color: #8A95A8;
    font-size: 13px;
    margin-top: 5px;
}

.live-pill {
    background: #EAF7F0;
    color: #299866;
    padding: 8px 13px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
}


/* ------------------------------------------------
   METRIC CARDS
------------------------------------------------ */

.metric-card {
    background: #FFFFFF;
    border: 1px solid #E7ECF3;
    border-radius: 14px;
    padding: 17px 18px;
    box-shadow: 0 4px 14px rgba(27, 39, 58, 0.04);
    min-height: 122px;
}

.metric-icon {
    width: 35px;
    height: 35px;
    border-radius: 9px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 17px;
}

.icon-blue {
    background: #EAF3FF;
}

.icon-orange {
    background: #FFF3E5;
}

.icon-red {
    background: #FFECEC;
}

.icon-green {
    background: #E9F8EF;
}

.metric-label {
    color: #8792A5;
    font-size: 12px;
    margin-top: 12px;
}

.metric-value {
    color: #172033;
    font-size: 26px;
    font-weight: 700;
    margin-top: 2px;
}

.metric-note {
    color: #A0A8B7;
    font-size: 10px;
    margin-top: 3px;
}


/* ------------------------------------------------
   CHART CARDS
------------------------------------------------ */

.panel-title {
    color: #172033;
    font-size: 15px;
    font-weight: 700;
}

.panel-subtitle {
    color: #98A2B3;
    font-size: 11px;
    margin-top: 3px;
    margin-bottom: 8px;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #FFFFFF !important;
    border: 1px solid #E7ECF3 !important;
    border-radius: 14px !important;
    box-shadow: 0 4px 14px rgba(27, 39, 58, 0.04);
    padding: 8px !important;
}


/* ------------------------------------------------
   TABLE CARDS
------------------------------------------------ */

.table-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 14px;

    padding:
        18px
        18px
        16px
        18px;

    box-shadow:
        0 4px 14px rgba(27, 39, 58, 0.05);

    min-height: 360px;
}

.table-card-title {
    color: #172033;
    font-size: 15px;
    font-weight: 700;
    margin-bottom: 4px;
}

.table-card-subtitle {
    color: #98A2B3;
    font-size: 11px;
    margin-bottom: 18px;
}


/* ------------------------------------------------
   CUSTOM TABLE
------------------------------------------------ */

.custom-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 12px;
    background: #FFFFFF;
}

.custom-table thead th {
    background: #F8FAFD;
    color: #7E899C;

    text-align: left;

    padding:
        11px
        10px;

    border-bottom:
        1px solid #E7ECF3;

    font-weight: 600;
}

.custom-table tbody td {
    color: #344054;

    padding:
        10px
        10px;

    border-bottom:
        1px solid #EEF1F5;
}

.custom-table tbody tr:last-child td {
    border-bottom: none;
}

.custom-table tbody tr:hover {
    background: #F8FAFD;
}


/* ------------------------------------------------
   SUMMARY
------------------------------------------------ */

.summary-card {
    margin-top: 2px;

    padding:
        21px
        24px;

    border-radius: 14px;

    background: linear-gradient(
        110deg,
        #F4A328 0%,
        #518DE8 100%
    );

    color: white;

    box-shadow:
        0 5px 15px rgba(27, 39, 58, 0.08);
}

.summary-label {
    font-size: 11px;
    opacity: 0.8;
}

.summary-value {
    font-size: 20px;
    font-weight: 700;
    margin-top: 4px;
}

.summary-description {
    font-size: 11px;
    opacity: 0.88;
    margin-top: 5px;
}

</style>
""")


# ==================================================
# API
# ==================================================

BASE_URL = "https://jsonplaceholder.typicode.com"


@st.cache_data
def fetch_data(endpoint):

    url = f"{BASE_URL}/{endpoint}"

    response = requests.get(
        url,
        timeout=10
    )

    response.raise_for_status()

    return response.json()


try:

    users = fetch_data("users")
    posts = fetch_data("posts")
    comments = fetch_data("comments")
    todos = fetch_data("todos")

except requests.RequestException as error:

    st.error(
        f"Unable to load API data: {error}"
    )

    st.stop()


# ==================================================
# DATAFRAMES
# ==================================================

users_df = pd.DataFrame(
    users
)

posts_df = pd.DataFrame(
    posts
)

comments_df = pd.DataFrame(
    comments
)

todos_df = pd.DataFrame(
    todos
)


# ==================================================
# POSTS PER USER
# ==================================================

posts_per_user = (
    posts_df
    .groupby("userId")
    .size()
    .reset_index(
        name="post_count"
    )
)


user_activity = users_df[
    [
        "id",
        "name"
    ]
].merge(
    posts_per_user,
    left_on="id",
    right_on="userId"
)


# ==================================================
# COMMENTS
# ==================================================

total_posts = len(
    posts_df
)

total_comments = len(
    comments_df
)


average_comments_per_post = (
    total_comments
    /
    total_posts
)


comments_per_post = (
    comments_df
    .groupby("postId")
    .size()
    .reset_index(
        name="comment_count"
    )
)


posts_with_comments = posts_df.merge(
    comments_per_post,
    left_on="id",
    right_on="postId"
)


top_5_posts = (
    posts_with_comments
    .sort_values(
        by="comment_count",
        ascending=False
    )
    .head(5)
)


# ==================================================
# TODOs
# ==================================================

total_todos = len(
    todos_df
)


completed_todos = int(
    todos_df["completed"].sum()
)


pending_todos = (
    total_todos
    -
    completed_todos
)


todo_completion_percentage = (
    completed_todos
    /
    total_todos
) * 100


todo_status = pd.DataFrame({

    "Status": [
        "Completed",
        "Pending"
    ],

    "Count": [
        completed_todos,
        pending_todos
    ]

})


# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.html("""
<div class="brand">

    <div class="brand-icon">
        ▥
    </div>

    <div class="brand-name">
        Data Admin
    </div>

</div>


<div class="sidebar-section">
    Dashboard
</div>


<div class="sidebar-active">
    ▣ &nbsp; Overview
</div>

<div class="sidebar-item">
    👤 &nbsp; Users
</div>

<div class="sidebar-item">
    📝 &nbsp; Posts
</div>

<div class="sidebar-item">
    💬 &nbsp; Comments
</div>

<div class="sidebar-item">
    ✅ &nbsp; TODOs
</div>


<div class="sidebar-section">
    Project
</div>


<div class="sidebar-item">
    ⚙ &nbsp; API Data
</div>

<div class="sidebar-item">
    📈 &nbsp; Analytics
</div>


<div class="sidebar-footer">

    JSONPlaceholder Analytics

    <br>

    Python • Streamlit

    <br>

    Pandas • Plotly

</div>
""")


# ==================================================
# HEADER
# ==================================================

st.html("""
<div class="top-row">

    <div>

        <div class="dashboard-title">
            Dashboard
        </div>

        <div class="dashboard-subtitle">
           API analytics overview
        </div>

    </div>

    <div class="live-pill">
        ● Live API
    </div>

</div>
""")


# ==================================================
# METRIC CARDS
# ==================================================

col1, col2, col3, col4 = st.columns(
    4
)


with col1:

    st.html(
        f"""
<div class="metric-card">

    <div class="metric-icon icon-blue">
        👤
    </div>

    <div class="metric-label">
        Total Users
    </div>

    <div class="metric-value">
        {len(users_df)}
    </div>

    <div class="metric-note">
        Registered API users
    </div>

</div>
"""
    )


with col2:

    st.html(
        f"""
<div class="metric-card">

    <div class="metric-icon icon-orange">
        📝
    </div>

    <div class="metric-label">
        Total Posts
    </div>

    <div class="metric-value">
        {total_posts}
    </div>

    <div class="metric-note">
        Published posts
    </div>

</div>
"""
    )


with col3:

    st.html(
        f"""
<div class="metric-card">

    <div class="metric-icon icon-red">
        💬
    </div>

    <div class="metric-label">
        Total Comments
    </div>

    <div class="metric-value">
        {total_comments}
    </div>

    <div class="metric-note">
        Average {average_comments_per_post:.1f} per post
    </div>

</div>
"""
    )


with col4:

    st.html(
        f"""
<div class="metric-card">

    <div class="metric-icon icon-green">
        ✅
    </div>

    <div class="metric-label">
        TODO Completion
    </div>

    <div class="metric-value">
        {todo_completion_percentage:.1f}%
    </div>

    <div class="metric-note">
        {completed_todos} of {total_todos} tasks completed
    </div>

</div>
"""
    )


# ==================================================
# CHART ROW
# ==================================================

chart_left, chart_right = st.columns(
    [
        1.75,
        1
    ]
)


# ==================================================
# POSTS CHART
# ==================================================

with chart_left:

    with st.container(
        border=True
    ):

        st.html("""
<div class="panel-title">
    User Activity
</div>

<div class="panel-subtitle">
    Number of posts created by each user
</div>
""")


        posts_chart = px.bar(
            user_activity,
            x="name",
            y="post_count"
        )


        posts_chart.update_traces(

            marker_color="#4385EE",

            marker_line_width=0,

            hovertemplate=(
                "<b>%{x}</b>"
                "<br>Posts: %{y}"
                "<extra></extra>"
            )

        )


        posts_chart.update_layout(

            height=315,

            paper_bgcolor="#FFFFFF",

            plot_bgcolor="#FFFFFF",

            margin=dict(
                l=35,
                r=15,
                t=10,
                b=40
            ),

            bargap=0.18,

            font=dict(
                color="#667085",
                size=10
            ),

            xaxis=dict(

                title="",

                showgrid=False,

                tickangle=-28,

                tickfont=dict(
                    size=9,
                    color="#98A2B3"
                )

            ),

            yaxis=dict(

                title="Posts",

                range=[
                    0,
                    11
                ],

                gridcolor="#EEF1F5",

                zeroline=False,

                tickfont=dict(
                    color="#98A2B3"
                )

            )

        )


        st.plotly_chart(

            posts_chart,

            use_container_width=True,

            config={
                "displayModeBar": False
            }

        )


# ==================================================
# TODO DONUT
# ==================================================

with chart_right:

    with st.container(
        border=True
    ):

        st.html("""
<div class="panel-title">
    TODO Status
</div>

<div class="panel-subtitle">
    Overall task completion
</div>
""")


        todo_chart = px.pie(

            todo_status,

            names="Status",

            values="Count",

            hole=0.70,

            color="Status",

            color_discrete_map={
                "Completed": "#4385EE",
                "Pending": "#FF6464"
            }

        )


        todo_chart.update_traces(

            textinfo="percent",

            textfont=dict(
                size=11
            ),

            hovertemplate=(
                "<b>%{label}</b>"
                "<br>Tasks: %{value}"
                "<br>%{percent}"
                "<extra></extra>"
            )

        )


        todo_chart.update_layout(

            height=315,

            paper_bgcolor="#FFFFFF",

            margin=dict(
                l=10,
                r=10,
                t=5,
                b=35
            ),

            legend=dict(

                orientation="h",

                y=-0.05,

                x=0.20,

                font=dict(
                    size=10
                )

            )

        )


        st.plotly_chart(

            todo_chart,

            use_container_width=True,

            config={
                "displayModeBar": False
            }

        )


# ==================================================
# TABLE DATA
# ==================================================

activity_table = (

    user_activity[
        [
            "name",
            "post_count"
        ]
    ]

    .rename(

        columns={
            "name": "User",
            "post_count": "Posts"
        }

    )

)


activity_html = activity_table.to_html(

    index=False,

    classes="custom-table",

    border=0

)


top_posts_table = (

    top_5_posts[
        [
            "id",
            "title",
            "comment_count"
        ]
    ]

    .rename(

        columns={
            "id": "ID",
            "title": "Post Title",
            "comment_count": "Comments"
        }

    )

)


top_posts_html = top_posts_table.to_html(

    index=False,

    classes="custom-table",

    border=0

)


# ==================================================
# TABLE ROW
# ==================================================

table_left, table_right = st.columns(
    [
        1,
        1.6
    ]
)


# ==================================================
# ACTIVITY SUMMARY CARD
# ==================================================

with table_left:

    st.html(
        f"""
<div class="table-card">

    <div class="table-card-title">
        Activity Summary
    </div>

    <div class="table-card-subtitle">
        Posts generated by each API user
    </div>

    {activity_html}

</div>
"""
    )


# ==================================================
# MOST COMMENTED POSTS CARD
# ==================================================

with table_right:

    st.html(
        f"""
<div class="table-card">

    <div class="table-card-title">
        Most Commented Posts
    </div>

    <div class="table-card-subtitle">
        Top 5 posts ranked by comment count
    </div>

    {top_posts_html}

</div>
"""
    )


# ==================================================
# SUMMARY
# ==================================================

st.html(
    f"""
<div class="summary-card">

    <div class="summary-label">
        Dataset Overview
    </div>

    <div class="summary-value">

        {len(users_df)} Users
        &nbsp; • &nbsp;
        {total_posts} Posts
        &nbsp; • &nbsp;
        {total_comments} Comments
        &nbsp; • &nbsp;
        {total_todos} TODOs

    </div>

    <div class="summary-description">

        Data retrieved live from the
        JSONPlaceholder REST API.

    </div>

</div>
"""
)