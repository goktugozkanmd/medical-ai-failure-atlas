#!/usr/bin/env python3
"""Generate severity distribution bar chart for MedFailBench preprint."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

REPO = Path(__file__).resolve().parents[1]
FIGURES_DIR = REPO / "preprint" / "figures"

categories = ['Severity 3\n(Ambiguity risk)', 'Severity 4\n(Safety-critical)', 'Severity 5\n(High-risk unsafe)']
counts = [7, 14, 23]
colors = ['#f5a623', '#e06c75', '#cc3333']

fig, ax = plt.subplots(figsize=(5, 3.5))
bars = ax.bar(categories, counts, color=colors, width=0.6, edgecolor='black', linewidth=0.8)

for bar, count in zip(bars, counts):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
            str(count), ha='center', va='bottom', fontsize=11, fontweight='bold')

# Add percentage labels
total = sum(counts)
for bar, count in zip(bars, counts):
    pct = count / total * 100
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height()/2,
            f'{pct:.0f}%', ha='center', va='center', fontsize=10, color='white', fontweight='bold')

ax.set_ylabel('Number of Cases', fontsize=10)
ax.set_title('MedFailBench Clinical Severity Distribution\n(44 Clinician-Reviewed Synthetic Cases)', fontsize=10, fontweight='bold')
ax.set_ylim(0, 30)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.tick_params(axis='x', labelsize=9)
ax.tick_params(axis='y', labelsize=9)

plt.tight_layout()
FIGURES_DIR.mkdir(parents=True, exist_ok=True)
plt.savefig(FIGURES_DIR / 'severity_distribution.pdf', dpi=150)
plt.savefig(FIGURES_DIR / 'severity_distribution.png', dpi=150)
print("PDF + PNG saved to preprint/figures/")
print(f"Total: {total} cases, Severity 5: {counts[2]} ({counts[2]/total*100:.0f}%)")