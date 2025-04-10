## Setting Up the Development Environment

Follow these steps to set up the project locally: (python 3.11.8 and django 4.1.13)

1. **Create a Virtual Environment**  
   Isolate project dependencies to avoid conflicts with system-wide packages. Make sure to use Python 3.11.8.
   ```bash
   python3.11 -m venv venv
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

## Deploying to Render

This project is configured for deployment on Render. Follow these steps to deploy:

1. **Push Your Code to GitHub**  
   Make sure your code is pushed to a GitHub repository.

2. **Sign Up for Render**  
   Create an account at [render.com](https://render.com) if you don't have one.

3. **Create a New Web Service**  
   - Connect your GitHub repository
   - Render will automatically detect the `render.yaml` configuration
   - Alternatively, you can manually configure:
     - Build Command: `./build.sh`
     - Start Command: `gunicorn healthstack.wsgi:application --bind 0.0.0.0:$PORT`
     - Python Version: `3.11.8`

4. **Set Environment Variables**  
   Add all required environment variables from your `.env` file in the Render dashboard:
   - `SECRET_KEY`
   - `DEBUG` (set to "False" for production)
   - `GEMINI_API_KEY`
   - `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`
   - `STORE_ID`, `STORE_PASSWORD`, `STORE_NAME`

5. **Deploy Your Application**  
   Click "Create Web Service" and Render will build and deploy your application.

6. **Set Up a Database**  
   - Create a PostgreSQL database in Render
   - Render will automatically set the `DATABASE_URL` environment variable
   - The application is configured to use this database in production
