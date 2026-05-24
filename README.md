# DATA201_Dashboard-Final_Assignment-
This project aim to build a dashboard for data analytics and interactive visualization to uncover the personal hidden relationship between dietary habits and physical well-being using synthetic data.

#  About Fuel or Fatigue Analytics Dashboard:

An interactive, data-driven web application built with **Streamlit** and **Plotly** to explore, analyze, and visualize the relationships between dietary habits, caloric intake, and subjective biological responses (energy levels, mood, and stomach comfort). 

This project was developed as the final academic submission for **DATA 201**.

---

##  Academic Metadata
* **Course:** DATA 201 – Final Assignment
* **Student Name:** Khine Nwe Lin
* **Student ID:** PIUS20230089

---

## Repository Structure
├── .streamlit/
│   └── config.toml                  # Streamlit theme and UI configurations
├── app2.py                          # application source code
├── basic_caffeine_discomfort.png 
├── cover.png                        # home page banner image
├── food_and_feeling_tracker.csv    # The synthetic dataset
├── requirements.txt                 # Application package dependencies
├── wrapup.png                       # wrap up image
└── README.md                        # project documentation 



## The Story behind the dashboard

The core story of this data diary centers around an everyday lifestyle paradox. As a student relying heavily on **restaurants and fast food** the initial assumption to discomfort was that large, high-calorie commercial portions were the direct cause of physical sluggishness and stomach distress. 

However, mapping the data chronologically and categorically reveals a completely different narrative. While restaurant meals do supply the highest caloric spikes of the month, they do not trigger physical discomfort. Instead, the real danger happens outside of main meals. The high-calorie restaurant meals create a volatile blood sugar cycle; when that wave clears, it triggers **snacking habits**, which the data explicitly isolates as the **#1 driver that drains daily energy the most**. Meanwhile, any realized stomach discomfort is entirely decoupled from portion sizes, pointing instead to the chemical irritation of **spicy configurations** frequently found on restaurant menus. 

---

## 💡 Key Findings

* **The Volume Myth Debunked:** Statistical boxplot distributions reveal that total caloric volume does not drive gastrointestinal distress. The median caloric load for cleanly digested meals was actually higher (~400 kcal) than meals causing discomfort (~360 kcal). Total meal size is not the enemy.
* **The Worst Fatigue Driver:** Main meals are innocent of daytime drowsiness. Snacking cycles are explicitly flagged as the primary variable that drains mental and physical energy levels the most.
* **The True Inflammatory Trigger:** Stomach aches and digestive discomfort are directly correlated with chemical irritants (spicy food entries). Moving to a spicy meal instantly destroys the body's gut comfort safety margin.
* **Commercial Dependency:** The underlying lifestyle profile shows a massive dependency on external food sourcing (Restaurants and Fast Food), making menu modification the highest-leverage point for health optimization.

---

##  Decision-Making Explanation

When designing this dashboard, specific engineering and analytical choices were made to translate raw data rows into responsible real-world insights:

1. **Choosing the Right Visualizations:** * **Box Plots** were chosen specifically for calorie analysis because averages hide data distributions. Box plots mathematically proved that the variance and medians of sick days vs. healthy days were nearly identical, successfully breaking the calorie myth.
   * **Grouped Histograms** were selected to isolate categorical variables (like Spicy vs. Non-Spicy), separating background noise from clear health incidents.
2. **Actionable Prescription Rules:** Rather than using vague, unhelpful data summaries, the insights section is deliberately programmed with an optimization framework. Because the data shows volume doesn't cause pain, the framework responsibly advises the user to keep enjoying restaurant social portions, but simply **drop the spice level to zero** and **swap quick processed snacks for low-glycemic fuel** to solve the energy drain.

---

##  Ethical Discussion & Governance

As an application dealing with personal health, wellness, and behavioral biomarkers, a rigorous data governance framework was built directly into the project architecture:

* **Strict Privacy Protocols:** The dataset enforces absolute data minimization. No Personally Identifiable Information (PII)—such as names, emails, contact details, or location tracking—is collected or stored. The app functions as an isolated, client-side journal completely decoupled from clinical health records.
* **The Isolation Fallacy Constraint:** An ethical data analysis must acknowledge its own limits. By choosing to isolate diet (calories, spice, caffeine) as the sole variables, the dashboard systematically ignores external macro-variables like sleep deprivation, academic exam stress, hydration levels, and genetics. It is responsibly disclosed that an energy crash could be caused by a sleepless night, even if the app blames a snack.
* **The Synthetic Data Limitation:** Because this system was tested and built using synthetically generated data, it exhibits clean, predictable mathematical boundaries. Real human biology is inherently chaotic, non-linear, and unpredictable. 
* **Responsible Next Steps:** To maintain high ethical standards, the dashboard explicitly frames its insights as a **Technical Proof of Concept ** rather than a medical diagnostic tool. It contains permanent disclaimers warning users not to make drastic lifestyle or health changes based on these simulated charts alone, but to use this codebase as a secure blueprint to be fueled by a real, long-term human food log in the future.

---

##  Local Installation

To run this dashboard locally, ensure you have Python 3.8+ installed, then follow these steps:

### 1. Clone the Repository
```bash
git clone [https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git)
cd YOUR_REPOSITORY_NAME
