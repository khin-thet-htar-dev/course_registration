#!/bin/bash

# Create virtual environment and activate it
python -m venv myeo_env
source myeo_env/bin/activate

# Create requirements.txt
cat > requirements.txt << EOL
Django==5.0.2
djangorestframework==3.14.0
psycopg2-binary==2.9.9
python-dotenv==1.0.1
django-cors-headers==4.3.1
django-filter==23.5
EOL

# Install dependencies
pip install -r requirements.txt

# Create Django project
django-admin startproject backend .

# Create Django apps inside backend directory
cd backend
django-admin startapp courses
django-admin startapp students
django-admin startapp grades
cd ..

# Create frontend directory structure
mkdir -p frontend/src/{components,routes,stores,lib}
mkdir -p frontend/public 