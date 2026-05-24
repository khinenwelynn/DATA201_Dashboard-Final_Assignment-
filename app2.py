import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration 
st.set_page_config(page_title="Fuel or Fatigue", layout="wide", initial_sidebar_state="expanded")

# 2. Load the Dataset 
@st.cache_data
def load_data():
    # Using your filename
    data = pd.read_csv("food_and_feeling_tracker.csv")
    data['Date'] = pd.to_datetime(data['Date'])
    return data

try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading data file: {e}")
    st.stop()

# 3. Navigation Sidebar
st.sidebar.title("You are at")
page = st.sidebar.radio(
    "Select:",
    ["Home", "Data Visualizations", "Key Insights", "Ethics & Responsibility"]
)

st.sidebar.markdown("---")

# 4. Filter Controls 
st.sidebar.header("Data Filters")

# --- Food Categories ---
unique_categories = list(df["Food_Category"].unique())
all_cat_checked = st.sidebar.checkbox("Select All Categories", value=True)

selected_categories = st.sidebar.multiselect(
    "Select Food Categories:",
    options=unique_categories,
    default=unique_categories if all_cat_checked else []
)

# --- Meal Types ---
unique_meals = list(df["Meal_Type"].unique())
all_meals_checked = st.sidebar.checkbox("Select All Meal Types", value=True)

selected_meals = st.sidebar.multiselect(
    "Select Meal Types:",
    options=unique_meals,
    default=unique_meals if all_cat_checked else []
)

# --- Downstream Filtering Logic ---
filtered_df = df[
    (df["Food_Category"].isin(selected_categories)) & 
    (df["Meal_Type"].isin(selected_meals))
]


if page == "Home":
    st.image("cover.png", caption="My Food Diary", use_container_width=True)
    st.title("Food: Fuel or Fatigue?")
    st.markdown("### *Evaluation of Personal Dietary Habits and Physical Well-being by Khine Nwe Lin*")
    st.markdown("---")

    # Story Section
    st.header("The Story Behind This Dashboard")
    
    st.markdown(
        """
        > **“Biologically, food is supposed to fuel us and give us energy. Instead, I often find myself feeling completely drowsy, sluggish, or dealing with an irritated stomach right after a meal.”**
        
        Like many people, I struggle with maintaining a healthy relationship with food. Eating mindlessly or choosing convenience 
        over nutrition has started taking a toll on my daily physical and mental state. To figure out if my post-meal crash 
        and digestive issues are directly tied to specific eating habits, I decided to track my pattern over an entire month.
        
        ### How This Dashboard Was Built
        Using my real logged history from **MyFitnessPal** as a foundation, this dataset was synthetically engineered to model 
        a comprehensive **31-day personal food and feeling log**. By cross-referencing caloric intake, food choices, 
        and daily physical symptoms (like energy dips and stomach comfort levels), this project aims to turn subjective physical exhaustion into objective, actionable data insights.
        """
    )
    
    st.markdown("---")
    st.header("General Overview")
    
    if not filtered_df.empty:
        # Calculate daily caloric 
        daily_calories = filtered_df.groupby(filtered_df['Date'].dt.date)['Total_Calories'].sum()
        
        avg_daily = daily_calories.mean()
        min_daily = daily_calories.min()
        max_daily = daily_calories.max()
        
        # Calculate discomfort occurrences 
        total_meals = len(filtered_df)
        discomfort_meals = len(filtered_df[filtered_df['Physical_Discomfort'] == 'Yes'])
        discomfort_rate = (discomfort_meals / total_meals * 100) if total_meals > 0 else 0
        
        # Display Metrics in Columns
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(label="Total Meals Logged", value=f"{total_meals} meals")
            
        with col2:
            st.metric(label="Avg. Daily Intake", value=f"{int(avg_daily):,} kcal")
            
        with col3:
            st.metric(label="Daily Caloric Range", value=f"{int(max_daily)} max", delta=f"{int(min_daily)} min delta", delta_color="off")
            
            st.caption(f"Range: {int(min_daily):,} to {int(max_daily):,} kcal/day")
            
        with col4:
            st.metric(label="Discomfort Frequency", value=f"{discomfort_rate:.1f}%", delta=f"{discomfort_meals} total incidents", delta_color="inverse")
            
    else:
        st.warning("⚠️ Please select at least one filter in the sidebar to populate the data metrics.")

    st.markdown("---")
    st.subheader("Explore the dataset:")
    st.markdown("Below is the record of my 31-day food journal that is used in this dashboard")
    st.dataframe(filtered_df, use_container_width=True)

