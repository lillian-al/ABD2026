# ABD_TA_BENCHMARKING_DASHBOARD
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm, colors
import textwrap
from IPython.display import display

plt.rcParams.update({
    "figure.dpi": 135,
    "savefig.dpi": 135,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "axes.edgecolor": "#333333",
    "axes.titlesize": 13,
    "axes.labelsize": 10,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "legend.fontsize": 9,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.18,
    "grid.linewidth": 0.7,
})

raw_rows = [
    {"Team": "Team 1", "F2F office floor [m]": "4", "F2C Height office floor [m]": "3,5", "Total office area [m2]": "1535", "Total desks": "300", "Permanent workspaces": "300", "Minimum height in office space [m]": "3", "Core vs Usable Space Ratio": "0,3712", "Cost": "67,9", "Hours": "1608", "Average Facade Transparency": "0,289", "Sustainability BEAT": "11,84"},
    {"Team": "Team 2", "F2F office floor [m]": "3,695", "F2C Height office floor [m]": "2,74", "Total office area [m2]": "1667", "Total desks": "300", "Permanent workspaces": "300", "Minimum height in office space [m]": "2,74", "Core vs Usable Space Ratio": "x", "Cost": "64,7", "Hours": "1328", "Average Facade Transparency": "0,25", "Sustainability BEAT": "28,22"},
    {"Team": "Team 3", "F2F office floor [m]": "4", "F2C Height office floor [m]": "3,05", "Total office area [m2]": "1165", "Total desks": "302", "Permanent workspaces": "302", "Minimum height in office space [m]": "3,05", "Core vs Usable Space Ratio": "0,175", "Cost": "59,3", "Hours": "998", "Average Facade Transparency": "0,77", "Sustainability BEAT": "15,47"},
    {"Team": "Team 4", "F2F office floor [m]": "4,5", "F2C Height office floor [m]": "2,975", "Total office area [m2]": "2160", "Total desks": "449", "Permanent workspaces": "415", "Minimum height in office space [m]": "2,9", "Core vs Usable Space Ratio": "0,2274", "Cost": "95,5", "Hours": "1340", "Average Facade Transparency": "0,2784", "Sustainability BEAT": "31"},
    {"Team": "Team 5", "F2F office floor [m]": "5,094", "F2C Height office floor [m]": "2,98", "Total office area [m2]": "2533", "Total desks": "310", "Permanent workspaces": "310", "Minimum height in office space [m]": "2,98", "Core vs Usable Space Ratio": "-", "Cost": "146,8", "Hours": "1131", "Average Facade Transparency": "0,4", "Sustainability BEAT": "40"},
    {"Team": "Team 6", "F2F office floor [m]": "3,67", "F2C Height office floor [m]": "2,5", "Total office area [m2]": "1495", "Total desks": "306", "Permanent workspaces": "306", "Minimum height in office space [m]": "2,5", "Core vs Usable Space Ratio": "0,1367", "Cost": "92,3", "Hours": "1433,5", "Average Facade Transparency": "0,264", "Sustainability BEAT": "63,6"},
    {"Team": "Team 7", "F2F office floor [m]": "3,26", "F2C Height office floor [m]": "2,5", "Total office area [m2]": "1474", "Total desks": "422", "Permanent workspaces": "422", "Minimum height in office space [m]": "2,5", "Core vs Usable Space Ratio": "-", "Cost": "-", "Hours": "-", "Average Facade Transparency": "-", "Sustainability BEAT": np.nan},
    {"Team": "Team 8", "F2F office floor [m]": "4,2", "F2C Height office floor [m]": "3", "Total office area [m2]": "1392", "Total desks": "413", "Permanent workspaces": "365", "Minimum height in office space [m]": "3", "Core vs Usable Space Ratio": "0,0787", "Cost": "82,1", "Hours": "1351", "Average Facade Transparency": "0,27", "Sustainability BEAT": "7,381307506"},
    {"Team": "Team 9", "F2F office floor [m]": "3,67", "F2C Height office floor [m]": "2,87", "Total office area [m2]": "1297", "Total desks": "301", "Permanent workspaces": "301", "Minimum height in office space [m]": "2,87", "Core vs Usable Space Ratio": "0,492", "Cost": "90", "Hours": "1039", "Average Facade Transparency": "0,48", "Sustainability BEAT": "28,56847176"},
    {"Team": "Team 10", "F2F office floor [m]": "3,6", "F2C Height office floor [m]": "---", "Total office area [m2]": "1817", "Total desks": "351", "Permanent workspaces": "302", "Minimum height in office space [m]": "3,1", "Core vs Usable Space Ratio": "---", "Cost": "42,4", "Hours": "527", "Average Facade Transparency": "0,57", "Sustainability BEAT": "7,443452816"},
]

