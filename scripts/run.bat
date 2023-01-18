@echo off

:: Activate virtual environment
if not defined VIRTUAL_ENV (
	call .venv\Scripts\activate
)

:: Run development server
python app/manage.py runserver localhost:80
