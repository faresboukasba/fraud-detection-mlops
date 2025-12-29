# Streamlit Frontend

Interactive web interface for the Fraud Detection System.

## Features

✨ **Single Transaction Analysis**
- Manual input of all features
- JSON file upload
- Paste JSON data
- Real-time predictions

📊 **Batch Prediction**
- CSV file upload with multiple transactions
- Bulk fraud detection
- Results export to CSV
- Performance metrics

📈 **Analytics Dashboard**
- API health status
- System information
- Connection verification

## Installation

### Local Development

```bash
# Install Streamlit and dependencies
pip install streamlit plotly pandas requests

# Run the app
streamlit run streamlit_app.py
```

The app will be available at `http://localhost:8501`

### Docker

```bash
# Build Streamlit image
docker build -f Dockerfile.streamlit -t fraud-detection-ui .

# Run with API
docker run --network fraud-detection-net \
  -p 8501:8501 \
  -e API_URL=http://api:8000 \
  fraud-detection-ui
```

### Docker Compose (Recommended)

```bash
# Start both API and UI
docker-compose up

# API: http://localhost:8000
# UI:  http://localhost:8501
```

## Configuration

Edit `.streamlit/config.toml` to customize:
- Theme colors
- Port number
- Server settings
- Logging level

## Deployment Options

### 1. Streamlit Cloud (Free, Recommended)

```bash
# 1. Push code to GitHub
git push origin main

# 2. Go to https://streamlit.io/cloud
# 3. Create new app
# 4. Connect GitHub repository
# 5. Set API_URL secret
```

### 2. AWS App Runner

Create a second App Runner service with:
- **Dockerfile**: `Dockerfile.streamlit`
- **Port**: 8501
- **Environment**: `API_URL=https://<api-service>.awsapprunner.com`

### 3. AWS EC2 + Nginx

```bash
# SSH to EC2
ssh -i key.pem ubuntu@<ip>

# Clone and setup
git clone <repo>
cd fraud-detection-mlops
pip install -r requirements.txt streamlit plotly

# Run with Nginx reverse proxy on port 443
streamlit run streamlit_app.py --server.port 8501 &

# Configure Nginx
# - Proxy to localhost:8501
# - SSL certificate
```

## API Connection

Update the API URL in sidebar configuration:
- **Local**: `http://localhost:8000`
- **AWS**: `https://2sdeaedszk.eu-west-3.awsapprunner.com`
- **Custom**: Any HTTP/HTTPS endpoint

## File Formats

### Single Transaction (JSON)
```json
{
  "Time": 0.0,
  "V1": -1.36,
  "V2": -0.07,
  "V3": 2.54,
  "V4": 4.41,
  "V5": -0.05,
  "V6": -0.10,
  "V7": 0.64,
  "V8": 0.46,
  "V9": -0.05,
  "V10": -0.03,
  "V11": -2.24,
  "V12": -0.65,
  "V13": -0.42,
  "V14": -0.38,
  "V15": 1.16,
  "V16": -0.17,
  "V17": -0.37,
  "V18": 0.20,
  "V19": 0.01,
  "V20": -0.44,
  "V21": -0.01,
  "V22": -0.23,
  "V23": 0.10,
  "V24": -0.46,
  "V25": -0.12,
  "V26": -0.51,
  "V27": -0.07,
  "V28": 0.01,
  "Amount": 149.62,
  "amount_zscore": 0.0,
  "amount_log": 5.0,
  "v1_v2_ratio": 18.32,
  "high_value": 0.0,
  "variance_all": 0.5,
  "max_abs_v": 4.4,
  "mean_abs_v": 0.6
}
```

### Batch Transactions (CSV)
```
Time,V1,V2,V3,Amount,amount_zscore,amount_log,v1_v2_ratio,high_value,variance_all,max_abs_v,mean_abs_v
0.0,-1.36,-0.07,2.54,100.0,0.0,5.0,18.32,0.0,0.5,4.4,0.6
100.0,1.36,0.07,-2.54,500.0,1.0,6.0,19.0,1.0,0.6,5.0,0.7
```

## Troubleshooting

### API Connection Failed
- Verify API URL in sidebar
- Check API health status: `/health` endpoint
- Ensure firewall allows connections

### Upload Fails
- Verify file format (JSON or CSV)
- Check file encoding (UTF-8)
- Ensure all required columns present

### Slow Predictions
- Check network latency
- Verify API is running
- Consider batch operations for multiple transactions

## Architecture

```
┌─────────────┐
│  Streamlit  │
│   UI        │
│ (Port 8501) │
└──────┬──────┘
       │ HTTP
       ▼
┌─────────────┐
│  FastAPI    │
│  Backend    │
│ (Port 8000) │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Models    │
│  (Ensemble) │
└─────────────┘
```

## Performance

- **Single prediction**: <100ms
- **Batch (100 txn)**: <1s
- **Throughput**: 1000+ predictions/min

## Security

- HTTPS for cloud deployments
- API authentication (optional)
- Input validation on all fields
- No data persistence