def to_number(value):
    if pd.isna(value):
        return np.nan
    text = str(value).strip()
    if text.lower() in {"", "-", "--", "---", "x", "xx", "xxx", "%", "#value!"}:
        return np.nan
    text = text.replace(" ", "").replace(",", ".")
    if re.fullmatch(r"[-+]?\d*\.?\d+", text):
        return float(text)
    return np.nan

df = pd.DataFrame(raw_rows)
for col in df.columns.difference(["Team"]):
    df[col] = df[col].map(to_number)

f2c_col = "F2C Height office floor [m]"
f2f_col = next(
    (
        col for col in [
            "F2F office floor [m]",
            "F2F Office Floor Height [m]",
            "F2F Office Floor Height",
            "F2F office floor height [m]",
            "F2F Height office floor [m]",
        ]
        if col in df.columns
    ),
    None,
)
if f2f_col is None:
    f2f_col = "F2F office floor [m]"
    df[f2f_col] = np.nan

df["Floor Buildup [m]"] = df[f2f_col] - df[f2c_col]

lower_is_better = [
    "Sustainability BEAT",
    "Cost",
    "Hours",
    "Core vs Usable Space Ratio",
    "Average Facade Transparency",
    "Floor Buildup [m]",
]
higher_is_better = [
    f2f_col,
    "F2C Height office floor [m]",
    "Total office area [m2]",
    "Total desks",
    "Permanent workspaces",
    "Minimum height in office space [m]",
]

metric_labels = {
    "Sustainability BEAT": "Sustainability BEAT",
    "Cost": "Cost",
    "Hours": "Hours",
    "Core vs Usable Space Ratio": "Core vs Usable Space Ratio",
    "Average Facade Transparency": "Average Facade Transparency",
    "Floor Buildup [m]": "Floor Buildup (F2F - F2C) [m]",
    f2f_col: "F2F office floor [m]",
    "F2C Height office floor [m]": "F2C Height office floor [m]",
    "Total office area [m2]": "Total Office Area [m²]",
    "Total desks": "Total desks",
    "Permanent workspaces": "Permanent workspaces",
    "Minimum height in office space [m]": "Minimum height in office space [m]",
}

def best_sort(metric):
    return metric in lower_is_better

def score_metric(series, lower_better):
    min_value = series.min(skipna=True)
    max_value = series.max(skipna=True)
    if pd.isna(min_value) or pd.isna(max_value) or np.isclose(max_value, min_value):
        return pd.Series(np.nan, index=series.index)
    if lower_better:
        return 100 * (max_value - series) / (max_value - min_value)
    return 100 * (series - min_value) / (max_value - min_value)

def value_text(value, unit=""):
    if pd.isna(value):
        return "NaN"
    if abs(value) >= 100:
        text = f"{value:,.0f}"
    elif abs(value) >= 10:
        text = f"{value:,.2f}".rstrip("0").rstrip(".")
    else:
        text = f"{value:,.3f}".rstrip("0").rstrip(".")
    return f"{text}{unit}"

