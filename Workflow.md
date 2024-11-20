# **Development Workflow Overview**
1. **Frontend Development (Vue.js)**: 
   - Build the user interface (UI).
   - Handle user interactions, forms, buttons, and data visualization.
   - Make API requests to the backend when needed.

2. **Backend Development (Django)**:
   - Process business logic.
   - Handle database operations and API endpoints.
   - Perform server-side actions (e.g., running Python scripts, retrieving data).

3. **Frontend and Backend Interaction**:
   - Use **REST APIs** to allow the frontend to send data to the backend and fetch results.
   - Use **Axios** or other HTTP clients in Vue.js to call Django endpoints.

---

### **Step-by-Step Development Workflow**

#### **1. Web Page Development**
The web page (UI) will be developed in the **Vue.js frontend**. For example:
- Buttons, forms, and other user interaction elements go in the Vue.js components.
- You will define Vue.js components for each page or feature.

Example:
In `frontend/src/App.vue`:
```vue
<template>
  <div id="app">
    <h1>Task Manager</h1>
    <form @submit.prevent="createTask">
      <input v-model="task" placeholder="Enter a task" />
      <button type="submit">Add Task</button>
    </form>
    <ul>
      <li v-for="task in tasks" :key="task.id">{{ task.name }}</li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      task: '',
      tasks: [],
    };
  },
  methods: {
    async fetchTasks() {
      const response = await axios.get('http://127.0.0.1:8000/api/tasks/');
      this.tasks = response.data;
    },
    async createTask() {
      const response = await axios.post('http://127.0.0.1:8000/api/tasks/', {
        name: this.task,
      });
      this.tasks.push(response.data);
      this.task = ''; // Clear the input field
    },
  },
  mounted() {
    this.fetchTasks();
  },
};
</script>

<style>
/* Add your styles here */
</style>
```

---

#### **2. Backend Development**
The backend handles the business logic and exposes APIs to the frontend.

1. **Define Models (Database Structure)**:
   Models represent the structure of your data in the database.

   In `home/models.py`:
   ```python
   from django.db import models

   class Task(models.Model):
       name = models.CharField(max_length=255)
       created_at = models.DateTimeField(auto_now_add=True)

       def __str__(self):
           return self.name
   ```

2. **Create the Database Table**:
   Run migrations to create the table:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Write API Views**:
   In `home/views.py`, define functions or class-based views to handle API requests:
   ```python
   from rest_framework.decorators import api_view
   from rest_framework.response import Response
   from .models import Task

   @api_view(['GET'])
   def get_tasks(request):
       tasks = Task.objects.all().values('id', 'name')
       return Response(list(tasks))

   @api_view(['POST'])
   def create_task(request):
       name = request.data.get('name')
       if name:
           task = Task.objects.create(name=name)
           return Response({'id': task.id, 'name': task.name})
       return Response({'error': 'Name is required'}, status=400)
   ```

4. **Add URLs**:
   In `home/urls.py`:
   ```python
   from django.urls import path
   from . import views

   urlpatterns = [
       path('api/tasks/', views.get_tasks, name='get_tasks'),
       path('api/tasks/', views.create_task, name='create_task'),
   ]
   ```

5. **Test Your API**:
   Use tools like **Postman** or **Bruno** to test your API endpoints (e.g., `http://127.0.0.1:8000/api/tasks/`).

---

### **3. Connecting Frontend and Backend**
The Vue.js frontend interacts with the Django backend using **Axios**. Each button or form action in Vue.js triggers an Axios request to the corresponding Django endpoint.

1. **GET Request Example**:
   Fetch data from the backend:
   ```javascript
   async fetchTasks() {
       const response = await axios.get('http://127.0.0.1:8000/api/tasks/');
       this.tasks = response.data;
   }
   ```

2. **POST Request Example**:
   Send data to the backend:
   ```javascript
   async createTask() {
       const response = await axios.post('http://127.0.0.1:8000/api/tasks/', {
           name: this.task,
       });
       this.tasks.push(response.data);
       this.task = ''; // Clear the input field
   }
   ```

---

### **Project Directory Structure**
Your project directory should now look like this:
```
django_vue_project/
├── venv/                         # Python virtual environment
├── backend/                      # Django backend
│   ├── backend/                  # Django project folder
│   │   ├── settings.py           # Django settings
│   │   ├── urls.py               # Project-level URLs
│   ├── home/                     # Django app
│   │   ├── models.py             # Database models
│   │   ├── views.py              # API views
│   │   ├── urls.py               # App-level URLs
│   │   ├── templates/            # Django templates
│   │   │   └── home/index.html   # Optional Django templates
│   ├── manage.py                 # Django management script
├── frontend/                     # Vue.js frontend
│   ├── src/                      # Vue source code
│   │   ├── App.vue               # Main Vue app
│   │   ├── components/           # Vue components
│   │   ├── main.js               # Vue entry point
│   ├── package.json              # Vue dependencies
│   ├── vite.config.js            # Vue configuration
```

---

### **How to Start Developing Features**
1. **Frontend Workflows**:
   - Create components for new pages or features.
   - Use Axios to interact with APIs.
   - Handle user input and display results dynamically.

2. **Backend Workflows**:
   - Add models for new data structures.
   - Create views for new business logic.
   - Test API endpoints with tools like Postman or cURL.

3. **Testing**:
   - Test APIs independently before connecting to the frontend.
   - Test frontend functionality after integrating APIs.

---

### **How the Frontend Executes Python Backend Commands**
1. **Frontend (Vue.js)**:
   - Triggers an API call (e.g., via a button or form).
   - Example:
     ```vue
     <button @click="executeCommand">Run Command</button>
     ```

   - Axios sends a request:
     ```javascript
     async executeCommand() {
         const response = await axios.get('http://127.0.0.1:8000/api/command/');
         console.log(response.data);
     }
     ```

2. **Backend (Django)**:
   - Responds to the API call with Python logic.
   - Example in `views.py`:
     ```python
     import subprocess
     @api_view(['GET'])
     def execute_command(request):
         result = subprocess.run(['echo', 'Hello, Django!'], stdout=subprocess.PIPE)
         return Response({'output': result.stdout.decode()})
     ```

   - Result is returned to the frontend.

---
