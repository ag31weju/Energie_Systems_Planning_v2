# Energy System Planning

This project is designed to help school students understand the challenges of energy system planning and learn about gradient-based mathematical optimization methods. It leverages Python and Django to create an educational and interactive web application.

## Table of Contents
1. [Requirements](#requirements)
2. [Installation](#installation)
3. [Getting Started](#getting-started)
4. [Contributing](#contributing)
5. [License](#license)

---

## Requirements

Before starting, ensure you have the following:
- **Git** installed on your computer
- **Python 3.12.7** installed (Microsoft Store has python 3.12.7, for linux you can use Conda if needed)
- **GitLab Account**: You'll need to generate a personal access token on GitLab for repository access.

## Installation

Follow these instructions to set up the project locally.

### 1. Install Git and check python version 

Make sure Git is installed on your machine and the python version is 3.12.7 with `python --version` (windows)

### 2. Generate a Personal Access Token

To securely access the repository, generate a personal access token on the GitLab website `https://git.rwth-aachen.de/`. Go to **Preferences > Access Tokens > Add new token**, create a new token with appropriate permissions, and keep it safe for later use as needed.

### 3. Clone the Repository
Go to folder of your choice on your device and open CMD/Bash in that directory `(Right click > Open in terminal)` and use the following command to clone the repository, replacing `<username>` and `<personal_access_token>` with your GitLab username and personal access token:

```bash
git clone https://<username>:<personal_access_token>@git.rwth-aachen.de/kartikeya.chaudhary/energy_system_planning.git
```
**You may be asked to authenticate with manager, provide your Uni email in username field and the Personal access token as password.**

### 4. Set Up the Virtual Environment

Open the project with your code editor, navigate into the project directory with terminal and create a virtual environment for dependency management 

```bash
python -m venv venv
```

Activate the virtual environment:

- **On Windows:**
  ```bash
  .\venv\Scripts\activate

  .\venv\Scripts\Activate.ps1 (powershell)
  ```
- **On macOS/Linux:**
  ```bash
  source venv/bin/activate
  ```

### 5. Install Required Packages

Install the dependencies listed in `requirements.txt`

```bash
pip install -r requirements.txt
```

---

## Getting Started

After setting up the environment, you can start the development server and explore the application.
1. Launch Visual Studio Code.
2. Open the project folder
3. When prompted, select the `venv` environment as the interpreter for the workspace, or activate it as explained previously
4. Change directory to the django project by navigating to \main with `cd main`
5. `python manage.py runserver` to start the server
---

## Contributing

n/a

---

## License

n/a

---