def ranked_colors(scores):
    cmap = cm.get_cmap("RdYlGn")
    norm = colors.Normalize(vmin=0, vmax=100)
    return [cmap(norm(score)) if pd.notna(score) else "#BDBDBD" for score in scores]

def ranked_benchmark_chart(data, metric, title, unit="", lower_better=True, score_chart=False):
    plot_data = data[["Team", metric]].copy()
    plot_data = plot_data.dropna(subset=[metric])
    if plot_data.empty:
        fig, ax = plt.subplots(figsize=(10.8, 2.4))
        ax.axis("off")
        ax.set_title(title, loc="left", fontweight="bold", pad=12)
        ax.text(0.0, 0.5, "No valid data available", transform=ax.transAxes, fontsize=10, color="#666666")
        fig.tight_layout()
        plt.show()
        return
    plot_data = plot_data.sort_values(metric, ascending=lower_better).reset_index(drop=True)
    plot_data["Rank"] = np.arange(1, len(plot_data) + 1)
    plot_data["Performance score"] = score_metric(plot_data[metric], lower_better)
    plot_data["Label"] = plot_data.apply(
        lambda row: f"{int(row['Rank'])}. {row['Team']}", axis=1
    )

    fig_height = max(4.0, 0.42 * len(plot_data) + 1.35)
    fig, ax = plt.subplots(figsize=(10.8, fig_height))
    bar_colors = ranked_colors(plot_data["Performance score"])
    bars = ax.barh(
        plot_data["Label"],
        plot_data[metric],
        color=bar_colors,
        edgecolor="#2B2B2B",
        linewidth=0.45,
    )
    ax.invert_yaxis()
    ax.set_title(title, loc="left", fontweight="bold", pad=12)
    ax.set_xlabel(metric_labels.get(metric, metric))
    ax.set_ylabel("")
    ax.grid(axis="x")
    ax.grid(axis="y", visible=False)

    xmax = plot_data[metric].max(skipna=True)
    xmin = plot_data[metric].min(skipna=True)
    span = xmax - xmin if not np.isclose(xmax, xmin) else max(abs(xmax), 1)
    ax.set_xlim(left=0, right=xmax + span * 0.22)

    for i, (bar, value) in enumerate(zip(bars, plot_data[metric])):
        rank = int(plot_data.loc[i, "Rank"])
        emphasis = "Best" if rank == 1 else ""
        label = value_text(value, unit)
        if emphasis:
            label = f"{label}  {emphasis}"
        ax.text(
            bar.get_width() + span * 0.025,
            bar.get_y() + bar.get_height() / 2,
            label,
            va="center",
            ha="left",
            fontsize=9,
            fontweight="bold" if emphasis else "normal",
            color="#222222",
        )

    for tick in ax.get_yticklabels():
        if tick.get_text().startswith("1. "):
            tick.set_fontweight("bold")
            tick.set_color("#145A32")

    fig.tight_layout()
    plt.show()


def heatmap_colors(values, lower_better=False):
    series = pd.Series(values, dtype="float64")
    scores = score_metric(series, lower_better=lower_better)
    return ranked_colors(scores)

