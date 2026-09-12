import sys
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from socratic_tutor.config import load_config, resolve_path

cfg = load_config()
csv_file = resolve_path(cfg["paths"]["evaluation_csv"])
out_dir = resolve_path("results/figures")
out_dir.mkdir(parents=True, exist_ok=True)
df = pd.read_csv(csv_file)

sns.histplot(df["unit_test_pass_rate"], bins=10, kde=True)
plt.xlabel("Unit-test Pass Rate (%)"); plt.ylabel("Number of Sessions")
plt.title("Distribution of Unit-test Pass Rate Across Chat Logs")
plt.tight_layout(); plt.savefig(out_dir / "pass_rate_distribution.png", dpi=200); plt.close()

plt.figure(figsize=(12, 6))
sns.boxplot(x="title", y="unit_test_pass_rate", data=df)
plt.xticks(rotation=45, ha="right"); plt.ylabel("Unit-test Pass Rate (%)"); plt.xlabel("Problem")
plt.title("Unit-test Pass Rate per Problem"); plt.tight_layout()
plt.savefig(out_dir / "pass_rate_by_problem.png", dpi=200); plt.close()

plt.figure(figsize=(8, 6))
sns.scatterplot(x="reference_test_lines", y="user_test_lines", hue="unit_test_pass_rate", size="unit_test_pass_rate", sizes=(50, 200), data=df)
plt.xlabel("Number of Reference Test Lines"); plt.ylabel("Number of User Test Lines Submitted")
plt.title("User Test Coverage vs Reference Tests"); plt.tight_layout()
plt.savefig(out_dir / "test_coverage.png", dpi=200); plt.close()

pivot = df.pivot_table(values="unit_test_pass_rate", index="title", aggfunc="mean")
plt.figure(figsize=(8, 6)); sns.heatmap(pivot, annot=True, fmt=".1f")
plt.title("Average Unit-test Pass Rate per Problem"); plt.xlabel("Average Pass Rate"); plt.ylabel("Problem")
plt.tight_layout(); plt.savefig(out_dir / "average_pass_rate_heatmap.png", dpi=200); plt.close()

avg = df.groupby("title")["unit_test_pass_rate"].mean().sort_values()
plt.figure(figsize=(12, 5)); avg.plot(kind="bar")
plt.ylabel("Average Unit-test Pass Rate (%)"); plt.title("Average Unit-test Pass Rate per Problem")
plt.xticks(rotation=45, ha="right"); plt.tight_layout(); plt.savefig(out_dir / "average_pass_rate.png", dpi=200); plt.close()

plt.figure(figsize=(8, 5)); sns.ecdfplot(df["unit_test_pass_rate"])
plt.xlabel("Unit-test Pass Rate (%)"); plt.ylabel("CDF"); plt.title("Cumulative Distribution of Unit-test Pass Rate")
plt.tight_layout(); plt.savefig(out_dir / "pass_rate_ecdf.png", dpi=200); plt.close()
print(f"Saved figures to {out_dir}")
