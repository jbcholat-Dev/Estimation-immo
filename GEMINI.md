# GEMINI.md

## Project Overview

This project is a real estate estimation application for the Haute-Savoie region of France (74), specifically the Chablais/Annemasse area. It is built as a Streamlit MVP to reduce estimation time significantly.

The application is structured around a series of "EPICs" (large user stories), with the first EPIC focusing on finding comparable properties from DVF+ data. It uses a multi-criteria scoring algorithm to find and rank comparable properties.

### Key Technologies

*   **Backend:** Python 3.10+
*   **Frontend:** Streamlit
*   **Database:** Supabase (PostgreSQL with PostGIS)
*   **Data Analysis:** Pandas, NumPy
*   **Geospatial:** Folium, Google Maps API
*   **Visualization:** Plotly, Folium
*   **PDF Generation:** ReportLab
*   **Testing:** Pytest

### Architecture

The application has been restructured to use `main.py` as the entry point, which manages navigation between different EPICs presented as tabs. The core business logic for the first EPIC is encapsulated in `src/ui/epic_1_dvf.py`.

*   `main.py`: The new main entry point for the Streamlit application, featuring a tab-based navigation.
*   `app.py`: Legacy entry point, kept for reference.
*   `src/ui/epic_1_dvf.py`: Module containing the UI and logic for EPIC 1 (DVF+ Comparables).
*   `src/supabase_data_retriever.py`: Handles data retrieval from the Supabase database using optimized PostGIS queries.
*   `src/estimation_algorithm.py`: Contains the core logic for the property estimation algorithm.
*   `src/streamlit_components/`: Reusable UI components for the Streamlit interface.
*   `src/utils/`: Utility functions, including `finance.py` for monetary calculations and `geocoding.py`.

## Building and Running

### Prerequisites

*   Python 3.10+
*   `pip` for installing Python packages.
*   A valid `.env` file with API keys for Supabase and Google Maps (see `PROJECT_STATUS.md` or `.env.example`).

### Installation

1.  **Navigate to the project directory:**

    ```bash
    cd C:\Users\jbcho\Estimation-immo-1
    ```

2.  **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

3.  **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

To run the Streamlit application, use the new entry point `main.py`:

```bash
streamlit run main.py
```

## Development

### Running Tests

The project uses `pytest` for testing. As of the last update, 22 out of 39 tests are passing.

```bash
pytest tests/
```

### Code Style and Linting

The project uses `black` for code formatting and `ruff` for linting.

*   **Format code:**

    ```bash
    black .
    ```

*   **Lint code:**

    ```bash
    ruff check .
    ```

### Project Structure

```
├── main.py                          # ✨ New entry point
├── app.py                           # ⚠️ Legacy entry point
├── requirements.txt                 # Python dependencies
├── src/
│   ├── ui/
│   │   └── epic_1_dvf.py            # ✨ EPIC 1 UI module
│   ├── streamlit_components/      # Reusable UI components
│   ├── supabase_data_retriever.py   # Data retrieval logic
│   ├── estimation_algorithm.py    # Estimation logic
│   └── utils/
│       ├── finance.py               # ✨ Financial calculations
│       └── geocoding.py
├── tests/                           # Unit and integration tests
├── docs/
│   └── Specs/                       # Project specifications per EPIC
└── ...
```