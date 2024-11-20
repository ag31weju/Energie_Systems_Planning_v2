
# Django + Vue.js Full-Stack Project

This guide walks you through setting up a full-stack project with **Django** as the backend and **Vue.js** as the frontend. The backend uses the Django REST framework to serve data to the Vue.js frontend. 

---

## Prerequisites

Before starting, ensure you have the following installed:
- Python 3.9 or higher
- Node.js and npm (or yarn)
- Git (optional but recommended)

---

## Project Structure

After completing the setup, your project directory structure will look like this:

```
django_vue_project/
├── venv/                     # Python virtual environment
├── backend/                  # Django backend
│   ├── backend/              # Main project folder
│   ├── home/                 # Django app folder
│   ├── db.sqlite3            # SQLite database
│   └── manage.py             # Django management script
├── frontend/                 # Vue.js frontend
│   ├── src/                  # Source code
│   ├── public/               # Static files
│   ├── package.json          # Frontend dependencies
│   └── vite.config.js        # Vite configuration
```

---

## Step 1: Set Up the Django Backend

### 1.1 Create a Virtual Environment
```bash
# Create a project directory
mkdir django_vue_project
cd django_vue_project

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 1.2 Install Django and Dependencies
```bash
pip install django djangorestframework django-cors-headers
```

### 1.3 Start the Django Project
```bash
django-admin startproject backend
cd backend
python manage.py startapp home
```

### 1.4 Update Django Settings
Edit `backend/settings.py`:
- Add `home` and `rest_framework` to `INSTALLED_APPS`:
  ```python
  INSTALLED_APPS = [
      'django.contrib.admin',
      'django.contrib.auth',
      'django.contrib.contenttypes',
      'django.contrib.sessions',
      'django.contrib.messages',
      'django.contrib.staticfiles',
      'rest_framework',
      'corsheaders',  # For CORS
      'home',
  ]
  ```
- Add CORS settings for Vue.js:
  ```python
  MIDDLEWARE = [
      'corsheaders.middleware.CorsMiddleware',  # Add before other middleware
      'django.middleware.common.CommonMiddleware',
      # other middleware
  ]

  CORS_ALLOWED_ORIGINS = [
      'http://localhost:5173',  # Vue.js dev server
  ]
  ```

### 1.5 Create Backend URLs and Views
- Update `backend/urls.py`:
  ```python
  from django.contrib import admin
  from django.urls import path, include

  urlpatterns = [
      path('admin/', admin.site.urls),
      path('', include('home.urls')),
  ]
  ```
- Create `home/urls.py`:
  ```python
  from django.urls import path
  from . import views

  urlpatterns = [
      path('', views.index, name='index'),
  ]
  ```
- Create a basic view in `home/views.py`:
  ```python
  from django.http import JsonResponse

  def index(request):
      return JsonResponse({'message': 'Hello from Django!'})
  ```

### 1.6 Run the Server
```bash
python manage.py migrate
python manage.py runserver
```

Test the backend by navigating to `http://127.0.0.1:8000/` in your browser.

---

## Step 2: Set Up the Vue.js Frontend

### 2.1 Initialize Vue.js
```bash
cd ..
npx create-vue@latest frontend
cd frontend
```

When prompted, select the following:
- **TypeScript support**: No
- **ESLint**: Yes (optional)
- **Router**: No

### 2.2 Install Axios
```bash
npm install axios
```

### 2.3 Update Vue.js Entry Files
- Update `frontend/src/main.js`:
  ```javascript
  import { createApp } from 'vue';
  import App from './App.vue';

  createApp(App).mount('#app');
  ```
- Edit `frontend/src/App.vue`:
  ```vue
  <template>
    <div id="app">
      <h1>Vue.js Frontend</h1>
      <button @click="fetchMessage">Fetch Message</button>
      <p v-if="message">{{ message }}</p>
    </div>
  </template>

  <script>
  import axios from 'axios';

  export default {
    data() {
      return {
        message: '',
      };
    },
    methods: {
      async fetchMessage() {
        try {
          const response = await axios.get('http://127.0.0.1:8000/');
          this.message = response.data.message;
        } catch (error) {
          console.error('Error fetching data:', error);
        }
      },
    },
  };
  </script>

  <style>
  body {
    font-family: Arial, sans-serif;
  }
  </style>
  ```

---

## Step 3: Run Both Servers

### 3.1 Start the Django Server
```bash
cd backend
python manage.py runserver
```

### 3.2 Start the Vue.js Development Server
```bash
cd ../frontend
npm run dev
```

Navigate to `http://127.0.0.1:5173` in your browser to view the Vue.js app. When you click the "Fetch Message" button, it will fetch data from the Django backend.

---

## Additional Notes

### To Build and Serve Vue.js in Production
1. Build the Vue.js app:
   ```bash
   npm run build
   ```
2. Copy the `frontend/dist` folder into Django’s `static` directory.
3. Update Django settings to serve static files.

---

## Troubleshooting

1. **CORS Issues**: Ensure `CORS_ALLOWED_ORIGINS` is correctly configured in `settings.py`.
2. **Backend Not Responding**: Check if the Django server is running on `http://127.0.0.1:8000/`.

---

## Future Enhancements

- Add routing to Vue.js for multiple pages.
- Integrate Django models and serializers.
- Use Vuex or Pinia for state management.

---

## License

This project is licensed under the MIT License.
