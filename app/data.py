"""Hard-coded sample data (users, projects, tasks, topics, posts) shaped like database tables with ids. Replaced by the database in Part II."""


# - projects data by Pratham
projects = [
    {"id": 1, "name": "Test Project 1", "deadline": "2027-02-01"},
    {"id": 2, "name": "Test Project 2", "deadline": "2027-03-15"},
    {"id": 3, "name": "Test Project 3", "deadline": "2027-04-30"},
    {"id": 4, "name": "Test Project 4", "deadline": "2027-05-20"},  # no tasks yet
]
 
# - tasks data by Pratham showing test cases
tasks = [
    # Project 1: partly done
    {"id": 1, "projectId": 1, "title": "Task 1", "status": "done"},
    {"id": 2, "projectId": 1, "title": "Task 2", "status": "todo"},
    {"id": 3, "projectId": 1, "title": "Task 3", "status": "todo"},
    # Project 2: all done
    {"id": 4, "projectId": 2, "title": "Task 1", "status": "done"},
    {"id": 5, "projectId": 2, "title": "Task 2", "status": "done"},
    {"id": 6, "projectId": 2, "title": "Task 3", "status": "done"},
    # Project 3: none done
    {"id": 7, "projectId": 3, "title": "Task 1", "status": "todo"},
    {"id": 8, "projectId": 3, "title": "Task 2", "status": "todo"},
    {"id": 9, "projectId": 3, "title": "Task 3", "status": "todo"},
    # Project 4 has no tasks
]
ROLES = ("Employee", "Manager")
# - end of pratham's data

# - users data by Andy
USERS = [
    {
        "id": 1,
        "email": "J.Smith@make-it-all.co.uk",
        "password": "M4keItAll123?",
        "name": "John Smith",
        "role": "Employee",
        "teamIds": [1], 
    },
    {
        "id": 2,
        "email": "G.Smith@make-it-all.co.uk",
        "password": "M4keItAll321!",
        "name": "George Smith",
        "role": "Manager",
        "teamIds": [1, 2], 
    }
]

# - end of andy's data