import sys
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from socratic_tutor.config import load_config, resolve_path

cfg = load_config()
csv_file = resolve_path(cfg["paths"]["evaluation_csv"])
out_dir = resolve_path(cfg["paths"]["figures"])
out_dir.mkdir(parents=True, exist_ok=True)
df = pd.read_csv(csv_file)

if df.empty:
    raise SystemExit("Evaluation CSV is empty; nothing to visualize.")

# The notebook used seaborn for these plots. Matplotlib-only versions keep the same
# analytical views while reducing an otherwise unnecessary dependency.
fig, ax = plt.subplots(figsize=(8,5))
ax.hist(df["unit_test_pass_rate"], bins=10)
ax.set(xlabel="Unit-test Pass Rate (%)", ylabel="Number of Sessions", title="Distribution of Unit-test Pass Rate Across Chat Logs")
fig.tight_layout(); fig.savefig(out_dir / "pass_rate_distribution.png", dpi=200); plt.close(fig)

fig, ax = plt.subplots(figsize=(12,6))
df.boxplot(column="unit_test_pass_rate", by="title", ax=ax)
ax.set_ylabel("Unit-test Pass Rate (%)"); ax.set_xlabel("Problem"); ax.set_title("Unit-test Pass Rate per Problem")
plt.suptitle(""); plt.xticks(rotation=45, ha="right"); fig.tight_layout(); fig.savefig(out_dir / "pass_rate_by_problem.png", dpi=200); plt.close(fig)

fig, ax = plt.subplots(figsize=(8,6))
ax.scatter(df["reference_test_lines"], df["user_test_lines"], s=50 + 2*df["unit_test_pass_rate"])
ax.set(xlabel="Number of Reference Test Lines", ylabel="Number of User Test Lines Submitted", title="User Test Coverage vs Reference Tests")
fig.tight_layout(); fig.savefig(out_dir / "test_coverage.png", dpi=200); plt.close(fig)

pivot = df.pivot_table(values="unit_test_pass_rate", index="title", aggfunc="mean")
fig, ax = plt.subplots(figsize=(8,6))
im = ax.imshow(pivot.values, aspect="auto")
ax.set_yticks(range(len(pivot.index)), pivot.index)
ax.set_xticks([0], ["Average Pass Rate"])
for i, value in enumerate(pivot.iloc[:,0]):
    ax.text(0, i, f"{value:.1f}", ha="center", va="center")
ax.set_title("Average Unit-test Pass Rate per Problem")
fig.colorbar(im, ax=ax, label="Average Pass Rate")
fig.tight_layout(); fig.savefig(out_dir / "average_pass_rate_heatmap.png", dpi=200); plt.close(fig)

avg = df.groupby("title")["unit_test_pass_rate"].mean().sort_values()
fig, ax = plt.subplots(figsize=(12,5)); avg.plot(kind="bar", ax=ax)
ax.set_ylabel("Average Unit-test Pass Rate (%)"); ax.set_title("Average Unit-test Pass Rate per Problem")
plt.xticks(rotation=45, ha="right"); fig.tight_layout(); fig.savefig(out_dir / "average_pass_rate.png", dpi=200); plt.close(fig)

fig, ax = plt.subplots(figsize=(8,5))
values = sorted(df["unit_test_pass_rate"].dropna())
y = [(i+1)/len(values) for i in range(len(values))]
ax.step(values, y, where="post")
ax.set(xlabel="Unit-test Pass Rate (%)", ylabel="CDF", title="Cumulative Distribution of Unit-test Pass Rate")
fig.tight_layout(); fig.savefig(out_dir / "pass_rate_ecdf.png", dpi=200); plt.close(fig)

print(f"Saved figures to {out_dir}")