def draw_value_heatmap(data, columns, title, lower_better_map, value_formatters=None, row_order=None, wrap_headers=False, white_text_dark_green=False):
    if row_order is not None:
        plot_data = data.set_index("Team").loc[row_order].reset_index()
    else:
        plot_data = data.copy()

    n_rows = len(plot_data)
    n_cols = len(columns)
    fig_width = max(14.0, 1.48 * n_cols)
    fig_height = max(5.2, 0.46 * n_rows + 1.8)
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    ax.set_xlim(0, n_cols)
    ax.set_ylim(0, n_rows)
    ax.invert_yaxis()
    ax.set_facecolor("white")

    for row_idx, row in plot_data.iterrows():
        for col_idx, col in enumerate(columns):
            value = row[col]
            color = "#D9D9D9"
            text_color = "#1F1F1F"
            if pd.notna(value):
                column_scores = score_metric(plot_data[col], lower_better=lower_better_map.get(col, False))
                cell_score = column_scores.iloc[row_idx]
                color = ranked_colors(column_scores)[row_idx]
                if white_text_dark_green and pd.notna(cell_score):
                    r, g, b, _ = color
                    luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b
                    if g > r and g > b and luminance < 0.46:
                        text_color = "white"
                elif pd.notna(cell_score) and cell_score >= 99.5:
                    text_color = "white"
            rect = plt.Rectangle(
                (col_idx, row_idx),
                1,
                1,
                facecolor=color,
                edgecolor="white",
                linewidth=1.4,
            )
            ax.add_patch(rect)
            formatter = value_formatters.get(col, value_text) if value_formatters else value_text
            ax.text(
                col_idx + 0.5,
                row_idx + 0.5,
                formatter(value),
                ha="center",
                va="center",
                fontsize=8.2,
                color=text_color,
                fontweight="bold" if pd.notna(value) else "normal",
            )

    header_labels = [
        "\n".join(textwrap.wrap(col, width=18, break_long_words=False)) if wrap_headers else col
        for col in columns
    ]
    ax.set_xticks(np.arange(n_cols) + 0.5)
    ax.set_xticklabels(header_labels, rotation=0 if wrap_headers else 25, ha="center")
    ax.xaxis.tick_top()
    ax.tick_params(axis="x", labeltop=True, labelbottom=False, pad=8)
    ax.set_yticks(np.arange(n_rows) + 0.5)
    ax.set_yticklabels(plot_data["Team"])
    ax.tick_params(length=0)
    ax.set_title(title, loc="left", fontweight="bold", pad=18)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.grid(False)
    fig.tight_layout()
    plt.show()

def score_text(value):
    return "NaN" if pd.isna(value) else f"{value:.1f}"

def score_chart(data, metric, title):
    plot_data = data[["Team", metric]].dropna().sort_values(metric, ascending=False).reset_index(drop=True)
    plot_data["Rank"] = np.arange(1, len(plot_data) + 1)
    plot_data["Label"] = plot_data.apply(lambda row: f"{int(row['Rank'])}. {row['Team']}", axis=1)
    fig_height = max(4.0, 0.42 * len(plot_data) + 1.35)
    fig, ax = plt.subplots(figsize=(10.8, fig_height))
    bars = ax.barh(
        plot_data["Label"],
        plot_data[metric],
        color=ranked_colors(plot_data[metric]),
        edgecolor="#2B2B2B",
        linewidth=0.45,
    )
    ax.invert_yaxis()
    ax.set_xlim(0, 112)
    ax.set_title(title, loc="left", fontweight="bold", pad=12)
    ax.set_xlabel("Score (0-100)")
    ax.set_ylabel("")
    ax.grid(axis="x")
    ax.grid(axis="y", visible=False)
    for i, (bar, value) in enumerate(zip(bars, plot_data[metric])):
        rank = int(plot_data.loc[i, "Rank"])
        emphasis = "Best" if rank == 1 else ""
        label = f"{value:.1f}"
        if emphasis:
            label = f"{label}  {emphasis}"
        ax.text(
            bar.get_width() + 1.6,
            bar.get_y() + bar.get_height() / 2,
            label,
            va="center",
            ha="left",
            fontsize=9,
            fontweight="bold" if emphasis else "normal",
            color="#222222",
        )
    for tick in ax.get_yticklabels():
        if tick.get_text().startswith("1. "):
            tick.set_fontweight("bold")
            tick.set_color("#145A32")
    fig.tight_layout()
    plt.show()

print("Cleaned benchmark dataset")
display(df.round(4))


