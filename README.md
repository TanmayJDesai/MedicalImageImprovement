# Medical Image Improvement — Setup Guide
## Prerequisites

Before you begin, make sure you have the following installed:
- Git
- Python 3.8 or higher
- Node.js and npm
- Visual Studio Code

### Download Links

- Git: [https://git-scm.com/downloads](https://git-scm.com/downloads)
- Python: [https://www.python.org/downloads/](https://www.python.org/downloads/)
- Node.js: [https://nodejs.org/](https://nodejs.org/)
- VS Code: [https://code.visualstudio.com/](https://code.visualstudio.com/)

## Overview of Steps

You will:
1. Create a GitHub repository and connect it to your computer
2. Clone the project files
3. Install required dependencies
4. Run the backend (Python)
5. Run the frontend (React)

## 1. Set Up Git and GitHub

### a. Create a GitHub Repository

1. Go to [github.com](https://github.com) and sign in (or create an account).
2. Click the "+" in the top-right and choose "New repository".
3. Name the repository `MedicalImageImprovement`.
4. Do not initialize with a README, .gitignore, or license.
5. Click "Create repository".

### b. Set Up Your Project Folder Locally

Open your terminal (Mac) or Command Prompt (Windows):

```bash
mkdir MedicalProject
cd MedicalProject
# Initialize a Git repository
git init
# Add your GitHub repo as the remote (replace URL with your GitHub URL)
git remote add origin https://github.com/YOUR_USERNAME/MedicalImageImprovement.git
```

## 2. Clone the Repository

Download the project files to your local machine:

```bash
git clone https://github.com/TanmayJDesai/MedicalImageImprovement.git
cd MedicalImageImprovement
```

## 3. Install Project Dependencies

### A. Backend (Python/Flask)

**Mac**

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Windows**

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### B. Frontend (React)

Works the same on Mac and Windows:

```bash
cd ../frontend
npm install
```

## 4. Running the Application

### A. Start the Backend Server

**Mac**

```bash
cd backend
source venv/bin/activate
python3 app.py
```

**Windows**

```bash
cd backend
venv\Scripts\activate
python app.py
```

The backend will run at http://localhost:5000.

### B. Start the Frontend Server

Open a new terminal window:

```bash
cd frontend
npm start
```

This will open the frontend at http://localhost:3000.

## 5. Opening the Project in VS Code

1. Open Visual Studio Code
2. Click "File" > "Open Folder"
3. Select the MedicalImageImprovement folder
4. Open a terminal in VS Code: "Terminal" > "New Terminal"
5. Follow the instructions above to install dependencies and run the backend and frontend

## Troubleshooting

### Port 5000 Already in Use (Backend)

**Mac**

```bash
lsof -i :5000
kill -9 [PID]
```

**Windows**

```bash
netstat -ano | findstr :5000
taskkill /PID [PID] /F
```

### npm Install Fails (Frontend)

```bash
rm -rf node_modules
npm cache clean --force
npm install
```

## Notes

- The backend runs on port 5000, and the frontend runs on port 3000.
- Both must be running simultaneously for the application to function.
