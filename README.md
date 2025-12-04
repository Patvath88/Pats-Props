# Pats-Props
# Professional Player Prop ML Pipeline

This application is a complete, end-to-end machine learning pipeline for generating daily NBA player prop picks. It uses real-time market odds and a custom-trained prediction model to identify statistical edges.

**Core Architecture:**
-   **MLOps Workflow:** Uses **MLflow** for experiment tracking and model registry, separating the training process from daily predictions.
-   **Feature Engineering:** A robust pipeline transforms raw player data into meaningful features like rolling averages and opponent defensive stats.
-   **Model Training:** Employs a **LightGBM** model, which is trained weekly on the latest historical data.
-   **Daily Inference:** Loads the "production" model from the registry to generate predictions for players playing today.
-   **Efficient API Usage:** Caches API calls to a local SQLite database to stay within free-tier limits.
-   **Interactive UI:** A Streamlit application provides a user-friendly interface to view the daily picks.

---

### 1. Setup Instructions

**A. Clone the Repository & Install Dependencies**

```bash
# Create your project directory
mkdir prop-picks-app
cd prop-picks-app

# Install Python libraries
pip install -r requirements.txt
