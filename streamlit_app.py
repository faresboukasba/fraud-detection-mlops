"""
Streamlit Frontend for Fraud Detection API
"""
import streamlit as st
import requests
import pandas as pd
import json
from io import StringIO
import plotly.graph_objects as go
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Fraud Detection System",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 20px;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar configuration
st.sidebar.title("⚙️ Configuration")
api_url = st.sidebar.text_input(
    "API URL",
    value="https://2sdeaedszk.eu-west-3.awsapprunner.com",
    help="Base URL of the Fraud Detection API"
)

st.sidebar.markdown("---")
st.sidebar.info(
    "**Fraud Detection System**\n\n"
    "Upload a JSON or CSV file containing transaction data to check for fraud.\n\n"
    "Required features: Time, V1-V28, Amount, and engineered features."
)

# Main title
st.title("🔍 Fraud Detection System")
st.markdown("### Powered by Machine Learning & Ensemble Models")

# Check API health
try:
    health_response = requests.get(f"{api_url}/health", timeout=5)
    if health_response.status_code == 200:
        st.sidebar.success("✅ API Connected")
    else:
        st.sidebar.error("❌ API Error")
except Exception as e:
    st.sidebar.error(f"❌ API Unreachable: {str(e)}")

# Tabs
tab1, tab2, tab3 = st.tabs(["📤 Single Prediction", "📊 Batch Prediction", "📈 Analytics"])

# TAB 1: Single Prediction
with tab1:
    st.header("Single Transaction Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📝 Input Data")
        input_method = st.radio("Select input method:", ["Manual Entry", "JSON", "Paste JSON"])
        
        if input_method == "Manual Entry":
            time_val = st.number_input("Time (seconds)", value=0.0)
            amount = st.number_input("Amount ($)", value=100.0, min_value=0.0)
            
            st.markdown("**Normalized Features (V1-V28)**")
            cols = st.columns(4)
            v_features = {}
            for i in range(28):
                with cols[i % 4]:
                    v_features[f"V{i+1}"] = st.number_input(f"V{i+1}", value=0.0, key=f"v{i+1}")
            
            # Engineered features
            st.markdown("**Engineered Features**")
            cols = st.columns(2)
            with cols[0]:
                amount_zscore = st.number_input("amount_zscore", value=0.0)
                amount_log = st.number_input("amount_log", value=5.0)
                v1_v2_ratio = st.number_input("v1_v2_ratio", value=0.0)
                high_value = st.number_input("high_value", value=0.0)
            with cols[1]:
                variance_all = st.number_input("variance_all", value=0.5)
                max_abs_v = st.number_input("max_abs_v", value=4.4)
                mean_abs_v = st.number_input("mean_abs_v", value=0.6)
            
            payload = {
                "Time": time_val,
                "Amount": amount,
                **v_features,
                "amount_zscore": amount_zscore,
                "amount_log": amount_log,
                "v1_v2_ratio": v1_v2_ratio,
                "high_value": high_value,
                "variance_all": variance_all,
                "max_abs_v": max_abs_v,
                "mean_abs_v": mean_abs_v
            }
        
        elif input_method == "JSON":
            uploaded_file = st.file_uploader("Upload JSON file", type="json")
            if uploaded_file:
                payload = json.loads(uploaded_file.getvalue())
                st.json(payload)
            else:
                payload = None
        
        else:  # Paste JSON
            json_text = st.text_area("Paste JSON data", height=300)
            if json_text:
                try:
                    payload = json.loads(json_text)
                except json.JSONDecodeError:
                    st.error("Invalid JSON format")
                    payload = None
            else:
                payload = None
    
    with col2:
        st.subheader("🎯 Prediction Result")
        
        if st.button("🚀 Analyze Transaction", key="single_predict"):
            if payload is None:
                st.error("Please provide valid input data")
            else:
                try:
                    with st.spinner("Processing..."):
                        response = requests.post(
                            f"{api_url}/predict",
                            json=payload,
                            timeout=10
                        )
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        # Display results
                        col_result1, col_result2 = st.columns(2)
                        
                        with col_result1:
                            if result.get("fraud") == 1:
                                st.error("🚨 FRAUD DETECTED!")
                            else:
                                st.success("✅ LEGITIMATE")
                        
                        with col_result2:
                            st.metric(
                                "Risk Score",
                                f"{result.get('hybrid_score', 0):.2%}",
                                delta=f"Threshold: {result.get('threshold_used', 0):.2%}"
                            )
                        
                        # Detailed results
                        st.markdown("### 📊 Detailed Analysis")
                        col_detail1, col_detail2, col_detail3 = st.columns(3)
                        
                        with col_detail1:
                            st.metric("Prediction", "Fraud" if result.get("fraud") == 1 else "Legitimate")
                        with col_detail2:
                            st.metric("Risk Score", f"{result.get('hybrid_score', 0):.4f}")
                        with col_detail3:
                            st.metric("Threshold", f"{result.get('threshold_used', 0):.4f}")
                        
                        # Display full response
                        st.markdown("### 📋 Full Response")
                        st.json(result)
                        
                    else:
                        st.error(f"API Error: {response.status_code}")
                        st.error(response.text)
                
                except Exception as e:
                    st.error(f"Request Error: {str(e)}")

