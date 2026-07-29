import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime
from PIL import Image
import io

# ---------------------------------------------------------
# Page Configuration & Modern Military Aesthetic Styling
# ---------------------------------------------------------
st.set_page_config(
    page_title="Army Asset Lifecycle Management System (AALMS)",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern dark-slate military dashboard styling
st.markdown("""
    <style>
        /* Main background and fonts */
        .stApp {
            background-color: #0d1117;
            color: #c9d1d9;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        /* Sidebar styling */
        section[data-testid="stSidebar"] {
            background-color: #161b22;
            border-right: 1px solid #30363d;
        }
        
        /* Metric cards custom look */
        div[data-testid="stMetric"] {
            background-color: #21262d;
            border: 1px solid #30363d;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        }
        div[data-testid="stMetric"] label {
            color: #8b949e !important;
            font-weight: 600;
        }
        div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
            color: #58a6ff !important;
            font-weight: bold;
        }
        
        /* Headers */
        h1, h2, h3, h4 {
            color: #f0f6fc !important;
            font-weight: 700;
        }
        
        /* Buttons */
        .stButton>button {
            background: linear-gradient(135deg, #1f6feb 0%, #1158c7 100%);
            color: #ffffff;
            font-weight: 600;
            border: none;
            border-radius: 6px;
            padding: 0.5rem 1rem;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background: linear-gradient(135deg, #388bfd 0%, #1f6feb 100%);
            box-shadow: 0 0 10px rgba(56, 139, 253, 0.4);
            color: #ffffff;
        }

        /* Success & Info Alerts */
        .stAlert {
            border-radius: 6px;
        }
        
        /* Badge pill design */
        .status-badge {
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 0.8rem;
            font-weight: 600;
            display: inline-block;
        }
        .badge-available { background-color: #238636; color: #ffffff; }
        .badge-assigned { background-color: #9e6a03; color: #ffffff; }
        .badge-disposed { background-color: #da3633; color: #ffffff; }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Session State Initialization
# ---------------------------------------------------------
if "backend_url" not in st.session_state:
    st.session_state.backend_url = "http://127.0.0.1:8000"

if "token" not in st.session_state:
    st.session_state.token = None

if "user_info" not in st.session_state:
    st.session_state.user_info = None

# ---------------------------------------------------------
# API Helper Functions
# ---------------------------------------------------------
def get_backend_url(endpoint: str) -> str:
    base = st.session_state.backend_url.rstrip("/")
    return f"{base}/{endpoint.lstrip('/')}"

def check_backend_health():
    try:
        res = requests.get(get_backend_url("/health"), timeout=3)
        return res.status_code == 200, res.json() if res.status_code == 200 else None
    except Exception:
        return False, None

def check_db_health():
    try:
        res = requests.get(get_backend_url("/db-test"), timeout=3)
        return res.status_code == 200, res.json() if res.status_code == 200 else None
    except Exception:
        return False, None

def fetch_all_assets():
    try:
        res = requests.get(get_backend_url("/assets/"), timeout=5)
        if res.status_code == 200:
            return res.json()
        return []
    except Exception as e:
        st.error(f"Failed to fetch assets: {e}")
        return []

# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------
st.sidebar.markdown("## 🛡️ **AALMS Portal**")
st.sidebar.caption("Army Asset Lifecycle Management System")
st.sidebar.divider()

# Backend status panel
backend_ok, health_data = check_backend_health()
db_ok, db_data = check_db_health()

status_col1, status_col2 = st.sidebar.columns(2)
with status_col1:
    if backend_ok:
        st.success("API: Online 🟢")
    else:
        st.error("API: Offline 🔴")

with status_col2:
    if db_ok:
        st.success("DB: Ready 🟢")
    else:
        st.error("DB: Error 🔴")

st.sidebar.divider()

# Backend Configuration
with st.sidebar.expander("⚙️ Server Configuration"):
    custom_url = st.text_input("FastAPI Backend URL", value=st.session_state.backend_url)
    if custom_url != st.session_state.backend_url:
        st.session_state.backend_url = custom_url
        st.rerun()

# User Session Banner
if st.session_state.token:
    st.sidebar.info(f"👤 Logged in as: **{st.session_state.user_info or 'Army Officer'}**")
    if st.sidebar.button("🚪 Logout"):
        st.session_state.token = None
        st.session_state.user_info = None
        st.rerun()
else:
    st.sidebar.warning("🔒 Not logged in (Guest View)")

st.sidebar.divider()

# Main Navigation
nav_option = st.sidebar.radio(
    "Navigation Menu",
    [
        "📊 Dashboard",
        "📦 Asset Registry",
        "🏷️ QR Code Scanner",
        "🔄 Issue & Transfer",
        "📉 Depreciation Calculator",
        "🗑️ Asset Disposal",
        "🎖️ Personnel & Auth"
    ]
)

st.sidebar.markdown("---")
st.sidebar.caption("Indian Army Inventory Control • Confidential")

# ---------------------------------------------------------
# Tab 1: Dashboard Overview
# ---------------------------------------------------------
if nav_option == "📊 Dashboard":
    st.title("🛡️ Command Center & Asset Metrics")
    st.markdown("Real-time operational summary of defense inventory, equipment allocation, and asset lifecycle stats.")
    
    assets = fetch_all_assets()
    
    # KPI Metrics
    total_assets = len(assets)
    available_assets = len([a for a in assets if a.get("status") == "Available"])
    assigned_assets = len([a for a in assets if a.get("status") == "Assigned" or a.get("assigned_to") is not None])
    disposed_assets = len([a for a in assets if a.get("status") == "Disposed"])
    
    total_val = sum(float(a.get("current_value") or a.get("purchase_price") or 0) for a in assets)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Equipment Items", f"{total_assets:,}")
    col2.metric("Available in Depot", f"{available_assets:,}")
    col3.metric("Currently Issued", f"{assigned_assets:,}")
    col4.metric("Total Inventory Value", f"₹ {total_val:,.2f}")
    
    st.divider()
    
    if assets:
        df = pd.DataFrame(assets)
        
        c1, c2 = st.columns([1, 1])
        
        with c1:
            st.subheader("Asset Distribution by Category")
            cat_counts = df['category'].value_counts().reset_index()
            cat_counts.columns = ['Category', 'Count']
            fig_pie = px.pie(
                cat_counts,
                values='Count',
                names='Category',
                color_discrete_sequence=px.colors.sequential.Darkmint_r,
                hole=0.4
            )
            fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#c9d1d9")
            st.plotly_chart(fig_pie, use_container_width=True)
            
        with c2:
            st.subheader("Equipment Status Overview")
            status_counts = df['status'].value_counts().reset_index()
            status_counts.columns = ['Status', 'Count']
            fig_bar = px.bar(
                status_counts,
                x='Status',
                y='Count',
                color='Status',
                color_discrete_sequence=px.colors.qualitative.Bold
            )
            fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#c9d1d9")
            st.plotly_chart(fig_bar, use_container_width=True)

        st.subheader("📋 Recent Asset Inventory")
        preview_df = df[['asset_id', 'asset_code', 'asset_name', 'category', 'status', 'current_value']].head(10)
        st.dataframe(preview_df, use_container_width=True)

    else:
        st.info("No asset records found in the database. Use the 'Asset Registry' tab to add your first military asset.")

# ---------------------------------------------------------
# Tab 2: Asset Registry & Creation
# ---------------------------------------------------------
elif nav_option == "📦 Asset Registry":
    st.title("📦 Military Asset Registry")
    st.write("Browse, filter, and register new army equipment into the system.")
    
    tab_list, tab_create = st.tabs(["📋 View & Filter Inventory", "➕ Register New Asset"])
    
    with tab_list:
        assets = fetch_all_assets()
        if assets:
            df = pd.DataFrame(assets)
            
            # Filters
            f_col1, f_col2, f_col3 = st.columns(3)
            with f_col1:
                search_term = st.text_input("🔍 Search Code/Name/Serial", "")
            with f_col2:
                categories = ["All"] + list(df["category"].dropna().unique())
                selected_cat = st.selectbox("Filter Category", categories)
            with f_col3:
                statuses = ["All"] + list(df["status"].dropna().unique())
                selected_status = st.selectbox("Filter Status", statuses)
                
            filtered_df = df.copy()
            if search_term:
                filtered_df = filtered_df[
                    filtered_df['asset_name'].astype(str).str.contains(search_term, case=False) |
                    filtered_df['asset_code'].astype(str).str.contains(search_term, case=False) |
                    filtered_df['serial_number'].astype(str).str.contains(search_term, case=False)
                ]
            if selected_cat != "All":
                filtered_df = filtered_df[filtered_df['category'] == selected_cat]
            if selected_status != "All":
                filtered_df = filtered_df[filtered_df['status'] == selected_status]

            st.markdown(f"Displaying **{len(filtered_df)}** of **{len(df)}** registered assets.")
            st.dataframe(filtered_df, use_container_width=True)
        else:
            st.warning("No assets found.")

    with tab_create:
        st.subheader("➕ Register New Equipment")
        with st.form("new_asset_form"):
            c1, c2 = st.columns(2)
            with c1:
                asset_code = st.text_input("Asset Code *", placeholder="e.g. AST-INSAS-001")
                asset_name = st.text_input("Asset Name *", placeholder="e.g. INSAS Rifle 5.56mm")
                category = st.selectbox("Category *", ["Weapons", "Vehicles", "Communication", "Optics", "Armour", "IT Equipment", "Medical", "General"])
                manufacturer = st.text_input("Manufacturer", placeholder="e.g. Ordnance Factory Board")
                model = st.text_input("Model Name / Number", placeholder="e.g. 1B1 INSAS")
            with c2:
                serial_number = st.text_input("Serial Number", placeholder="e.g. SN-987654321")
                purchase_date = st.date_input("Purchase Date", value=datetime.today())
                purchase_price = st.number_input("Purchase Price (₹)", min_value=0.0, step=500.0, value=75000.0)
                current_value = st.number_input("Initial Current Value (₹)", min_value=0.0, step=500.0, value=75000.0)
                status = st.selectbox("Initial Status", ["Available", "Assigned", "In Maintenance"])

            submitted = st.form_submit_button("🛡️ Submit Asset to Inventory")
            if submitted:
                if not asset_code or not asset_name:
                    st.error("Asset Code and Asset Name are required!")
                else:
                    payload = {
                        "asset_code": asset_code,
                        "asset_name": asset_name,
                        "category": category,
                        "manufacturer": manufacturer or None,
                        "model": model or None,
                        "serial_number": serial_number or None,
                        "purchase_date": purchase_date.strftime("%Y-%m-%d"),
                        "purchase_price": purchase_price,
                        "current_value": current_value,
                        "status": status,
                        "assigned_to": None
                    }
                    try:
                        res = requests.post(get_backend_url("/assets/"), json=payload, timeout=5)
                        if res.status_code in [200, 201]:
                            st.success(f"Asset '{asset_name}' ({asset_code}) registered successfully!")
                            st.json(res.json())
                        else:
                            st.error(f"Failed to register asset: {res.text}")
                    except Exception as e:
                        st.error(f"Request error: {e}")

# ---------------------------------------------------------
# Tab 3: QR Code Scanner / Generator
# ---------------------------------------------------------
elif nav_option == "🏷️ QR Code Scanner":
    st.title("🏷️ Asset QR Code Generator")
    st.write("Generate and view barcode/QR tag for equipment tracking.")

    assets = fetch_all_assets()
    if not assets:
        st.info("No assets available to generate QR code.")
    else:
        asset_options = {f"{a['asset_code']} - {a['asset_name']} (ID: {a['asset_id']})": a['asset_id'] for a in assets}
        selected_label = st.selectbox("Select Equipment Item", list(asset_options.keys()))
        selected_id = asset_options[selected_label]

        if st.button("🔍 Fetch / Generate QR Code"):
            qr_url = get_backend_url(f"/assets/{selected_id}/qr")
            try:
                res = requests.get(qr_url, timeout=5)
                if res.status_code == 200:
                    image_bytes = res.content
                    image = Image.open(io.BytesIO(image_bytes))
                    
                    q_col1, q_col2 = st.columns([1, 2])
                    with q_col1:
                        st.image(image, caption=f"QR Tag for Asset ID: {selected_id}", width=250)
                    with q_col2:
                        st.success("QR Code stream fetched successfully!")
                        st.write("**Details encoded in QR:**")
                        matching_asset = next((a for a in assets if a['asset_id'] == selected_id), {})
                        st.json(matching_asset)
                        st.download_button(
                            label="💾 Download QR Image",
                            data=image_bytes,
                            file_name=f"QR_Asset_{selected_id}.png",
                            mime="image/png"
                        )
                else:
                    st.error(f"Could not load QR code. Server returned HTTP {res.status_code}: {res.text}")
            except Exception as e:
                st.error(f"Error fetching QR code: {e}")

# ---------------------------------------------------------
# Tab 4: Issue, Return & Transfer Operations
# ---------------------------------------------------------
elif nav_option == "🔄 Issue & Transfer":
    st.title("🔄 Equipment Custody & Assignment Lifecycle")
    st.write("Issue equipment to personnel, record returns, or execute direct transfer.")

    tab_issue, tab_return, tab_transfer, tab_history = st.tabs([
        "📤 Issue Equipment",
        "📥 Return Equipment",
        "🔀 Transfer Equipment",
        "📜 Audit History"
    ])

    # Issue
    with tab_issue:
        st.subheader("Issue Equipment to Army Personnel")
        with st.form("issue_form"):
            asset_id = st.number_input("Asset ID *", min_value=1, step=1, value=1)
            user_id = st.number_input("Personnel User ID *", min_value=1, step=1, value=1)
            condition = st.selectbox("Issue Condition", ["New", "Good", "Fair", "Needs Maintenance"])
            
            sub_issue = st.form_submit_button("📤 Confirm Issue")
            if sub_issue:
                payload = {
                    "asset_id": int(asset_id),
                    "user_id": int(user_id),
                    "issue_condition": condition
                }
                res = requests.post(get_backend_url("/assignments/issue"), json=payload)
                if res.status_code in [200, 201]:
                    st.success("Asset issued successfully!")
                    st.json(res.json())
                else:
                    st.error(f"Failed to issue asset: {res.text}")

    # Return
    with tab_return:
        st.subheader("Record Equipment Return")
        with st.form("return_form"):
            asset_id_ret = st.number_input("Asset ID *", min_value=1, step=1, value=1)
            condition_ret = st.selectbox("Return Condition", ["Good", "Fair", "Damaged", "Needs Repair"])
            
            sub_return = st.form_submit_button("📥 Confirm Return")
            if sub_return:
                payload = {
                    "asset_id": int(asset_id_ret),
                    "return_condition": condition_ret
                }
                res = requests.post(get_backend_url("/assignments/return"), json=payload)
                if res.status_code in [200, 201]:
                    st.success("Asset returned successfully!")
                    st.json(res.json())
                else:
                    st.error(f"Failed to record return: {res.text}")

    # Transfer
    with tab_transfer:
        st.subheader("Transfer Custody to Another Officer")
        with st.form("transfer_form"):
            asset_id_tr = st.number_input("Asset ID *", min_value=1, step=1, value=1)
            new_user_id = st.number_input("New Recipient User ID *", min_value=1, step=1, value=2)
            condition_tr = st.selectbox("Transfer Condition", ["Good", "Fair", "Needs Repair"])

            sub_tr = st.form_submit_button("🔀 Execute Transfer")
            if sub_tr:
                payload = {
                    "asset_id": int(asset_id_tr),
                    "new_user_id": int(new_user_id),
                    "transfer_condition": condition_tr
                }
                res = requests.post(get_backend_url("/assignments/transfer"), json=payload)
                if res.status_code in [200, 201]:
                    st.success("Asset transferred successfully!")
                    st.json(res.json())
                else:
                    st.error(f"Failed to execute transfer: {res.text}")

    # Audit History
    with tab_history:
        st.subheader("📜 Equipment Custody Audit Trail")
        hist_asset_id = st.number_input("Enter Asset ID to Inspect History", min_value=1, step=1, value=1)
        if st.button("🔎 Fetch Audit Log"):
            res = requests.get(get_backend_url(f"/assignments/history/{hist_asset_id}"))
            if res.status_code == 200:
                history_data = res.json()
                if history_data:
                    st.success(f"Found {len(history_data)} assignment records.")
                    st.dataframe(pd.DataFrame(history_data), use_container_width=True)
                else:
                    st.info("No prior assignment history found for this asset.")
            else:
                st.error(f"Error fetching history: {res.text}")

# ---------------------------------------------------------
# Tab 5: Depreciation Calculator
# ---------------------------------------------------------
elif nav_option == "📉 Depreciation Calculator":
    st.title("📉 Asset Valuation & Depreciation Engine")
    st.write("Automate financial valuation recalculations based on asset lifecycle guidelines.")

    assets = fetch_all_assets()
    if not assets:
        st.info("No assets available for depreciation calculation.")
    else:
        df = pd.DataFrame(assets)
        st.dataframe(df[['asset_id', 'asset_code', 'asset_name', 'purchase_price', 'current_value', 'purchase_date']], use_container_width=True)

        st.divider()
        st.subheader("Run Depreciation Engine")
        
        dep_asset_id = st.number_input("Select Asset ID for Depreciation", min_value=1, max_value=1000, value=int(assets[0]['asset_id']))
        
        selected_item = next((a for a in assets if a['asset_id'] == dep_asset_id), None)
        if selected_item:
            st.info(f"Selected: **{selected_item['asset_name']}** ({selected_item['asset_code']}) | Current Value: **₹ {float(selected_item.get('current_value') or 0):,.2f}**")
        
        if st.button("⚡ Calculate & Apply Depreciation"):
            try:
                res = requests.post(get_backend_url(f"/assets/{dep_asset_id}/depreciate"))
                if res.status_code == 200:
                    updated_asset = res.json()
                    st.balloons()
                    st.success("Depreciation calculated and database updated successfully!")
                    
                    orig = float(updated_asset.get("purchase_price") or 0)
                    curr = float(updated_asset.get("current_value") or 0)
                    
                    st.metric("New Asset Value", f"₹ {curr:,.2f}", delta=f"₹ {curr - orig:,.2f}")
                    st.json(updated_asset)
                else:
                    st.error(f"Failed to recalculate depreciation: {res.text}")
            except Exception as e:
                st.error(f"Request error: {e}")

# ---------------------------------------------------------
# Tab 6: Asset Disposal Portal
# ---------------------------------------------------------
elif nav_option == "🗑️ Asset Disposal":
    st.title("🗑️ Asset Disposal & Decommissioning Portal")
    st.write("Submit requests for decommissioning or approve pending disposal requests.")

    t_req, t_app = st.tabs(["📝 Submit Disposal Request", "✅ Approve Disposal Request"])

    with t_req:
        st.subheader("Submit New Disposal Request")
        with st.form("disposal_req_form"):
            disp_asset_id = st.number_input("Asset ID *", min_value=1, step=1, value=1)
            req_by_id = st.number_input("Requested By (User ID) *", min_value=1, step=1, value=1)
            reason = st.text_area("Reason for Disposal / Decommissioning *", placeholder="e.g. Beyond Economical Repair (BER), damaged in field ops...")

            sub_disp = st.form_submit_button("📝 Submit Request")
            if sub_disp:
                if not reason.strip():
                    st.error("Please provide a valid reason.")
                else:
                    payload = {
                        "asset_id": int(disp_asset_id),
                        "requested_by": int(req_by_id),
                        "reason": reason
                    }
                    res = requests.post(get_backend_url("/disposals/request"), json=payload)
                    if res.status_code in [200, 201]:
                        st.success("Disposal request submitted successfully!")
                        st.json(res.json())
                    else:
                        st.error(f"Request failed: {res.text}")

    with t_app:
        st.subheader("Approve Asset Disposal")
        with st.form("disposal_app_form"):
            disposal_id = st.number_input("Disposal Request ID *", min_value=1, step=1, value=1)
            approved_by_id = st.number_input("Approving Officer User ID *", min_value=1, step=1, value=1)

            sub_app = st.form_submit_button("✅ Approve Disposal")
            if sub_app:
                url = get_backend_url(f"/disposals/approve/{disposal_id}?approved_by={approved_by_id}")
                res = requests.put(url)
                if res.status_code == 200:
                    st.success(f"Disposal request #{disposal_id} approved!")
                    st.json(res.json())
                else:
                    st.error(f"Approval failed: {res.text}")

# ---------------------------------------------------------
# Tab 7: Personnel & Authentication
# ---------------------------------------------------------
elif nav_option == "🎖️ Personnel & Auth":
    st.title("🎖️ Army Personnel Registry & Authentication")
    st.write("Login with military credentials or register new army personnel.")

    p_login, p_reg = st.tabs(["🔐 Personnel Login", "🎖️ Register Army Officer"])

    with p_login:
        st.subheader("Officer / User Authentication")
        with st.form("login_form"):
            army_number = st.text_input("Army Service Number", placeholder="e.g. IC-12345")
            password = st.text_input("Password", type="password")
            
            sub_login = st.form_submit_button("🔑 Login")
            if sub_login:
                if not army_number or not password:
                    st.error("Please enter Army Number and Password.")
                else:
                    payload = {"army_number": army_number, "password": password}
                    res = requests.post(get_backend_url("/users/login"), json=payload)
                    if res.status_code == 200:
                        token_data = res.json()
                        st.session_state.token = token_data.get("access_token")
                        st.session_state.user_info = army_number
                        st.success("Authentication Successful! Session token updated.")
                        st.json(token_data)
                    else:
                        st.error(f"Login failed: {res.text}")

    with p_reg:
        st.subheader("Register New Military Personnel")
        with st.form("register_form"):
            r_c1, r_c2 = st.columns(2)
            with r_c1:
                r_army = st.text_input("Army Service Number *", placeholder="e.g. IC-998877")
                r_fname = st.text_input("First Name *", placeholder="e.g. Vikram")
                r_lname = st.text_input("Last Name *", placeholder="e.g. Batra")
                r_email = st.text_input("Official Email *", placeholder="v.batra@army.mil")
                r_phone = st.text_input("Phone Number *", placeholder="9876543210")
            with r_c2:
                r_pwd = st.text_input("Password *", type="password")
                r_role = st.number_input("Role ID (1: Admin, 2: CO, 3: QM, 4: Store Keeper)", min_value=1, max_value=5, value=1)
                r_rank = st.number_input("Rank ID (1: Col, 2: Lt Col, 3: Maj, 4: Capt, 5: Lt)", min_value=1, max_value=5, value=1)
                r_unit = st.number_input("Unit ID (1: HQ, 2: Northern, 3: Western)", min_value=1, max_value=5, value=1)

            sub_reg = st.form_submit_button("🎖️ Register Personnel")
            if sub_reg:
                if not r_army or not r_fname or not r_email or not r_pwd:
                    st.error("Please fill in all mandatory fields.")
                else:
                    payload = {
                        "army_number": r_army,
                        "first_name": r_fname,
                        "last_name": r_lname,
                        "email": r_email,
                        "phone": r_phone,
                        "password": r_pwd,
                        "role_id": int(r_role),
                        "rank_id": int(r_rank),
                        "unit_id": int(r_unit)
                    }
                    res = requests.post(get_backend_url("/users/"), json=payload)
                    if res.status_code in [200, 201]:
                        st.success("Personnel registered successfully!")
                        st.json(res.json())
                    else:
                        st.error(f"Registration failed: {res.text}")
