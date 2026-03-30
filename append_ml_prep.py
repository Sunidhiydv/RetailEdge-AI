import json

notebook_path = r"d:\advantageAnalysis\prepare_olist_data.ipynb"

# Load the notebook
with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Markdown cell
md_cell = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "### 8. Machine Learning Data Preparation\n",
        "Preparing the data for a Random Forest model to predict `review_score`.\n",
        "We'll create a feature matrix `X` and target vector `y`, fill any missing values with the median, and perform an 80/20 train-test split."
    ]
}

# Code cell
code_cell = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "from sklearn.model_selection import train_test_split\n",
        "\n",
        "# Define features to include\n",
        "features = ['price', 'freight_value', 'product_description_lenght', 'product_photos_qty', 'Delivery_Speed_Days']\n",
        "\n",
        "# Create the feature dataframe X and target variable y using master_df\n",
        "X = master_df[features].copy()\n",
        "y = master_df['review_score'].copy()\n",
        "\n",
        "# Handle remaining NaN values in X by filling them with the median of each column\n",
        "X = X.fillna(X.median())\n",
        "\n",
        "# Split the data into 80% training and 20% testing sets\n",
        "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)\n",
        "\n",
        "print(f\"Training Data Shape: X_train={X_train.shape}, y_train={y_train.shape}\")\n",
        "print(f\"Testing Data Shape: X_test={X_test.shape}, y_test={y_test.shape}\")\n"
    ]
}

# Append the new cells
nb['cells'].append(md_cell)
nb['cells'].append(code_cell)

# Save the updated notebook
with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

print("Notebook updated with Machine Learning Data Preparation.")