elif page == "Data Visualizations":
    st.title("Exploratory Data Analysis & Insights")
    st.markdown("---")
    
    if filtered_df.empty:
        st.warning("⚠️ No data matches your filter criteria. Please re-select options from the sidebar filters.")
    else:
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("1. Food Category vs. Stomach & Mood")
            avg_metrics = filtered_df.groupby("Food_Category")[["Stomach_Comfort", "Mood"]].mean().reset_index()
            fig1 = px.bar(
                avg_metrics, x="Food_Category", y=["Stomach_Comfort", "Mood"],
                barmode="group", color_discrete_sequence=["#F232EF", "#bcbd22"],
                labels={"value": "Average Score (1-10)", "variable": "Metric"}
            )
            fig1.update_layout(plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig1, use_container_width=True)
            st.caption("Insight: Home-cooked best and stable in both mood and physical wellbeing.")

        with c2:
            st.subheader("2. Caloric Intake Timeline")
            fig2 = px.line(
                filtered_df, x="Date", y="Total_Calories", color="Food_Category",
                markers=True, title="My Caloric Footprint within a month",
                color_discrete_map={"fast food": "#bcbd22", "restaurant": "#1f77b4", "homecook": "#2ca02c", "prepacked": "#F232EF"}
            )
            st.plotly_chart(fig2, use_container_width=True)
            st.caption("Insight: a cycle of restricted eating followed by sudden heavy meals rather than steady fuel distribution")

        st.markdown("<br>", unsafe_allow_html=True) 
        c3, c4 = st.columns(2)
        
        with c3:
            st.subheader("3. Does Caffeine make me feel good? ")
            fig3=px.histogram(
                filtered_df, x="Physical_Discomfort", color="Caffeine_Intake",
                barmode="group", color_discrete_map={"Yes": "#F232EF", "No": "#bcbd22"},
                labels={"Caffeine_Intake": "Caffeine Consumed", "count": "Log Count"}
            )
            st.plotly_chart(fig3, use_container_width=True)
            st.caption("Insight: Caffeine is a neutral factor that doesn't effect my physical wellbeing")

        with c4:
            st.subheader("4. IS my discomfort due to the spicy food I am eating?")
            fig4 = px.histogram(
                filtered_df, x="Spicy_Or_NonSpicy", color="Physical_Discomfort",
                barmode="group", color_discrete_map={"Yes":  "#F232EF", "No": "#bcbd22"}
            )
            st.plotly_chart(fig4, use_container_width=True)
            st.caption("Insight: Spicy food are absolute destroyer of the physical wellbeing")

        st.markdown("<br>", unsafe_allow_html=True) 
        c5, c6 = st.columns(2)
        with c5:
            st.subheader("5. Which meal do I eat Most? ")
            meal_counts = filtered_df["Meal_Type"].value_counts().reset_index()
            meal_counts.columns = ["Meal_Type", "Count"]
            fig7 = px.pie(
                meal_counts, values="Count", names="Meal_Type",
                color_discrete_sequence=px.colors.sequential.Plasma
            )
            st.plotly_chart(fig7, use_container_width=True)
            st.caption("Insight:Snack was the most eated category.")
        
        
        with c6:
            st.subheader("6. Top 10 Most Eaten Foods Overall")
            top_foods = filtered_df["Food_Name"].value_counts().reset_index().head(10)
            top_foods.columns = ["Food_Name", "Log_Count"]
            fig6 = px.bar(
                top_foods, x="Log_Count", y="Food_Name", orientation='h',
                color="Log_Count", color_continuous_scale="Plasma"
            )
            fig6.update_layout(yaxis={'categoryorder':'total ascending'}, plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig6, use_container_width=True)
            st.caption("Insight:Cp chicken roll and instant noodles, shan noodles are the most eaten.")

        st.markdown("<br>", unsafe_allow_html=True) 
        c7, c8 = st.columns(2)
        
        with c7:
            st.subheader("7. Does Meal Size (Calories) Trigger Discomfort?")
            
            if "Total_Calories" in filtered_df.columns and "Physical_Discomfort" in filtered_df.columns:
                fig7 = px.box(
                    filtered_df, 
                    x="Physical_Discomfort", 
                    y="Total_Calories",
                    color="Physical_Discomfort",
                    color_discrete_map={"Yes": "#F232EF", "No": "#bcbd22"}, 
                    labels={"Physical_Discomfort": "Experienced Discomfort?", "Total_Calories": "Meal Calories (kcal)"}
                )
                fig7.update_layout(plot_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig7, use_container_width=True)
                st.caption("Insight: frequently eat larger meals and feel completely fine")
            else:
                st.warning("⚠️ Missing 'Total_Calories' or 'Physical_Discomfort' columns.")

        with c8:
            st.subheader("8. Sourcing Profile: Do I Eat at Restaurants Most?")
            cat_counts = filtered_df["Food_Category"].value_counts().reset_index()
            cat_counts.columns = ["Food_Category", "Count"]
            fig8 = px.pie(
                cat_counts, values="Count", names="Food_Category",
                color_discrete_sequence=px.colors.sequential.Blues_r)
            st.plotly_chart(fig8, use_container_width=True)
            st.caption("Insight: mostly rely on restaurant and fast food than home-cooked meals.")

        st.markdown("<br><hr>", unsafe_allow_html=True)
        st.subheader("9.  Which Meal Type Drains Your Energy Most?")
        
        if "Meal_Type" in filtered_df.columns and "Energy_After" in filtered_df.columns:
            fig9 = px.box(
                filtered_df, 
                x="Meal_Type", 
                y="Energy_After",
                color="Meal_Type",
                color_discrete_sequence=px.colors.sequential.Blues_r, 
                labels={"Meal_Type": "Meal Type", "Energy_After": "Post-Meal Energy Level (1-10)"}
            )
            fig9.update_layout(plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig9, use_container_width=True)
            st.caption("Value Insight: 'Snacks' Category with median 4 shows that snacking habits are actively causing drowsiness instead of providing fuel.")
        else:
            st.warning("⚠️ Missing 'Meal_Type' or 'Energy_After' columns in your dataset.")