beat_summary_columns = [
    "F2C Height office floor [m]",
    "Floor Buildup [m]",
    "Total office area [m2]",
    "Permanent workspaces",
    "Average Facade Transparency",
    "Minimum height in office space [m]",
    "Sustainability BEAT",
    "Core vs Usable Space Ratio",
    "Cost",
    "Hours",
]
beat_summary_titles = {
    "F2C Height office floor [m]": "F2C Height Office Floor [m]",
    "Floor Buildup [m]": "Floor Buildup (F2F Height - F2C Height) [m]",
    "Total office area [m2]": "Total Office Area [m²]",
    "Total desks": "Total Desks",
    "Permanent workspaces": "Permanent Workspaces",
    "Average Facade Transparency": "Average Facade Transparency",
    "Minimum height in office space [m]": "Minimum Height in Office Space (Floor-to-Ceiling) [m]",
    "Sustainability BEAT": "[(CO²·kg/m²/year)·Total Office Area (m²)] / Permanent Desks",
    "Core vs Usable Space Ratio": "Core vs Usable Space Ratio",
    "Cost": "Cost",
    "Hours": "Hours",
}
beat_summary = df[["Team"] + beat_summary_columns].rename(columns=beat_summary_titles)
beat_lower_better = {
    beat_summary_titles[col]: (col in lower_is_better)
    for col in beat_summary_columns
}

print("Dashboard 1 - BEAT Benchmark Summary")
draw_value_heatmap(
    beat_summary,
    [beat_summary_titles[col] for col in beat_summary_columns],
    "BEAT Benchmark Summary",
    beat_lower_better,
    wrap_headers=True,
    white_text_dark_green=True,
)

summary_score_df = df[["Team"]].copy()
for metric in lower_is_better:
    summary_score_df[metric + " score"] = score_metric(df[metric], lower_better=True)
for metric in higher_is_better:
    summary_score_df[metric + " score"] = score_metric(df[metric], lower_better=False)

summary_category_metrics = {
    "Sustainability": ["Sustainability BEAT score"],
    "Cost": ["Cost score"],
    "Productivity": ["Hours score"],
    "Space Efficiency": [
        "Total office area [m2] score",
        "Permanent workspaces score",
        "Core vs Usable Space Ratio score",
    ],
    "Space Quality": [
        f"{f2f_col} score",
        "F2C Height office floor [m] score",
        "Minimum height in office space [m] score",
        "Floor Buildup [m] score",
        "Average Facade Transparency score",
    ],
}

category_summary = summary_score_df[["Team"]].copy()
for category, metrics in summary_category_metrics.items():
    category_summary[category] = summary_score_df[metrics].mean(axis=1, skipna=True)
category_summary["Overall Benchmark Score"] = category_summary[list(summary_category_metrics)].mean(axis=1, skipna=True)
category_summary_columns = [
    "Sustainability",
    "Cost",
    "Productivity",
    "Space Efficiency",
    "Space Quality",
    "Overall Benchmark Score",
]
category_summary = category_summary.sort_values("Overall Benchmark Score", ascending=False).reset_index(drop=True)

print("Dashboard 2 - Normalized Category Score Summary (0-100)")
draw_value_heatmap(
    category_summary,
    category_summary_columns,
    "Normalized Category Score Summary (0-100)",
    {col: False for col in category_summary_columns},
    value_formatters={col: score_text for col in category_summary_columns},
    wrap_headers=True,
)

print("Step 1 - Raw Benchmark Comparison")
raw_charts = [
    (f2f_col, "F2F office floor [m]", " m", False),
    ("F2C Height office floor [m]", "F2C Height Office Floor [m]", " m", False),
    ("Floor Buildup [m]", "Floor Buildup (F2F Height - F2C Height) [m]", " m", True),
    ("Total office area [m2]", "Total Office Area [mÂ²]", " m2", False),
    ("Total desks", "Total Desks", "", False),
    ("Permanent workspaces", "Permanent Workspaces", "", False),
    ("Average Facade Transparency", "Average Facade Transparency", "", True),
    ("Minimum height in office space [m]", "Minimum Height in Office Space (Floor-to-Ceiling) [m]", " m", False),
    ("Sustainability BEAT", "[(CO²kg/m²/year)·Total Office Area (m²)] / Permanent Desks", "", True),
    ("Core vs Usable Space Ratio", "Core vs Usable Space Ratio", "", True),
    ("Cost", "Cost", "", True),
    ("Hours", "Hours", "", True),
]

