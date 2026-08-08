# CiviSense AI

### AI-powered civic issue reporting and analysis

CiviSense is an AI application that helps citizens report and understand civic problems such as potholes, damaged infrastructure, and electrical hazards.

Users can upload an image of an issue, provide optional details and location, and receive an AI-powered assessment of the problem.

## How It Works

```text
Citizen
   ↓
Upload Image
   ↓
Gemma 4 Analysis
   ↓
Issue Detection + Severity Score
   ↓
Risks & Recommended Actions
   ↓
Complaint / Resolution Guidance
Key Features
📷 Image-based civic issue analysis
🤖 Powered by Google Gemma 4
📊 Issue severity scoring from 1–10
⚠️ Potential risk identification
📝 Actionable citizen instructions
✉️ AI-generated complaint letters
🏛️ Authority routing through a deterministic backend system
Tech Stack

Frontend

React
Vite
Lucide React
Vercel

Backend

Python
FastAPI
Google Gemini/Gemma API

AI

Google Gemma 4
Project Structure
civiс-issue-analyser/
├── backend/
│   ├── api/
│   ├── services/
│   └── data/
├── frontend/
│   ├── src/
│   └── public/
├── tests/
├── .env.example
├── .gitignore
└── README.md
Environment Variables

Create a .env file locally:

GOOGLE_API_KEY=your_api_key
GEMMA_MODEL=your_gemma_model

Never commit your API key to GitHub.

Goal

CiviSense aims to turn a simple photograph into an actionable civic report, helping citizens understand the seriousness of an issue and take the appropriate next step.