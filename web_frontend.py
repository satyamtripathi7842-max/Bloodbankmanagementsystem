import streamlit as st
import datetime
import re

# ==========================================
# 1. ENTERPRISE DATA ENGINE & BACKEND
# ==========================================
class BloodStockNotAvailableException(Exception):
    """Custom exception handled when stock runs out"""
    pass

class BloodBankManagementSystem:
    def __init__(self):
        # Professional Default Stock Settings (ml)
        self.blood_stock = {
            "A+": 1200, "A-": 600, 
            "B+": 1500, "B-": 450, 
            "O+": 2000, "O-": 300, 
            "AB+": 800, "AB-": 250
        }
        self.blood_requests = [
            {"Request ID": "REQ-2026-101", "Hospital Name": "City General Hospital", "Blood Group": "A+", "Quantity (ml)": 300, "Status": "Approved", "Timestamp": "2026-06-10 14:32", "Notification Email": "admin@cityhospital.org"},
            {"Request ID": "REQ-2026-102", "Hospital Name": "Metro Emergency Care", "Blood Group": "O-", "Quantity (ml)": 150, "Status": "Approved", "Timestamp": "2026-06-11 09:15", "Notification Email": "emergency@metrocare.in"}
        ]
        self.donors_list = [
            {"Donor ID": "D-901", "Name": "Rahul Sharma", "Blood Group": "O+", "Age": 28, "Units Donated": 1, "Contact": "+91 98765 43210", "Status": "Available", "Last Donated": "2026-03-12", "Email": "rahul.s@email.com"},
            {"Donor ID": "D-902", "Name": "Anjali Verma", "Blood Group": "A+", "Age": 24, "Units Donated": 1, "Contact": "+91 87654 32109", "Status": "Available", "Last Donated": "2026-04-01", "Email": "anjali.v@email.com"}
        ]
        self.camp_schedules = [
            {"Camp Name": "Mega Delhi Donation Drive", "Date": "2026-06-15", "Location": "Connaught Place, Central Core", "Organiser": "RedLife NGO"},
            {"Camp Name": "Tech Park Blood Camp", "Date": "2026-06-22", "Location": "Sector 62 Institutional Area", "Organiser": "Rotary Club"}
        ]

    def process_request(self, req_id, hosp, req_bg, req_qty, email):
        available_qty = self.blood_stock.get(req_bg, 0)
        if available_qty < req_qty:
            raise BloodStockNotAvailableException(
                f"🚨 Supply Shortage: Requested {req_qty}ml for {req_bg}. Core Reserve has only {available_qty}ml."
            )
        self.blood_stock[req_bg] -= req_qty
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        self.blood_requests.append({
            "Request ID": req_id,
            "Hospital Name": hosp,
            "Blood Group": req_bg,
            "Quantity (ml)": req_qty,
            "Status": "Approved",
            "Timestamp": now,
            "Notification Email": email if email else "N/A"
        })
        return True

    def register_donor(self, name, bg, age, contact, units, email):
        donor_id = f"D-{len(self.donors_list) + 901}"
        now_date = datetime.date.today().strftime("%Y-%m-%d")
        self.donors_list.append({
            "Donor ID": donor_id,
            "Name": name,
            "Blood Group": bg,
            "Age": age,
            "Units Donated": units,
            "Contact": contact,
            "Status": "Available",
            "Last Donated": now_date,
            "Email": email if email else "N/A"
        })
        total_ml_added = units * 450
        self.blood_stock[bg] += total_ml_added
        return donor_id, total_ml_added


# ==========================================
# 2. ULTRA-PREMIUM LOGISTICS DASHBOARD UI
# ==========================================
st.set_page_config(page_title="RedLife Cloud OS - Control Console", layout="wide", page_icon="🩸")

