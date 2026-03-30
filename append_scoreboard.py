import json

notebook_path = 'd:\\advantageAnalysis\\prepare_olist_data.ipynb'

with open(notebook_path, 'r', encoding='utf-8') as f:
    notebook = json.load(f)

# check if we already appended
has_scoreboard = any('Competitive Advantage Scoreboard' in cell.get('source', [''])[0] for cell in notebook['cells'])

if has_scoreboard:
    print("Scoreboard already exists.")
else:
    markdown_cell = {
     "cell_type": "markdown",
     "metadata": {},
     "source": [
      "### 7. Competitive Advantage Scoreboard\n",
      "Bringing it all together: Total Revenue, Average Review Score, and Delivery Delay are normalized into a single `Competitive_Advantage_Score`.\n",
      "We limit the analysis to sellers with at least 10 orders to ensure statistical significance."
     ]
    }
    
    code_cell = {
     "cell_type": "code",
     "execution_count": None,
     "metadata": {},
     "outputs": [],
     "source": [
      "import pandas as pd\n",
      "import matplotlib.pyplot as plt\n",
      "import seaborn as sns\n",
      "from sklearn.preprocessing import MinMaxScaler\n",
      "\n",
      "# 1. Calculate Delivery Delay in days (Actual - Estimated)\n",
      "master_df['Delivery_Delay_Days'] = (master_df['order_delivered_customer_date'] - master_df['order_estimated_delivery_date']).dt.total_seconds() / (24 * 3600)\n",
      "\n",
      "# Filter for delivered orders with necessary data\n",
      "score_df = master_df.dropna(subset=['price', 'review_score', 'Delivery_Delay_Days']).copy()\n",
      "\n",
      "# 2. Group by seller_id\n",
      "seller_summary = score_df.groupby('seller_id').agg(\n",
      "    Total_Revenue=('price', 'sum'),\n",
      "    Avg_Price=('price', 'mean'),\n",
      "    Avg_Review_Score=('review_score', 'mean'),\n",
      "    Avg_Delivery_Delay=('Delivery_Delay_Days', 'mean'),\n",
      "    Total_Orders=('order_id', 'nunique')\n",
      ").reset_index()\n",
      "\n",
      "# Filter for sellers with at least 10 orders to reduce noise (1-order wonders)\n",
      "seller_summary = seller_summary[seller_summary['Total_Orders'] >= 10].copy()\n",
      "\n",
      "# 3. Normalize values using MinMaxScaler\n",
      "scaler = MinMaxScaler()\n",
      "\n",
      "# For Revenue and Review Score, higher is better\n",
      "seller_summary[['Rev_Norm', 'Revw_Norm']] = scaler.fit_transform(seller_summary[['Total_Revenue', 'Avg_Review_Score']])\n",
      "\n",
      "# For Delivery Delay, lower is better. We negate it before scaling so higher score = less delay\n",
      "seller_summary['Delay_Neg'] = -seller_summary['Avg_Delivery_Delay']\n",
      "seller_summary['Delay_Norm'] = scaler.fit_transform(seller_summary[['Delay_Neg']])\n",
      "\n",
      "# Combine into a single score (max possible score is 3.0)\n",
      "seller_summary['Competitive_Advantage_Score'] = seller_summary['Rev_Norm'] + seller_summary['Revw_Norm'] + seller_summary['Delay_Norm']\n",
      "\n",
      "# 4. Identify the Top 10 Sellers\n",
      "top_10_scoreboard = seller_summary.sort_values(by='Competitive_Advantage_Score', ascending=False).head(10)\n",
      "\n",
      "print(\"--- Top 10 Sellers by Competitive Advantage Score ---\")\n",
      "print(top_10_scoreboard[['seller_id', 'Total_Revenue', 'Avg_Review_Score', 'Avg_Delivery_Delay', 'Competitive_Advantage_Score']])\n",
      "\n",
      "# 5. Plot the Top 10 Sellers on a Scatter Plot\n",
      "plt.figure(figsize=(10, 7))\n",
      "\n",
      "# Bubble size scale factor \n",
      "bubble_sizes = (top_10_scoreboard['Total_Revenue'] / top_10_scoreboard['Total_Revenue'].max()) * 2000 \n",
      "\n",
      "scatter = plt.scatter(\n",
      "    x=top_10_scoreboard['Avg_Price'],\n",
      "    y=top_10_scoreboard['Avg_Review_Score'],\n",
      "    s=bubble_sizes,\n",
      "    c=top_10_scoreboard['Competitive_Advantage_Score'],\n",
      "    cmap='coolwarm',\n",
      "    alpha=0.7,\n",
      "    edgecolors='w',\n",
      "    linewidth=1.5\n",
      ")\n",
      "\n",
      "# Add a colorbar for the Score\n",
      "cbar = plt.colorbar(scatter)\n",
      "cbar.set_label('Competitive Advantage Score', fontsize=12)\n",
      "\n",
      "# Add labels and title\n",
      "plt.title('Top 10 Sellers: Avg Price vs. Avg Review Score (Bubble Size = Revenue)', fontsize=14, fontweight='bold')\n",
      "plt.xlabel('Average Item Price ($)', fontsize=12)\n",
      "plt.ylabel('Average Review Score', fontsize=12)\n",
      "plt.grid(True, linestyle='--', alpha=0.5)\n",
      "\n",
      "# Add seller IDs as text next to the bubbles for reference\n",
      "for i, row in top_10_scoreboard.iterrows():\n",
      "    plt.annotate(\n",
      "        row['seller_id'][:6] + '...',  # Show first 6 chars of seller_id to keep it clean\n",
      "        (row['Avg_Price'], row['Avg_Review_Score']),\n",
      "        fontsize=9,\n",
      "        ha='left',\n",
      "        va='bottom',\n",
      "        xytext=(5, 5),\n",
      "        textcoords='offset points'\n",
      "    )\n",
      "\n",
      "plt.tight_layout()\n",
      "plt.show()\n"
     ]
    }
    
    notebook['cells'].extend([markdown_cell, code_cell])
    
    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=1)
    
    print("Notebook updated with Competitive Advantage Scoreboard.")
