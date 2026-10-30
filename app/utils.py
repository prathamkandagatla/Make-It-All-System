"""Shared helpers used across screens, e.g. formatting dates for display."""

#  function that returns how many tasks a project has by pratham
def countTasks(project):
    return len(project["tasks"])

#Counts tasks by each status (todo / done) 
#for a breakdown under the bar by pratham
def countTasksByStatus(project, status):
    return len([task for task in project["tasks"] if task["status"] == status])


# A function that returns how many tasks are "done" by pratham

def countDoneTasks(project):
    return countTasksByStatus(project, "done")


#A function that returns the percentage of tasks done by pratham
def getPercentage(project):
    totalTasks = countTasks(project)
    if totalTasks == 0:
        return 0
    else:
        tasksDone = countDoneTasks(project)
        percentage = (tasksDone / totalTasks) * 100
        return round(percentage)
