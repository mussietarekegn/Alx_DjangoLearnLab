### Running Tests

To execute API tests:

    python manage.py test api

These tests verify:
✔ CRUD operations for the Book API  
✔ Authentication enforcement  
✔ Filtering by author  
✔ Searching book titles  
✔ Ordering by publication year  

All tests run on a separate test database, ensuring no modification to production data.
