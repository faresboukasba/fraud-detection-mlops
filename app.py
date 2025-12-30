#!/usr/bin/env python3
"""
Streamlit Fraud Detection UI - Version minimale sans dépendances
"""
import streamlit as st
import requests
import json
import os

st.set_page_config(page_title="Fraud Detection", page_icon="🚨", layout="wide")

# CSS custom
st.markdown("""
<style>
    .big-font {font-size:40px; font-weight:bold; color:#FF4B4B;}
    .metric-card {background-color:#f0f2f6; padding:20px; border-radius:10px; margin:10px 0;}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-font">🔍 Fraud Detection System</p>', unsafe_allow_html=True)
st.markdown("---")

# API Config
API_URL = os.getenv("API_URL", "https://2sdeaedszk.eu-west-3.awsapprunner.com")

# Sidebar
with st.sidebar:
    st.title("⚙️ Configuration")
    st.info(f"🔗 API: {API_URL}")
    
    # Health check
    try:
        resp = requests.get(f"{API_URL}/health", timeout=3)
        if resp.status_code == 200:
            st.success("✅ API Connected")
        else:
            st.error("❌ API Error")
    except:
        st.error("❌ API Unreachable")

# Tabs
tab1, tab2 = st.tabs(["Single Prediction", "Batch Prediction"])

with tab1:
    st.header("Single Transaction Analysis")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Transaction Details")
        time_val = st.number_input("Time (seconds)", value=0, min_value=0)
        amount = st.number_input("Amount ($)", value=100.0, min_value=0.0)
        
        st.subheader("Features (V1-V5)")
        v1 = st.number_input("V1", value=0.0, step=0.1)
        v2 = st.number_input("V2", value=0.0, step=0.1)
        v3 = st.number_input("V3", value=0.0, step=0.1)
        v4 = st.number_input("V4", value=0.0, step=0.1)
        v5 = st.number_input("V5", value=0.0, step=0.1)
    
    with col2:
        st.subheader("JSON Input Alternative")
        json_input = st.text_area("Paste JSON", height=200, value='{"Time": 0, "Amount": 100}')
    
    # Predict button
    if st.button("🔍 Check for Fraud", key="predict"):
        try:
            if json_input.strip().startswith("{"):
                data = json.loads(json_input)
            else:
                # Build from manual inputs
                import math
                data = {
                    "Time": int(time_val),
                    "Amount": float(amount),
                    "V1": v1, "V2": v2, "V3": v3, "V4": v4, "V5": v5,
                    "V6": 0, "V7": 0, "V8": 0, "V9": 0, "V10": 0,
                    "V11": 0, "V12": 0, "V13": 0, "V14": 0, "V15": 0,
                    "V16": 0, "V17": 0, "V18": 0, "V19": 0, "V20": 0,
                    "V21": 0, "V22": 0, "V23": 0, "V24": 0, "V25": 0,
                    "V26": 0, "V27": 0, "V28": 0,
                    "amount_zscore": (amount - 88) / 250 if amount > 0 else 0,
                    "amount_log": math.log(amount + 1) if amount > 0 else 0,
                    "v1_v2_ratio": abs(v1 / (v2 + 0.0001)) if v2 != 0 else 0,
                    "high_value": 1.0 if amount > 1000 else 0.0,
                    "variance_all": 0.5,
                    "max_abs_v": max(abs(v1), abs(v2), abs(v3), abs(v4), abs(v5)),
                    "mean_abs_v": (abs(v1) + abs(v2) + abs(v3) + abs(v4) + abs(v5)) / 5
                }
            
            # API call
            response = requests.post(f"{API_URL}/predict", json=data, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                
                st.markdown("---")
                st.success("✅ Prediction Complete!")
                
                # Display results
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    score = result.get("hybrid_score", 0)
                    st.markdown(f'<div class="metric-card"><b>Fraud Score</b><br><h2>{score:.4f}</h2></div>', unsafe_allow_html=True)
                
                with col2:
                    is_fraud = result.get("fraud", 0)
                    status = "🚨 FRAUD" if is_fraud else "✅ LEGITIMATE"
                    color = "#FF4B4B" if is_fraud else "#00CC88"
                    st.markdown(f'<div class="metric-card"><b>Status</b><br><h2 style="color:{color}">{status}</h2></div>', unsafe_allow_html=True)
                
                with col3:
                    threshold = result.get("threshold_used", 0)
                    st.markdown(f'<div class="metric-card"><b>Threshold</b><br><h2>{threshold:.4f}</h2></div>', unsafe_allow_html=True)
                
                st.markdown("---")
                st.subheader("Full Response")
                st.json(result)
            else:
                st.error(f"API Error: {response.status_code}")
                st.error(response.text)
        
        except json.JSONDecodeError:
            st.error("Invalid JSON format")
        except Exception as e:
            st.error(f"Error: {str(e)}")

with tab2:
    st.header("Batch Prediction")
    st.info("Upload a CSV file with transaction data")
    
    csv_file = st.file_uploader("Choose CSV file", type="csv")
    
    if csv_file is not None:
        try:
            import pandas as pd
            df = pd.read_csv(csv_file)
            
            st.write(f"Loaded {len(df)} transactions")
            st.dataframe(df.head(10))
            
            if st.button("⚡ Predict All", key="batch_predict"):
                records = df.to_dict(orient='records')
                
                response = requests.post(f"{API_URL}/predict-batch", json=records, timeout=30)
                
                if response.status_code == 200:
                    results = response.json()
                    results_df = pd.DataFrame(results)
                    
                    st.success(f"✅ Processed {len(results)} transactions")
                    
                    # Stats
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        fraud_count = sum(1 for r in results if r.get("fraud"))
                        st.metric("Fraud Cases", fraud_count)
                    with col2:
                        avg_score = sum(r.get("hybrid_score", 0) for r in results) / len(results)
                        st.metric("Avg Score", f"{avg_score:.4f}")
                    with col3:
                        fraud_rate = (fraud_count / len(results) * 100) if results else 0
                        st.metric("Fraud Rate", f"{fraud_rate:.1f}%")
                    
                    st.dataframe(results_df)
                else:
                    st.error(f"API Error: {response.status_code}")
        except Exception as e:
            st.error(f"Error: {str(e)}")

st.markdown("---")
st.caption("🛡️ Fraud Detection System | Powered by Ensemble ML Models")