# Advanced UI Custom Style Injection
st.markdown("""
    <style>
    .bolt-banner {
        background: linear-gradient(135deg, #0f0c1b 0%, #d92432 100%);
        padding: 35px;
        border-radius: 16px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 8px 24px rgba(217, 36, 50, 0.2);
    }
    .section-header {
        color: #11111b;
        font-weight: 700;
        font-size: 20px;
        border-left: 6px solid #d92432;
        padding-left: 12px;
        margin-top: 15px;
        margin-bottom: 15px;
    }
    .email-container {
        background-color: #f0f4f8;
        border: 1px dashed #d92432;
        padding: 12px;
        border-radius: 8px;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Session State Persistence
if 'bbms' not in st.session_state:
    st.session_state.bbms = BloodBankManagementSystem()

bbms = st.session_state.bbms

# --- PORTAL HEADER PROFILE ---
st.markdown("""
    <div class='bolt-banner'>
        <h1 style='font-size: 44px; margin:0; font-weight: 800; letter-spacing: 0.5px;'>🩸 REDLIFE AUTOMATED OVERSEER OS</h1>
        <p style='font-size: 15px; opacity: 0.9; margin-top: 6px;'>Enterprise Logistics Cloud • Unified Email Gateway & Live Asset Dispatch Network</p>
    </div>
""", unsafe_allow_html=True)

# --- OVERVIEW METRICS GRID ---
total_stock = sum(bbms.blood_stock.values())
total_reqs = len(bbms.blood_requests)
total_donors = len(bbms.donors_list)

col_m1, col_m2, col_m3, col_m4 = st.columns(4)
with col_m1:
    st.metric(label="Global Vault Inventory", value=f"{total_stock} ml", delta="Live Synced")
with col_m2:
    st.metric(label="Emergency Dispatches Issued", value=total_reqs)
with col_m3:
    st.metric(label="Registered Network Donors", value=total_donors, delta="+ Verified Nodes")
with col_m4:
    critical_alerts = len([v for v in bbms.blood_stock.values() if v <= 400])
    st.metric(label="Critical Buffers Alert", value=critical_alerts, delta="- Stock Emergency" if critical_alerts > 0 else "Optimal Vaults")

st.write("---")

# --- MAIN RESPONSIVE CORE SPLIT LAYOUT ---
workspace_pane, asset_pane = st.columns([2.3, 1])

with workspace_pane:
    # Navigation Modules 
    tab_dispatch, tab_directory, tab_onboard, tab_camps = st.tabs([
        "🏥 Hospital Emergency Dispatch", 
        "👥 Live Donor Directory Search", 
        "➕ New Donor Onboarding Hub",
        "📅 Donation Camps Coordinator"
    ])
    
    # --- TAB 1: HOSPITAL EMERGENCY DISPATCH ---
    with tab_dispatch:
        st.markdown("<div class='section-header'>Create Urgent Blood Asset Release Order</div>", unsafe_allow_html=True)
        with st.form("hosp_dispatch_form", clear_on_submit=True):
            h_name = st.text_input("Destination Medical Center / Hospital Entity", placeholder="e.g. AIIMS Emergency Trauma Wing")
            
            sub_c1, sub_c2 = st.columns(2)
            with sub_c1:
                b_group = st.selectbox("Requested Blood Type Blueprint", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
            with sub_c2:
                b_volume = st.number_input("Volume Dimension Required (ml)", min_value=50, max_value=5000, value=450, step=50)
            
            # UNIQUE FEATURE: Email Alert Field
            h_email = st.text_input("Hospital Notification Email (Gateway Integration)", placeholder="emergency-desk@hospital.org")
                
            trigger_dispatch = st.form_submit_button("⚡ Authorize Real-time Vault Release")
            
            if trigger_dispatch:
                if not h_name.strip():
                    st.error("🔒 Security Halt: Valid target hospital profile name required.")
                elif h_email and not re.match(r"[^@]+@[^@]+\.[^@]+", h_email):
                    st.error("🔒 Security Halt: Invalid format detected in Notification Email field.")
                else:
                    try:
                        r_code = f"REQ-2026-{len(bbms.blood_requests) + 101}"
                        bbms.process_request(r_code, h_name, b_group, b_volume, h_email)
                        st.success(f"🚀 **Security Protocol Approved!** Dispatched {b_volume}ml of **{b_group}** safely to *{h_name}*. Tracking Reference ID: **{r_code}**")
                        
                        if h_email:
                            st.markdown(f"""
                            <div class='email-container'>
                                📧 <b>Automated RedLife Email Dispatch Terminal:</b><br/>
                                To: <u>{h_email}</u><br/>
                                Subject: <b>🚨 EMERGENCY BLOOD ALLOCATION DETECTED [ID: {r_code}]</b><br/>
                                Body: <i>Your requested {b_volume}ml of {b_group} blood has passed validation and left the vault corridor. Clear the transit zone.</i>
                            </div>
                            """, unsafe_allow_html=True)
                        st.balloons()
                    except BloodStockNotAvailableException as msg:
                        st.error(str(msg))

        st.write("##")
        st.markdown("<div class='section-header'>Central Audit Log File (Live Monitoring)</div>", unsafe_allow_html=True)
        
        search_query = st.text_input("🔍 Filter Dashboard Logs by Hospital Name", placeholder="Type hospital name to live filter...")
        if bbms.blood_requests:
            import pandas as pd
            df_reqs = pd.DataFrame(bbms.blood_requests)
            if search_query:
                df_reqs = df_reqs[df_reqs['Hospital Name'].str.contains(search_query, case=False)]
            st.dataframe(df_reqs, use_container_width=True, hide_index=True)

    # --- TAB 2: LIVE DONOR DIRECTORY SEARCH ---
    with tab_directory:
        st.markdown("<div class='section-header'>Searchable Network Donor Grid</div>", unsafe_allow_html=True)
        filter_group = st.selectbox("Global Filter Segment by Blood Group", ["All Profiles", "A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
        
        if filter_group == "All Profiles":
            rendered_donors = bbms.donors_list
        else:
            rendered_donors = [d for d in bbms.donors_list if d["Blood Group"] == filter_group]
            
        if rendered_donors:
            st.dataframe(rendered_donors, use_container_width=True, hide_index=True)
        else:
            st.info(f"No active donor records matching {filter_group} on this network node.")

    # --- TAB 3: NEW DONOR ONBOARDING HUB ---
    with tab_onboard:
        st.markdown("<div class='section-header'>Voluntary Donor Intake Enrollment</div>", unsafe_allow_html=True)
        with st.form("donor_intake_form", clear_on_submit=True):
            d_name = st.text_input("Full Legal Name of Donor", placeholder="e.g. Dr. Samir Khan")
            d_phone = st.text_input("Secure Contact Path / Phone", placeholder="+91 XXXXX XXXXX")
            d_email = st.text_input("Donor Digital Mail ID (Certificate Delivery)", placeholder="donor.name@domain.com")
            
            o_c1, o_c2, o_c3 = st.columns([2, 1, 1])
            with o_c1:
                d_bg = st.selectbox("Donor Blood Grid Classification", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
            with o_c2:
                d_age = st.number_input("Verified Medical Age (18-65)", min_value=18, max_value=65, value=28)
            with o_c3:
                d_units = st.selectbox("Blood Units Contributed", [1, 2, 3], index=0)
                
            trigger_onboard = st.form_submit_button("❤️ Finalize Enrollment & Process Donation Assets")
            
            if trigger_onboard:
                if not d_name.strip() or not d_phone.strip():
                    st.error("🔒 Validation Fault: Onboarding profiles must contain valid name strings.")
                elif d_email and not re.match(r"[^@]+@[^@]+\.[^@]+", d_email):
                    st.error("🔒 Validation Fault: Please insert a realistic Email architecture.")
                else:
                    d_code, ml_added = bbms.register_donor(d_name, d_bg, d_age, d_phone, d_units, d_email)
                    st.success(f"🎉 **Enrollment Successful!** Profile ID **{d_code}** linked. Contributed **{d_units} Unit(s)** (**{ml_added}ml** total injected into **{d_bg}** reserves!)")
                    
                    if d_email:
                        st.markdown(f"""
                        <div class='email-container' style='border-color: #2e7d32;'>
                            📧 <b>Automated RedLife System Certificate Dispatcher:</b><br/>
                            To: <u>{d_email}</u><br/>
                            Subject: <b>❤️ Thank You for Saving Lives! Donation Receipt [{d_code}]</b><br/>
                            Body: <i>Dear {d_name}, your contribution of {d_units} Unit(s) has been successfully verified. RedLife appreciates your incredible civic action. Certification attached.</i>
                        </div>
                        """, unsafe_allow_html=True)
                    st.rerun()

    # --- TAB 4: NEW DONATION CAMPS COORDINATOR ---
    with tab_camps:
        st.markdown("<div class='section-header'>Scheduled Field Donation Drives</div>", unsafe_allow_html=True)
        st.table(bbms.camp_schedules)
        
        with st.expander("➕ Schedule/Announce New Donation Camp Event"):
            with st.form("camp_creation_form", clear_on_submit=True):
                c_title = st.text_input("Camp Event Title")
                c_loc = st.text_input("Venue Location Map Address")
                c_org = st.text_input("Lead Organizing Authority/Sponsor")
                if st.form_submit_button("📢 Publish Camp Notification Live"):
                    if c_title and c_loc:
                        bbms.camp_schedules.append({
                            "Camp Name": c_title,
                            "Date": str(datetime.date.today() + datetime.timedelta(days=7)),
                            "Location": c_loc,
                            "Organiser": c_org if c_org else "RedLife Affiliate"
                        })
                        st.success("Event operational broadcast system deployed successfully!")
                        st.rerun()


with asset_pane:
    # --- AUTOMATED STORAGE PROGRESS PROGRESS BARS ---
    st.markdown("<h3 style='color: #d92432; margin-top:10px;'>📊 Vault Inventory Status</h3>", unsafe_allow_html=True)
    st.write("Dynamic metrics scaling framework (Max indexing index threshold optimized at 2500ml limits):")
    
    CRITICAL = 400
    OPTIMAL = 1000
    
    for blood_group, current_volume in bbms.blood_stock.items():
        scaled_ratio = min(current_volume / 2500, 1.0)
        label_descriptor = f"**{blood_group}** Registry — {current_volume} ml"
        
        if current_volume <= CRITICAL:
            st.markdown(f"<span style='color:#d92432; font-weight:bold;'>🚨 {label_descriptor} (CRITICAL RESERVE)</span>", unsafe_allow_html=True)
            st.progress(scaled_ratio)
        elif current_volume < OPTIMAL:
            st.write(f"🔸 {label_descriptor} (Stable Buffer)")
            st.progress(scaled_ratio)
        else:
            st.markdown(f"<span style='color:#2e7d32; font-weight:bold;'>🟢 {label_descriptor} (Optimal Level)</span>", unsafe_allow_html=True)
            st.progress(scaled_ratio)
            
    # --- ACTIVE FLEET TRANSIT MATRIX ---
    st.write("##")
    st.markdown("<h3>📍 Fleet Transit Tracker</h3>", unsafe_allow_html=True)
    st.caption("Active automated asset transport parameters matrix")
    st.info("🛰️ Dispatch Vehicle assigned to `REQ-2026-102` is en route to Metro Emergency Care. ETA: 12 Mins.")