##################################3
if page == "Key Insights":
    st.title("Key Insights based on the visualizations")
    st.markdown("---")


    # THE BIG PICTURE: THE CORE DIETARY 

    st.markdown("## Executive Summary: My Dietary Pattern")
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric(label="Primary Food Source", value="Outside", delta="- Restaurant/Fast Food")
    m2.metric(label="Highest Calorie Source", value="Restaurant Meals", delta="1100 calories in one sitting for mala xianguo")
    m3.metric(label="Primary Stomach Trigger", value="Spiciness", delta="Inflammatory Factor", delta_color="inverse")
    m4.metric(label="Worst Energy Drainer", value="Snacks", delta="Sodium", delta_color="inverse")
    
    st.markdown("---")

    # DETAILED THEME ANALYSIS: TWO-COLUMN LAYOUT
    # Left Side: High-Impact Visuals | Right Side: Analytical Narratives
    # =========================================================
    left_visuals, right_narratives = st.columns([2, 1], gap="large")

    with left_visuals:
        # ---------------------------------------------------------
        # THEME 1: THE COMMERCIAL DEPENDENCY & CALORIC LOAD
        # ---------------------------------------------------------
        st.subheader(" The Commercial Dependency")
        c1, c2 = st.columns(2)
        
        with c1:
            if "Food_Category" in filtered_df.columns:
                cat_counts = filtered_df["Food_Category"].value_counts().reset_index()
                cat_counts.columns = ["Food_Category", "Count"]
                fig_source = px.pie(
                    cat_counts, values="Count", names="Food_Category",
                    title="Food sources",
                    color_discrete_sequence=px.colors.sequential.Pinkyl
                )
                fig_source.update_layout(showlegend=False, margin=dict(t=40, b=10, l=10, r=10))
                st.plotly_chart(fig_source, use_container_width=True)
        
        with c2:
            if "Food_Category" in filtered_df.columns and "Total_Calories" in filtered_df.columns:
                avg_cal = filtered_df.groupby("Food_Category")["Total_Calories"].mean().reset_index()
                fig_cal = px.bar(
                    avg_cal, x="Food_Category", y="Total_Calories",
                    title="Average Calorie Intake by Source",
                    color="Total_Calories", color_continuous_scale="Pinkyl"
                )
                fig_cal.update_layout(plot_bgcolor="rgba(0,0,0,0)", showlegend=False, coloraxis_showscale=False, margin=dict(t=40, b=10, l=10, r=10))
                st.plotly_chart(fig_cal, use_container_width=True)

        st.markdown("<hr style='border-top: 1px dashed #bbb;'>", unsafe_allow_html=True)


        # THEME 2: DISPROVING THE CALORIE THRESHOLD

        st.subheader("The High Calorie Intake Myth")
        
        if "Total_Calories" in filtered_df.columns and "Physical_Discomfort" in filtered_df.columns:
            fig_box = px.box(
                filtered_df, x="Physical_Discomfort", y="Total_Calories",
                color="Physical_Discomfort",
                color_discrete_map={"Yes": "#e05297", "No": "#fcd34d"},
                title="Portion Size vs. Realized Stomach Discomfort"
            )
            fig_box.update_layout(plot_bgcolor="rgba(0,0,0,0)", margin=dict(t=40, b=10, l=10, r=10))
            st.plotly_chart(fig_box, use_container_width=True)

        st.markdown("<hr style='border-top: 1px dashed #bbb;'>", unsafe_allow_html=True)


        st.subheader("The Real Culprit of physical discomfort")
        c3, c4 = st.columns(2)
        
        with c3:
            if "Spicy_Or_NonSpicy" in filtered_df.columns and "Physical_Discomfort" in filtered_df.columns:
                fig_spice = px.histogram(
                    filtered_df, x="Spicy_Or_NonSpicy", color="Physical_Discomfort",
                    barmode="group", color_discrete_map={"Yes": "#e05297", "No": "#fcd34d"},
                    title="Stomach Discomfort: Spicy vs Non-Spicy"
                )
                fig_spice.update_layout(plot_bgcolor="rgba(0,0,0,0)", margin=dict(t=40, b=10, l=10, r=10))
                st.plotly_chart(fig_spice, use_container_width=True)
                
        with c4:
            if "Meal_Type" in filtered_df.columns and "Energy_After" in filtered_df.columns:
                fig_energy = px.box(
                    filtered_df, x="Meal_Type", y="Energy_After",
                    title="Post-Meal Energy Distribution",
                    color="Meal_Type", color_discrete_sequence=px.colors.sequential.Sunset
                )
                fig_energy.update_layout(plot_bgcolor="rgba(0,0,0,0)", showlegend=False, margin=dict(t=40, b=10, l=10, r=10))
                st.plotly_chart(fig_energy, use_container_width=True)


    with right_narratives:
        st.markdown("### Explanations")
        st.markdown("---")
        
        
        st.info(
            """
            **The Commercial Dependency**
            
            The heavy reliance on external food options—with **Fast Food and Restaurants controlling THE MOST** of monthly food comsumption. 
            
            Obviously, **restaurant meals bring in highest calorie counts of the month**. 
            """
        )
        
        
        st.success(
            """
            **Volume Doesn't Matter (at least for me)**
            
            The common myth of *'I only feel sick because I overate'* is entirely debunked. 
            
            The median calorie baseline for meals that caused distress is actually **lower (~360 kcal)** than meals digested cleanly without any issues **(~400 kcal)**. That means the body manages total physical volume efficiently; portion size is not my worst enemy.
            """
        )
        
        st.error(
            """
            **The Spice & The Snack Problem**
            
            If meal size doesn't matter, what does? The data shoes two highly specific culprits:
            
            * **Stomach Distress:** Driven directly by **spicy configurations**. Moving to a spicy meal instantly destroys physical comfort. 
            * **Mental/Physical Fatigue:** Main meals are innocent. **Snacks are explicitly flagged as the #1 item that drains your energy levels the most**, leading to sharp energy crashes.
            """
        )
        
        st.markdown("---")
        
        st.markdown("#### In the Future")
        st.warning(
            """
            **The Optimization with food:**
            
            1. **Mala Xianguo with no spice** Since calorie volume doesn't cause stomach aches, so can order mala xianguo but need to **drop the spice level almost entirely** to remove the physical discomfort trigger.
            
            2. **No more snacks** Needs to reduce eating snacks that induce drowsiness. Plan to Swap them for clean, steady-burning fuel sources to protect the productivity.

            3. **Homecooked meals**  clean, steady-burning fuel sources such as homecooked meals are recommended to increase frequency to protect the productivity, energy, mood and physical discomfort.
            """
        )
