"""Shared helpers used across screens, e.g. formatting dates for display."""
from app.data import tasks

# -returns the list of tasks that belong to a project
def getProjectTasks(project):
    return [task for task in tasks if task["projectId"] == project["id"]]
 
 # -returns the list of the tasks that belong to a project.
def countTasks(project):
    return len(getProjectTasks(project))
 
 # -returns how many of a project's tasks have the given status ("todo" or "done").
def countTasksByStatus(project, status):
    
    return len([task for task in getProjectTasks(project) if task["status"] == status])
 
 # -returns how many of a project's tasks are done.
def countDoneTasks(project):
    return countTasksByStatus(project, "done")
 
 # -returns what percentage of a project's tasks are done (0 if it has no tasks(test case)).
def getPercentage(project):
    totalTasks = countTasks(project)
    if totalTasks == 0:
        return 0
    tasksDone = countDoneTasks(project)
    return round((tasksDone / totalTasks) * 100)
