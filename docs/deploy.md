Step 1: create .env file in alembic folder with DATABASE_URL url containing Supabase direct connection URL
Step 2: cd backend
Step 3: alembic upgrade head
Step 4: create nothinbutnet render environment using the following values: CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET, CLOUDINARY_CLOUD_NAM, DATABASE_URL(session pooler), PYTHON_VERSION, SECRET_KEY
Step 5: https://nothingbutnet-0l0a.onrender.com/health
