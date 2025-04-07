## Setting Up the Development Environment

Follow these steps to set up the project locally: (python 3.11.8 and django 4.1.13)

1. **Create a Virtual Environment**  
   Isolate project dependencies to avoid conflicts with system-wide packages.
   ```bash
   python -m venv venv
   ```

2. **Activate the Virtual Environment**  
   - On **Linux** or **macOS**:  
     ```bash
     source venv/bin/activate
     ```
   - On **Windows**:  
     ```bash
     venv\Scripts\activate
     ```

3. **Install Project Dependencies**  
   Install all required packages listed in `requirements.txt`.
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**  
   Copy the example environment configuration to create your own `.env` file.  
   Update the `.env` file with your project-specific settings (e.g., database credentials).  
   ```bash
   cp .env.example .env
   ```

5. **Upgrade Simple JWT Package**  
   Ensure you're using the latest version of Django REST Framework's Simple JWT for authentication.  
   ```bash
   pip install --upgrade djangorestframework-simplejwt
   ```

6. **Apply Database Migrations**  
   Set up the database schema based on your Django models.  
   ```bash
   python manage.py migrate
   ```

7. **Run the Development Server**  
   Start the Django development server to view your project in the browser at `http://127.0.0.1:8000/`.  
   ```bash
   python manage.py runserver
   ```
