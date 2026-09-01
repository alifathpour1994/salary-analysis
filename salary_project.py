# ============================================================
# PROJECT: Global Salary Analysis — Data Analytics Job Market
# Author: Ali Fathpour
# Date: 2024
# Dataset: Salary by Job Title and Country (Kaggle)
# ============================================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ── LOAD ─────────────────────────────────────────────────────
df = pd.read_csv(r"C:\Users\acer\Desktop\Salary.csv")

# ── CLEAN ────────────────────────────────────────────────────
df = df[df["Salary"] >= 1000]          # remove suspicious salaries

education_map = {                       # decode education numbers
    0: "High School",
    1: "Bachelor",
    2: "Master",
    3: "PhD"
}
df["Education Level"] = df["Education Level"].map(education_map)
df["Senior"] = df["Senior"].map({0: "Junior", 1: "Senior"})

# ── ANALYSIS ─────────────────────────────────────────────────
data_analysts = df[df["Job Title"] == "Data Analyst"]

# Q1 — Data Analyst global salary
print("Q1 — Data Analyst Salaries Globally")
print(f"Count:   {len(data_analysts)}")
print(f"Average: ${data_analysts['Salary'].mean():,.0f}")
print(f"Median:  ${data_analysts['Salary'].median():,.0f}")
print(f"Min:     ${data_analysts['Salary'].min():,.0f}")
print(f"Max:     ${data_analysts['Salary'].max():,.0f}")

# Q2 — by country
print("\nQ2 — Data Analyst Salary by Country")
da_by_country = data_analysts.groupby("Country")["Salary"].mean().sort_values(ascending=False)
print(da_by_country.apply(lambda x: f"${x:,.0f}"))

# Q3 — by education
print("\nQ3 — Salary by Education Level")
edu_order = ["High School", "Bachelor", "Master", "PhD"]
edu_salary = df.groupby("Education Level")["Salary"].mean().reindex(edu_order)
print(edu_salary.apply(lambda x: f"${x:,.0f}"))

# Q4 — junior vs senior
print("\nQ4 — Junior vs Senior")
senior_salary = df.groupby("Senior")["Salary"].mean()
print(senior_salary.apply(lambda x: f"${x:,.0f}"))
junior = df[df["Senior"] == "Junior"]["Salary"].mean()
senior = df[df["Senior"] == "Senior"]["Salary"].mean()
print(f"Senior earns ${senior-junior:,.0f} more (+{(senior-junior)/junior*100:.1f}%)")

# Q5 — top paying jobs
print("\nQ5 — Top 10 Highest Paying Jobs")
top_jobs = df.groupby("Job Title")["Salary"].mean().sort_values(ascending=False).head(10)
print(top_jobs.apply(lambda x: f"${x:,.0f}"))

# ── VISUALIZATIONS ───────────────────────────────────────────
sns.set_theme(style="whitegrid")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("Global Salary Analysis — Data Analytics Job Market",
             fontsize=16, fontweight="bold", y=1.02)

# chart 1 — DA salary by country
axes[0, 0].bar(da_by_country.index, da_by_country.values,
               color="steelblue", edgecolor="white")
axes[0, 0].set_title("Data Analyst Salary by Country", fontweight="bold")
axes[0, 0].set_xlabel("Country")
axes[0, 0].set_ylabel("Average Salary ($)")
axes[0, 0].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"${x:,.0f}"))

# chart 2 — salary by education
axes[0, 1].bar(edu_salary.index, edu_salary.values,
               color=["#d4e6f1", "#7fb3d3", "#2e86c1", "#1a5276"],
               edgecolor="white")
axes[0, 1].set_title("Salary by Education Level", fontweight="bold")
axes[0, 1].set_xlabel("Education Level")
axes[0, 1].set_ylabel("Average Salary ($)")
axes[0, 1].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"${x:,.0f}"))

# chart 3 — junior vs senior
axes[1, 0].bar(senior_salary.index, senior_salary.values,
               color=["#aed6f1", "#1a5276"], edgecolor="white", width=0.5)
axes[1, 0].set_title("Junior vs Senior Salary", fontweight="bold")
axes[1, 0].set_xlabel("Level")
axes[1, 0].set_ylabel("Average Salary ($)")
axes[1, 0].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"${x:,.0f}"))

# chart 4 — top 10 jobs
axes[1, 1].barh(top_jobs.index, top_jobs.values,
                color="steelblue", edgecolor="white")
axes[1, 1].set_title("Top 10 Highest Paying Jobs", fontweight="bold")
axes[1, 1].set_xlabel("Average Salary ($)")
axes[1, 1].invert_yaxis()
axes[1, 1].xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"${x:,.0f}"))

plt.tight_layout()
plt.savefig("salary_analysis.png", dpi=150, bbox_inches="tight")
plt.show()

# ── SUMMARY ──────────────────────────────────────────────────
print("\n" + "=" * 60)
print("PROJECT SUMMARY — Global Salary Analysis")
print("=" * 60)
print(f"""
Dataset: 6,680 employees across 5 countries

KEY FINDINGS:
1. Data Analysts earn $120,606 average globally
   - UK pays most ($125,097), Australia least ($117,807)
   - Difference between countries: only $7,290

2. Education has the biggest salary impact:
   - High School: $34,416
   - Bachelor:    $95,177  (+$60,761)
   - Master:      $130,078 (+$34,901)
   - PhD:         $165,772 (+$35,694)

3. Seniority adds 30.4% to salary:
   - Junior: $110,551 → Senior: $144,159

4. Career ceiling:
   - Data Analyst:            ~$120,000
   - Director of Data Science: ~$204,000
   - CTO / CEO:                $250,000

CONCLUSION:
Bachelor's degree entry level: ~$95,177 globally.
Becoming senior adds ~$33,608.
UK offers highest Data Analyst compensation globally.
""")

