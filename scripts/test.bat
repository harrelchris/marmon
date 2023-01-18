@echo off

:: Activate virtual environment
if not defined VIRTUAL_ENV (
	call .venv\Scripts\activate
)

:: Run Pytest with Coverage and generate reports
coverage erase
coverage run -m pytest --html=.reports/pytest/index.html --self-contained-html
coverage html