for metric, title, unit, lower_better in raw_charts:
    ranked_benchmark_chart(
        df,
        metric,
        title,
        unit=unit,
        lower_better=lower_better,
    )

print("Step 2 - Category Scoring")
score_df = df[["Team"]].copy()
for metric in lower_is_better:
    score_df[metric + " score"] = score_metric(df[metric], lower_better=True)
for metric in higher_is_better:
    score_df[metric + " score"] = score_metric(df[metric], lower_better=False)

category_metrics = {
    "Sustainability": ["Sustainability BEAT score"],
    "Cost": ["Cost score"],
    "Productivity": ["Hours score"],
    "Space Efficiency": [
        "Total office area [m2] score",
        "Permanent workspaces score",
        "Core vs Usable Space Ratio score",
    ],
    "Space Quality": [
        f"{f2f_col} score",
        "F2C Height office floor [m] score",

        "Minimum height in office space [m] score",
        "Floor Buildup [m] score",
        "Average Facade Transparency score",
    ],
}

category_scores = score_df[["Team"]].copy()
for category, metrics in category_metrics.items():
    category_scores[category] = score_df[metrics].mean(axis=1, skipna=True)
category_scores["Overall score"] = category_scores[list(category_metrics)].mean(axis=1, skipna=True)
ranking = category_scores.sort_values("Overall score", ascending=False).reset_index(drop=True)
ranking.insert(0, "Rank", np.arange(1, len(ranking) + 1))

display(ranking.round(2))

part2_titles = {
    "Sustainability": "Normalized Sustainability Score (CO² per Permanent Workspace)",
    "Cost": "Normalized Cost Score (Project Cost)",
    "Productivity": "Normalized Productivity Score (Total Design Hours)",
    "Space Efficiency": "Normalized Space Efficiency Score (Office Area, Permanent Workspaces, Core Ratio)",
    "Space Quality": "Normalized Space Quality Score (F2F Height, F2C Height, Minimum Office Height, Floor Buildup, Facade Transparency)",
}

for category in category_metrics:
    score_chart(category_scores, category, part2_titles[category])

score_chart(category_scores, "Overall score", "Overall Benchmark Score (Combined Category Performance)")

radar_categories = list(category_metrics)
radar_data = category_scores.set_index("Team")[radar_categories]
angles = np.linspace(0, 2 * np.pi, len(radar_categories), endpoint=False).tolist()
angles += angles[:1]

fig, ax = plt.subplots(figsize=(8.6, 8.6), subplot_kw={"projection": "polar"})
line_colors = plt.cm.tab10(np.linspace(0, 1, len(radar_data)))
for color, (team, values) in zip(line_colors, radar_data.iterrows()):
    vals = values.fillna(0).tolist()
    vals += vals[:1]
    ax.plot(angles, vals, label=team, linewidth=1.5, color=color)
    ax.fill(angles, vals, color=color, alpha=0.035)

ax.set_title("Radar Comparison: Category Scores", loc="left", fontweight="bold", pad=24)
ax.set_xticks(angles[:-1])
ax.set_xticklabels(radar_categories)
ax.set_ylim(0, 100)
ax.set_yticks([20, 40, 60, 80, 100])
ax.set_yticklabels(["20", "40", "60", "80", "100"])
ax.legend(loc="upper left", bbox_to_anchor=(1.05, 1.02), frameon=False)
fig.tight_layout()
plt.show()








