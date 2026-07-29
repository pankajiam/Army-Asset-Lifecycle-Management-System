# Army Asset Lifecycle Management System (AALMS) - Streamlit UI

A modern Streamlit frontend for the Army Asset Lifecycle Management System backend.

## Features

- 📊 **Command Center Dashboard**: Live KPIs, total inventory value, equipment distribution charts, and status breakdowns.
- 📦 **Asset Inventory**: Full CRUD view, search/filtering by category and status, registration of new weapons, vehicles, and equipment.
- 🏷️ **QR Code Generator**: On-demand streaming and downloading of QR tracking tags for assets.
- 🔄 **Equipment Custody Operations**: Issue equipment to officers, record returns with condition logs, direct custody transfer, and complete audit history.
- 📉 **Depreciation Engine**: Automated financial depreciation calculation for equipment lifecycle management.
- 🗑️ **Asset Disposal**: Request and approve decommissioning or scrapping of BER (Beyond Economical Repair) assets.
- 🎖️ **Personnel & Auth**: Officer login with JWT token integration and personnel registration.

---

## Quick Start Guide

### 1. Requirements & Dependencies

Make sure Python 3.10+ is installed. Install frontend requirements:

```bash
pip install -r frontend/requirements.txt
```

---

### 2. Start the Backend API

Navigate to the `backend` directory, activate your virtual environment (if using one), and run the FastAPI server:

```bash
cd backend
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

To seed initial roles, ranks, and units into the database:
```bash
python seed_database.py
```

---

### 3. Launch the Streamlit Frontend

In a separate terminal, run:

```bash
streamlit run frontend/app.py
```

The Streamlit UI will open automatically in your browser at `http://localhost:8501`.
