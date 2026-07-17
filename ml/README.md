# Machine Learning Project Workflow

This project utilizes a powerful stack of Python libraries to handle everything from low-level mathematical operations to full machine learning lifecycle management.

## Tech Stack Overview

*   **NumPy:** Performs the underlying mathematical calculations.
*   **Pandas:** Structures your raw data into tables for cleaning.
*   **Scikit-Learn:** Uses that cleaned data to train a machine learning model.
*   **MLflow:** Logs the performance of that model and saves it for production.

---

### The Workflow Pipeline

```text
[ Raw Data ] ──> (NumPy & Pandas) ──> [ Cleaned Data ] ──> (Scikit-Learn) ──> [ Trained Model ] ──> (MLflow) ──> [ Production Deployment ]
```
