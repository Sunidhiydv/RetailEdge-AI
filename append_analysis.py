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
            "### 5. Cost Leadership Analysis\n",
            "We analyze the core categories to understand price positioning by calculating the `Price_Competitiveness_Index`."
        ]
    }

    new_code_cell = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "import matplotlib.pyplot as plt\n",
            "import seaborn as sns\n",
            "\n",
            "# 1. Identify the Top 10 product categories by volume\n",
            "top_10_categories = master_df['product_category_name_english'].value_counts().nlargest(10).index\n",
            "print(f\"Top 10 Categories: {list(top_10_categories)}\\n\")\n",
            "\n",
            "cost_leadership_df = master_df[master_df['product_category_name_english'].isin(top_10_categories)].copy()\n",
            "\n",
            "# 2. Calculate average price and average freight value\n",
            "category_stats = cost_leadership_df.groupby('product_category_name_english')[['price', 'freight_value']].mean().reset_index()\n",
            "category_stats.rename(columns={'price': 'avg_price', 'freight_value': 'avg_freight_value'}, inplace=True)\n",
            "print(\"Average Price & Freight Value for Top 10 Categories:\")\n",
            "print(category_stats)\n",
            "\n",
            "# 3. Create Price_Competitiveness_Index\n",
            "# First calculate median price per category\n",
            "category_medians = cost_leadership_df.groupby('product_category_name_english')['price'].median().reset_index()\n",
            "category_medians.rename(columns={'price': 'category_median_price'}, inplace=True)\n",
            "\n",
            "# Merge medians back onto our df\n",
            "cost_leadership_df = cost_leadership_df.merge(category_medians, on='product_category_name_english', how='left')\n",
            "\n",
            "# Calculate Price_Competitiveness_Index (Product Price / Category Median Price)\n",
            "cost_leadership_df['Price_Competitiveness_Index'] = cost_leadership_df['price'] / cost_leadership_df['category_median_price']\n",
            "\n",
            "# 4. Visualize the index using a Seaborn Boxplot\n",
            "plt.figure(figsize=(12, 8))\n",
            "sns.boxplot(\n",
            "    data=cost_leadership_df, \n",
            "    y='product_category_name_english', \n",
            "    x='Price_Competitiveness_Index', \n",
            "    palette='viridis',\n",
            "    orient='h',\n",
            "    showfliers=False # Hide extreme outliers to better visualize the competitive spread\n",
            ")\n",
            "\n",
            "plt.axvline(x=1, color='red', linestyle='--', linewidth=2, label='Category Median (Index = 1)')\n",
            "plt.title('Cost Leadership: Price Competitiveness Index by Top 10 Categories', fontsize=14, fontweight='bold')\n",
            "plt.ylabel('Product Category (English)', fontsize=12)\n",
            "plt.xlabel('Price Competitiveness Index (Price / Category Median Price)', fontsize=12)\n",
            "plt.legend()\n",
            "plt.tight_layout()\n",
            "plt.show()\n"
        ]
    }

    # Don't add if already exists to avoid duplication in case of reruns
    has_analysis = any("Cost Leadership Analysis" in "".join(cell.get('source', [])) for cell in nb['cells'])
    
    if not has_analysis:
        nb['cells'].extend([new_markdown_cell, new_code_cell])
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(nb, f, indent=1)
        print("Notebook successfully updated.")
    else:
        print("Analysis cells already exist in the notebook.")
else:
    print(f"Error: {file_path} not found.")