elif page == "Ethics & Responsibility":
    st.title("Ethics & Responsibility Disclosure")
    st.markdown("---")
    
    st.header("Privacy & Data Protection Statement")
    
    with st.container():
        st.markdown(
            """
            This section outlines how this personal data is handled responsibly. Because dietary habits and personal well-being metrics are sensitive, the application is built with strict privacy and security standards in mind
            """
        )
        
        priv_col1, priv_col2 = st.columns(2)
        
        with priv_col1:
            st.info(
                """
                #### **Data Included**
                * **Dietary Logistics:** Time of consumption, meal types (Breakfast, Lunch, Dinner, Snack), and food categorization tags.
                * **Nutritional Metrics:** Total estimated caloric intake ($kcal$) aggregated via MyFitnessPal inputs.
                * **Subjective Biomarkers:** User-reported quantitative ratings ($1-10$) monitoring stomach comfort, emotional mood, and post-meal energy levels.
                """
            )
            
        with priv_col2:
            st.success(
                """
                #### **Excluded Data**
                * **Personal Information:** names, places, email addresses, or any personal data are not stored in the underlying dataset.
                * **No Medical Records:** This log strictly records informal behavioral tracking entries; it does not connect to or pull from any real health records.
                """
            )

    st.markdown("<br><hr>", unsafe_allow_html=True)


    st.header("Bias & System Limitation Disclosure")
    st.markdown(
        """ 
        Users must evaluate the insights on this dashboard through the lens of the following limitations:
        """
    )

    with st.expander(" Memory & Recency Bias"):
        st.markdown(
            """
            * **The Bias:** Because food logs rely on manual, self-reported entry, they are heavily subject to **Memory Bias**. Meals eaten on the go, late at night, or small snacks are frequently logged hours after consumption, leading to estimated or forgotten entries. Furthermore, **Recency Bias** might cause the user to rate post-meal symptoms harsher if they are filling out the log during an active state of severe discomfort.
            """
        )

    with st.expander(" Small Dataset & Synthetic Constraints"):
        st.markdown(
            """
            * **The Limitation:** The dataset captures a short-term snapshot of behavioral metricswhich was **synthetically generated** for development purposes. Small sample sizes mean that minor data anomalies can disproportionately skew the averages.
              Furthermore, because the data is simulated, it lacks real-world randomness and biological complexity. Therefore, cannot be treated as real-world clinical **causations**."""
        )

    with st.expander(" Subjective Scoring"):
        st.markdown(
            """
            * **The Bias:** Metrics like `Mood`, `Energy_After`, and `Stomach_Comfort` are personal and  forced into a quantitative scale ($1-10$).
            * **The Impact:** A score of '5' given on a high-stress Monday might feel biologically identical to a score of '7' given on a relaxed Saturday. Over the course of a month, **Scale Drift** occurs as the tracker's internal definition of comfort and fatigue fluctuates, introducing measurement noise into the charts.
            """
        )

    with st.expander(" Variable Exclusions"):
        st.markdown(
            """
            * **The Limitation:** This dashboard isolates food, spice, and caffeine as the sole drivers of physical wellness. External macro-variables such as systemic sleep deprivation, baseline work stress, hormonal fluctuations, and hydration levels are completely omitted from the pipeline, meaning some recorded crashes may be falsely attributed to food.
            """
        )

    st.header("Limitations of future suggestions made in this project")
    st.markdown(
        """Deploying this analytics dashboard involves clear trade-offs, summarized by two major constraints: the Isolation Fallacy and Synthetic Data Generation. By designing a system that focuses exclusively on food metrics (calories, spice, and caffeine), the dashboard might operates by systematically ignoring other critical external factors such as sleep quality, academic stress, and  hydration. 
        In addition, because the underlying data is mathematically simulated rather than organically logged from a human subject, it exhibits clean, predictable correlations that lack the chaotic, non-linear realities of actual human biology. Consequently, there can be a risk of false attribution such as blaming a restaurant meal for an energy crash that was actually caused by an anxious, sleepless week.
        To handle these insights responsibly, this dashboard must be treated strictly as a technical proof of concept and no user should make drastic lifestyle or health changes based on these charts
        """
    )
    # Final legal/ethical footprint note
    st.markdown("<br>", unsafe_allow_html=True)
    st.caption(
        "*Disclaimer: This dashboard functions purely as a personal exploratory behavioral analytics done for DATA 201 Final Assignment. "
        "The calculated insights do not constitute, and should not be substituted for, formal medical advice or dietary prescriptions.*"
    )

    st.image("wrapup.png", caption="My Food Diary (continued) Photo Consent was also granted", use_container_width=True)
    st.markdown("---")
    st.header("Thank you!")

st.markdown("<br><br><br>", unsafe_allow_html=True) 
st.markdown("---")
st.markdown(
    "<center style='color: gray; font-size: 0.85em;'>"
    "DATA 201 – Final Assignment &nbsp;|&nbsp; <b>Khine Nwe Lin</b> &nbsp;|&nbsp; ID: PIUS20230089"
    "</center>", 
    unsafe_allow_html=True
)