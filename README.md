# 🚀 GitHub Webhook Listener & Activity Feed  

This project receives GitHub webhook events (Push, Pull Request, and Merge), stores minimal event data in MongoDB, and displays the latest repository activity in a simple UI that refreshes every 15 seconds.

📦 This repository (`webhook-repo`) contains:
- Flask backend webhook receiver  
- MongoDB integration  
- Minimal UI for displaying events  

A separate repository (`action-repo`) is used to trigger GitHub actions.

⚠️ **NOTE**:
- This app is deployed on Render free tier. The first request after inactivity may take a few seconds while the service wakes up.
- This project uses Gunicorn as the production WSGI server when deployed on Render.

🔗 Live Demo:
- **Webhook Receiver**: https://webhook-repo-k0r5.onrender.com/webhook/receiver
- **UI**: https://webhook-repo-k0r5.onrender.com/webhook/

---

## 🧰 Tech Stack

- **Python** (Flask)  
- **MongoDB** (PyMongo)  
- **HTML**, **CSS**, **JavaScript**  
- **Gunicorn**  

---

## 📂 Project Structure

```text
webhook-repo/  
├── app/  
│   ├── __init__.py  
│   ├── extensions.py  
│   └── webhook/  
│       ├── __init__.py  
│       └── routes.py  
├── ui/  
│   └── index.html  
├── Procfile  (for render, Gunicorn)
├── run.py  
├── requirements.txt  
└── README.md
```
---

## 🔁 Application Flow

GitHub Repo (action-repo)
→ GitHub Webhook  
→ Flask Receiver (/webhook/receiver)  
→ MongoDB  
→ Flask API (/webhook/events)  
→ UI (polls every 15 seconds)

---


## 🗄️ MongoDB Schema

Each webhook event is stored as:

```json
{
  "request_id": "string",
  "author": "string",
  "action": "PUSH | PULL_REQUEST | MERGE",
  "from_branch": "string | null",
  "to_branch": "string",
  "timestamp": "UTC datetime string"
}
```
---

## 🔌 API Endpoints

- POST /webhook/receiver → Receive GitHub webhook (payload endpoint)
- GET /webhook/events → Get latest 10 events
- GET /webhook/ → UI page

---


## ⚙️ Local Setup

### 📥 Clone Repository

```bash
git clone https://github.com/navu545/webhook-repo.git 
cd webhook-repo
```

### 🧪 Create Virtual Environment
```bash
pip install virtualenv  
virtualenv venv
```
Activate (Windows):
```bash
venv\Scripts\activate
```
Activate (macOS/Linux):
```bash
source venv/bin/activate
```

### 📦 Install Dependencies
```bash
pip install -r requirements.txt  
```
### 🗄️ Configure MongoDB

You can use your localhost to host the DB or a service like Mongo Atlas

Update in app/__init__.py:

`app.config["MONGO_URI"] = "<your-mongodb-connection-string>"`

Note: In real-world applications, sensitive values should be stored using environment variables.

### ▶️ Run Server

```bash
python run.py
```

Open UI in browser:

`http://localhost:5000/webhook/` 

Live Demo:
https://webhook-repo-k0r5.onrender.com/webhook/

---

## 🔔 GitHub Webhook Setup

Inside action-repo:

Settings → Webhooks → Add Webhook  

Payload URL:

`<your-deployed-backend-url>/webhook/receiver`

Content-Type:
`application/json`  

Select events:
- Push  
- Pull requests  

Save.

Live Demo:
https://webhook-repo-k0r5.onrender.com/webhook/receiver

---

## 📌 Repositories

Webhook Repo: https://github.com/navu545/webhook-repo 
Action Repo: https://github.com/navu545/action-repo 

---

## 👤 Author

Navdeep Singh
