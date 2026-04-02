import streamlit as st
import pandas as pd
import time
import plotly.graph_objects as go
import plotly.express as px

from inference.predict_freight import predict_freight_cost
from inference.predict_invoice_flag import predict_invoice_flag

# -----------------------------------------------------------------------------
# 1. Page Configuration & CSS Styling
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Invoice Intelligence",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enterprise SaaS Custom CSS
st.markdown("""
    <style>
    /* Clean up the main UI */
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    
    /* Standardized Card Styling for Forms */
    div[data-testid="stForm"] {
        border: 1px solid var(--secondary-background-color);
        border-radius: 8px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        padding: 2rem;
        background-color: var(--secondary-background-color);
    }
    
    /* Elegant Headers */
    h1, h2, h3 { font-weight: 600 !important; letter-spacing: -0.5px; }
    
    /* Interactive Button Styling */
    .stButton > button {
        border-radius: 6px;
        font-weight: 600;
        transition: all 0.2s ease-in-out;
        width: 100%;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. Header & Navigation (Tabs)
# -----------------------------------------------------------------------------
col_logo, col_title = st.columns([1, 11])
with col_logo:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135679.png", width=60)
with col_title:
    st.markdown("## Vendor Invoice Intelligence")
    st.caption("AI-Powered Financial Governance & Forecasting Engine")

st.divider()

# Using Tabs instead of Sidebar for a more standard web app feel
tab_dash, tab_freight, tab_risk = st.tabs([
    "📊 System Overview", 
    "🚚 Freight Forecaster", 
    "🚨 Risk Auditor"
])

# -----------------------------------------------------------------------------
# 3. Tab: System Overview
# -----------------------------------------------------------------------------
with tab_dash:
    st.markdown("### Operational Metrics")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric(label="Models Online", value="2/2", delta="Active", delta_color="normal")
    m2.metric(label="Avg Prediction Latency", value="0.4s", delta="-0.1s", delta_color="inverse")
    m3.metric(label="YTD Invoices Audited", value="14,205", delta="+12%")
    m4.metric(label="Anomalies Prevented", value="$42,500", delta="+5.2%")
    
    st.info("👈 Navigate to the **Freight Forecaster** or **Risk Auditor** tabs above to run inference on live data.")

# -----------------------------------------------------------------------------
# 4. Tab: Freight Forecaster
# -----------------------------------------------------------------------------
with tab_freight:
    st.markdown("### 🚚 Freight Cost Projection")
    st.write("Predict shipping overheads based on invoice volume and monetary value.")
    
    f_col1, f_col2 = st.columns([1, 1])
    
    with f_col1:
        with st.form("freight_form"):
            st.markdown("#### Input Parameters")
            quantity = st.slider("📦 Order Quantity", min_value=1, max_value=5000, value=1200, step=10)
            dollars = st.number_input("💰 Invoice Subtotal ($)", min_value=1.0, value=18500.0, step=100.0)
            submit_freight = st.form_submit_button("Generate Forecast", type="primary")

    with f_col2:
        if submit_freight:
            with st.status("Querying Prediction Engine...", expanded=True) as status:
                st.write("Scaling input vectors...")
                time.sleep(0.5)
                st.write("Running Random Forest inference...")
                
                input_data = {"Quantity": [quantity], "Dollars": [dollars]}
                prediction = predict_freight_cost(input_data)['Predicted_Freight'][0]
                
                time.sleep(0.5)
                status.update(label="Forecast Generated", state="complete", expanded=False)
            
            st.toast("Freight prediction successful!", icon="✅")
            
            # Interactive Plotly Gauge Chart for visual flair
            fig = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = prediction,
                title = {'text': "Estimated Freight Cost ($)", 'font': {'size': 24}},
                delta = {'reference': prediction * 1.1, 'increasing': {'color': "red"}, 'decreasing': {'color': "green"}},
                gauge = {
                    'axis': {'range': [0, max(500, prediction * 2)], 'tickwidth': 1, 'tickcolor': "darkblue"},
                    'bar': {'color': "#3b82f6"},
                    'bgcolor': "rgba(0,0,0,0)",
                    'borderwidth': 2,
                    'bordercolor': "gray",
                    'steps': [
                        {'range': [0, prediction * 0.8], 'color': "rgba(59, 130, 246, 0.2)"},
                        {'range': [prediction * 0.8, prediction * 1.2], 'color': "rgba(59, 130, 246, 0.5)"}],
                }
            ))
            fig.update_layout(height=350, margin=dict(l=10, r=10, t=50, b=10))
            st.plotly_chart(fig, use_container_width=True)

# -----------------------------------------------------------------------------
# 5. Tab: Risk Auditor
# -----------------------------------------------------------------------------
with tab_risk:
    st.markdown("### 🚨 Autonomous Risk Guard")
    st.write("Detect discrepancies between vendor invoices and internal purchase order records.")

    r_col1, r_col2 = st.columns([1, 1.2])

    with r_col1:
        with st.form("invoice_flag_form"):
            st.markdown("#### Invoice Details (Vendor)")
            c1, c2 = st.columns(2)
            inv_qty = c1.number_input("Invoice Quantity", min_value=1, value=50)
            inv_val = c2.number_input("Invoice Value ($)", min_value=1.0, value=1000.0)
            freight = st.number_input("Billed Freight ($)", min_value=0.0, value=1.73)
            
            st.markdown("#### System Details (Internal PO)")
            c3, c4 = st.columns(2)
            tot_qty = c3.number_input("Expected Quantity", min_value=1, value=162)
            tot_val = c4.number_input("Expected Value ($)", min_value=1.0, value=1000.0)
            
            submit_flag = st.form_submit_button("Execute Risk Audit", type="primary")

    with r_col2:
        if submit_flag:
            with st.spinner("Analyzing historical patterns & variances..."):
                time.sleep(1) # Simulated network latency for UI feel
                
                input_data = {
                    "invoice_quantity": [inv_qty],
                    "invoice_dollars": [inv_val],
                    "Freight": [freight],
                    "total_item_quantity": [tot_qty],
                    "total_item_dollars": [tot_val]
                }
                
                flag_prediction = predict_invoice_flag(input_data)['Predicted_Flag']
                is_flagged = bool(flag_prediction[0])

            # Interactive Plotly Bar Chart comparing Invoiced vs Expected
            plot_df = pd.DataFrame({
                "Category": ["Quantity", "Dollars"],
                "Invoiced": [inv_qty, inv_val],
                "System Expected": [tot_qty, tot_val]
            })
            
            fig_risk = px.bar(
                plot_df, 
                x="Category", 
                y=["Invoiced", "System Expected"],
                barmode="group",
                color_discrete_map={"Invoiced": "#ef4444" if is_flagged else "#3b82f6", "System Expected": "#64748b"},
                title="Variance Analysis"
            )
            fig_risk.update_layout(height=300, margin=dict(l=10, r=10, t=40, b=10), legend_title=None)
            st.plotly_chart(fig_risk, use_container_width=True)

            # Display Results Notice
            if is_flagged:
                st.error("#### 🛑 HIGH RISK DETECTED\nSignificant variance identified between invoiced amounts and internal system expectations. **Manual approval required.**", icon="🚨")
            else:
                st.success("#### ✅ CLEARANCE GRANTED\nInvoice metrics fall within standard tolerance levels. Approved for automated routing.", icon="🛡️")