# ClearView: Improving X-Ray Image Quality — Setup Guide

Medical workers in underserved communities do not have immediate access to adequate imaging equipment, leading to low-quality/lack of necessary images for diagnoses. Diagnoses could be more accurate with improved x-ray quality, leading to life-saving outcomes in many cases with basic x-ray images. 

We worked on making an open-source technical pipeline that improves X-Ray Quality. This guide walks you through setting up and running the our project from scratch. It's written to be beginner-friendly — no prior experience with Git or VS Code is assumed.

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
1. Fork the GitHub repository and clone it to your computer
2. Create your own branch to work on
3. Install required dependencies
4. Run the backend (Python)
5. Run the frontend (React)
6. Make changes, commit, and push them

## 1. Access the Repository and Set Up Git

### a. Fork the Repository

1. Go to [https://github.com/TanmayJDesai/MedicalImageImprovement](https://github.com/TanmayJDesai/MedicalImageImprovement)
2. Click the "Fork" button in the top-right corner
3. This creates a copy of the repository in your GitHub account

### b. Clone Your Forked Repository

Open your terminal (Mac) or Command Prompt (Windows):

```bash
git clone https://github.com/YOUR_USERNAME/MedicalImageImprovement.git
cd MedicalImageImprovement
```

### c. Add the Original Repository as a Remote

This allows you to pull updates from the original repository:

```bash
git remote add upstream https://github.com/TanmayJDesai/MedicalImageImprovement.git
```

## 2. Create Your Own Branch

Create and switch to a new branch using your name:

```bash
git checkout -b yourname
```

For example:
```bash
git checkout -b john-smith
```

This makes it clear who owns each branch and simplifies merging at the project's conclusion.

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

## 5. Making Changes and Contributing

### a. Make Your Changes

1. Open the project in VS Code: `code .`
2. Make changes to the files you want to modify
3. Test your changes locally

### b. Commit Your Changes

```bash
# See what files you've changed
git status

# Add the files you want to commit
git add file1 file2

# Or add all changed files
git add .

# Commit with a descriptive message
git commit -m "Add feature X" or "Fix bug Y"
```

### c. Push Your Changes to GitHub

```bash
git push origin yourname
```

### d. Create a Pull Request

1. Go to your forked repository on GitHub
2. Click the "Pull Request" button
3. Select your branch and click "Create Pull Request"
4. Add a title and description explaining your changes
5. Submit the pull request

## 6. Keeping Your Fork Updated

To get updates from the original repository:

```bash
git checkout main
git pull upstream main
git push origin main
```

Then switch back to your personal branch:

```bash
git checkout yourname
git merge main
```

## 7. Opening the Project in VS Code

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

### Git Authentication Issues

If you're having trouble authenticating with GitHub:
1. Make sure you've set up SSH keys or using GitHub CLI
2. Or use HTTPS with a personal access token
3. See GitHub's documentation: [https://docs.github.com/en/authentication](https://docs.github.com/en/authentication)

## Notes

- The backend runs on port 5000, and the frontend runs on port 3000.
- Both must be running simultaneously for the application to function.
- Always work on your own name-based branch - don't work directly on the main branch.
- Include descriptive commit messages to explain your changes.