# TAB 2: Batch Prediction
with tab2:
    st.header("Batch Transaction Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📤 Upload Batch Data")
        
        uploaded_csv = st.file_uploader(
            "Upload CSV file with multiple transactions",
            type="csv"
        )
        
        if uploaded_csv:
            df = pd.read_csv(uploaded_csv)
            st.write(f"Loaded {len(df)} transactions")
            st.dataframe(df.head())
            
            if st.button("🚀 Analyze Batch"):
                with st.spinner("Processing batch predictions..."):
                    try:
                        # Prepare batch request
                        samples = []
                        for idx, row in df.iterrows():
                            sample = row.to_dict()
                            samples.append(sample)
                        
                        batch_payload = {"samples": samples}
                        
                        response = requests.post(
                            f"{api_url}/predict_batch",
                            json=batch_payload,
                            timeout=30
                        )
                        
                        if response.status_code == 200:
                            results = response.json()
                            
                            # Summary stats
                            predictions = results.get("predictions", [])
                            fraud_count = sum(1 for p in predictions if p.get("fraud") == 1)
                            
                            st.success(f"✅ Processed {results.get('total_samples', 0)} transactions")
                            
                            # Metrics
                            col_metric1, col_metric2, col_metric3, col_metric4 = st.columns(4)
                            with col_metric1:
                                st.metric("Total", results.get("total_samples", 0))
                            with col_metric2:
                                st.metric("Fraud", fraud_count)
                            with col_metric3:
                                st.metric("Legitimate", results.get("total_samples", 0) - fraud_count)
                            with col_metric4:
                                st.metric("Time (ms)", f"{results.get('execution_time_ms', 0):.0f}")
                            
                            # Results table
                            results_df = pd.DataFrame([
                                {
                                    "Transaction": i+1,
                                    "Fraud": "Yes" if p.get("fraud") == 1 else "No",
                                    "Risk Score": p.get("hybrid_score", 0),
                                    "Confidence": p.get("confidence", 0)
                                }
                                for i, p in enumerate(predictions)
                            ])
                            
                            st.dataframe(results_df, use_container_width=True)
                            
                            # Download results
                            csv = results_df.to_csv(index=False)
                            st.download_button(
                                label="📥 Download Results (CSV)",
                                data=csv,
                                file_name=f"fraud_predictions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                                mime="text/csv"
                            )
                        else:
                            st.error(f"API Error: {response.status_code}")
                    
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
    
    with col2:
        st.subheader("📊 Sample CSV Format")
        sample_df = pd.DataFrame({
            "Time": [0.0, 100.0],
            "V1": [-1.36, 1.36],
            "V2": [-0.07, 0.07],
            "V3": [2.54, -2.54],
            "Amount": [100.0, 500.0],
            "amount_zscore": [0.0, 1.0],
            "amount_log": [5.0, 6.0],
            "v1_v2_ratio": [18.32, 19.0],
            "high_value": [0.0, 1.0],
            "variance_all": [0.5, 0.6],
            "max_abs_v": [4.4, 5.0],
            "mean_abs_v": [0.6, 0.7]
        })
        st.dataframe(sample_df)
        
        # Download sample
        csv = sample_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Sample CSV",
            data=csv,
            file_name="sample_transactions.csv",
            mime="text/csv"
        )

# TAB 3: Analytics
with tab3:
    st.header("📈 System Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("API Health")
        try:
            health = requests.get(f"{api_url}/health", timeout=5).json()
            st.json(health)
        except Exception as e:
            st.error(f"Cannot reach API: {str(e)}")
    
    with col2:
        st.subheader("System Information")
        st.info(
            f"**API Endpoint**: {api_url}\n\n"
            f"**Streamlit Version**: {st.__version__}\n\n"
            f"**Last Update**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )

# Footer
st.markdown("---")
st.markdown(
    "**Fraud Detection System** | "
    "Powered by Isolation Forest + XGBoost Ensemble | "
    "[GitHub](https://github.com/faresboukasba/fraud-detection-mlops)"
)
