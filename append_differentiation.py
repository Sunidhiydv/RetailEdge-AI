import json
import os

file_path = r'd:\advantageAnalysis\prepare_olist_data.ipynb'
if os.path.exists(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    new_markdown_cell = {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### 6. Differentiation Advantage Analysis\n",
            "This section explores delivery speed and identifies \"Premium\" sellers who maintain high operational and review standards despite above-average pricing."
        ]
    }

    new_code_cell = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "import numpy as np\n",
            "\n",
            "# 1. Calculate Delivery_Speed (in days)\n",
            "master_df['Delivery_Speed_Days'] = (master_df['order_delivered_customer_date'] - master_df['order_purchase_timestamp']).dt.total_seconds() / (24 * 3600)\n",
            "\n",
            "# Drop NaN values for these specific columns to ensure clean correlation\n",
            "delivered_orders = master_df.dropna(subset=['Delivery_Speed_Days', 'review_score']).copy()\n",
            "\n",
            "# 2. Calculate the correlation between 'Delivery_Speed' and 'review_score'\n",
            "correlation = delivered_orders['Delivery_Speed_Days'].corr(delivered_orders['review_score'])\n",
            "print(f\"Correlation between Delivery Speed (Days) and Review Score: {correlation:.4f}\")\n",
            "print(\"Note: A negative correlation implies that as delivery time increases, the review score tends to decrease.\\n\")\n",
            "\n",
            "# 3. Identify Top 5 Sellers: High Ratings despite Above-Average Prices\n",
            "# Require a minimum of 10 order items to eliminate outliers with a single lucky 5-star review\n",
            "order_counts = delivered_orders['seller_id'].value_counts()\n",
            "valid_sellers = order_counts[order_counts >= 10].index \n",
            "\n",
            "seller_metrics = delivered_orders[delivered_orders['seller_id'].isin(valid_sellers)].groupby('seller_id').agg(\n",
            "    avg_price=('price', 'mean'),\n",
            "    avg_review_score=('review_score', 'mean'),\n",
            "    total_orders=('order_id', 'nunique')\n",
            ").reset_index()\n",
            "\n",
            "# Calculate the overall average seller price\n",
            "global_avg_price = seller_metrics['avg_price'].mean()\n",
            "print(f\"Global Average Seller Price: ${global_avg_price:.2f}\\n\")\n",
            "\n",
            "# Filter for Premium sellers (price higher than average)\n",
            "premium_sellers = seller_metrics[seller_metrics['avg_price'] > global_avg_price].copy()\n",
            "\n",
            "# Sort by highest review score, then by volume (total_orders)\n",
            "top_premium_sellers = premium_sellers.sort_values(by=['avg_review_score', 'total_orders'], ascending=[False, False])\n",
            "\n",
            "print(\"--- Top 5 Sellers With Premium Brand Advantage ---\")\n",
            "top_premium_sellers.head()\n"
        ]
    }
    
    # Don't add if already exists
    has_diff = any("Differentiation Advantage Analysis" in "".join(cell.get('source', [])) for cell in nb['cells'])
    
    if not has_diff:
        nb['cells'].extend([new_markdown_cell, new_code_cell])
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(nb, f, indent=1)
        print("Notebook updated with Differentiation Analysis.")
    else:
        print("Differentiation Analysis already exists.")
else:
    print(f"Error: {file_path} not found.")
