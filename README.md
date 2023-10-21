# EE308-Assignment2-Back-end
## Calculator API

Features:
- Calculate mathematical expressions
- Store calculation history
- Retrieve and display the last 10 calculations

Usage:

Calculate Result:
You can make POST requests to calculate mathematical expressions using the /calculate_result endpoint.

Example:
curl -X POST -F "formula=2+2" http://127.0.0.1:8000/calculate_result

Set History:
You can save calculation history to the database using the /set_history endpoint.

Example:
curl -X POST -F "data=2+2" http://127.0.0.1:8000/set_history

Read History:
Retrieve the last 10 calculations from the history using the /read_history endpoint.

Example:
curl http://127.0.0.1:8000/read_history

