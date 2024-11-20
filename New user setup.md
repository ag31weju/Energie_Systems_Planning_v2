
# Setting Up the Django + Vue.js Project

This guide explains how a new user who pulls this repository can set it up for local development.

---

## Step 1: Clone the Repository
```bash
git clone <repository_url>
cd django_vue_project
```

---

## Step 2: Set Up the Backend (Django)

### 2.1 Activate the Virtual Environment
```bash
# On macOS/Linux
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

### 2.2 Install Python Dependencies
Install the dependencies from the `requirements.txt` file:
```bash
pip install -r requirements.txt
```

### 2.3 Apply Migrations
```bash
python manage.py migrate
```

### 2.4 Run the Django Development Server
```bash
python manage.py runserver
```

Open your browser and navigate to `http://127.0.0.1:8000` to confirm the backend is working.

---

## Step 3: Set Up the Frontend (Vue.js)

### 3.1 Navigate to the Frontend Directory
```bash
cd frontend
```

### 3.2 Install Frontend Dependencies
```bash
npm install
```

### 3.3 Run the Vue.js Development Server
```bash
npm run dev
```

The frontend will be available at `http://127.0.0.1:5173`.

---

## Exporting Dependencies for Other Users

### For Python (Django Backend)

1. **Generate `requirements.txt`**
   Run the following command in your virtual environment:
   ```bash
   pip freeze > requirements.txt
   ```

2. **Add `requirements.txt` to Version Control**
   Ensure that `requirements.txt` is committed to your Git repository:
   ```bash
   git add requirements.txt
   git commit -m "Add requirements.txt"
   git push
   ```

---

### For npm (Vue.js Frontend)

1. **Ensure `package.json` is Up-to-Date**
   When you install new packages, ensure they are added to `package.json`. Run this command to save changes if required:
   ```bash
   npm install <package_name> --save
   ```

2. **Commit `package.json` and `package-lock.json`**
   These files are used by npm to track dependencies. Make sure they are part of your repository:
   ```bash
   git add package.json package-lock.json
   git commit -m "Update npm dependencies"
   git push
   ```

---

## Final Checklist for New Users

1. Clone the repository.
2. Set up the Python environment (`venv`) using `requirements.txt`.
3. Install frontend dependencies using `npm install`.
4. Run both backend and frontend servers as described above.

This ensures a smooth onboarding experience for anyone pulling the project.
