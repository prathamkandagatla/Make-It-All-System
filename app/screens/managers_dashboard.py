import sys
import matplotlib.pyplot as plt
from PySide6 import QtCore, QtGui, QtWidgets

"""
the main dashboard class with functions inside which are called when buttons are pressed
"""
class managersDashboard(QtWidgets.QWidget):

  """
  this function has all the initial layout of the page when you first selct a project
  """
  def __init__(self):
    super().__init__()

    #title label
    self.title = QtWidgets.QLabel(
        "Choose a project to see it's task delegation and progession and assign tasks",
        alignment=QtCore.Qt.AlignCenter,
    )
    
    #drop down option or type in text box to choose the project 
    self.projectSearch = QtWidgets.QComboBox()
    self.projectSearch.setPlaceholderText("Project:")
    self.projectSearch.addItems([
        "Project 1",
        "Project 3",
        "Project 4"
    ])
    self.projectSearch.setEditable(True)
    self.projectSearch.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

    #submit button
    self.submitProject = QtWidgets.QPushButton("Submit")
    self.submitProject.setStyleSheet("background-color: #f5a623; color: #1e1e1e")

    #assign task button but it appears later when the submit button is pressed 
    self.taskButton = QtWidgets.QPushButton("Assign Tasks")
    self.taskButton.hide()
    
    #a box for the pie chart to go into
    self.outputTask = QtWidgets.QWidget()
    self.outputLayout = QtWidgets.QVBoxLayout(self.outputTask)

    #setting the main layout
    self.mainLayout = QtWidgets.QVBoxLayout(self)
    self.mainLayout.setAlignment(QtCore.Qt.AlignTop)
    self.mainLayout.setSpacing(10)

    #the text next to the dropdown box to give it context
    self.searchRowLayout = QtWidgets.QHBoxLayout()
    self.searchRowLayout.addWidget(QtWidgets.QLabel("Project:"))
    self.searchRowLayout.addWidget(self.projectSearch, 1)
    
    #layout all the widgets in the right place on the page 
    self.mainLayout.addWidget(self.title)
    self.mainLayout.addLayout(self.searchRowLayout)
    self.mainLayout.addWidget(self.submitProject)
    self.mainLayout.addWidget(self.outputTask)
    self.mainLayout.addWidget(self.taskButton)   

    #calling the functions when the specific button is pressed 
    self.submitProject.clicked.connect(self.submitClicked)
    self.taskButton.clicked.connect(self.assignTaskButton)


  """
  function which clears the outputs wehn you re press the submit button 
  """
  def clearOutput(self):
    while self.outputLayout.count():
      child = self.outputLayout.takeAt(0)
      if child.widget():
        child.widget().deleteLater()

  """
  Function which is called when you press the submit button after choosing the project 
  it creates the pie chart with the info in the text file
  """
  @QtCore.Slot()
  def submitClicked(self):
    #clears any other pie chart which is already there 
    self.clearOutput()

    #opens the project files used for the pie chart 
    try:
      delegationFile = open("projectDelegation.txt", "r").readlines()
    except FileNotFoundError:
      self.outputLayout.addWidget(
          QtWidgets.QLabel("Error: projectDelegation.txt not found.")
      )
      return

    #running variables to update how big the pie chart slices need to be
    #in the hardcoded verion this will not be the case as we dont know how many employees there will be from signing up so it will need to be dynamic
    statEmployee1 = 0
    statEmployee2 = 0
    statEmployee3 = 0
    statEmployee4 = 0
    statEmployee5 = 0
    positiveProgress = 0
    overallProgress = 0
    #gets the project which has been inputted 
    searchVal = self.projectSearch.currentText()

    #ensures there is a something in the project search bar 
    if searchVal == "":
      self.outputLayout.addWidget(QtWidgets.QLabel("Please enter a search"))
    
    #if there is a project then it can split up the file and every time it reads the employees it can add a task to their running total
    #for that project as well it will check its completion status and add it to a running total
    else:
      for line in delegationFile[1:]:
        cleanline = line.strip()
        delegationRecord = cleanline.split(",")
        if len(delegationRecord) > 3:
          if delegationRecord[0] == searchVal:
            employee = delegationRecord[1]
            status = delegationRecord [3]
            if employee==("Alice"):
              statEmployee1 += 1
            elif employee==("Bert"):
              statEmployee2 += 1
            elif employee==("Clara"):
              statEmployee3 += 1
            elif employee==("Dilip"):
              statEmployee4 += 1
            elif employee==("Emma"):
              statEmployee5 += 1
            if status == ("Complete"):
              positiveProgress += 1
              overallProgress +=1
            elif status == ("In Progress"):
              overallProgress +=1

      #creates counts of how many tasks employees have by getting the employee variables 
      employee = ["Alice", "Bert", "Clara", "Dilip","Emma"]
      counts = [statEmployee1, statEmployee2, statEmployee3, statEmployee4, statEmployee5]
      

      #if there are no tasks assigned to anyone then there will be no pie charts just this message 
      if sum(counts) == 0:
        self.outputLayout.addWidget(QtWidgets.QLabel(f"No employee tasks found for {searchVal}."))
        return

      #creating a pie chart with the data from count and using a specific colour scheme and a title
      #then it saves it as a file which can be accessed later 
      plt.figure(figsize=(5, 4))
      colours = ['#f5a623', "#e5e5e5", "#ffb84d", "#A1A1A1","#555555"]
      plt.pie(counts, labels=employee, autopct="%1.1f%%", colors=colours)
      plt.title(f"Task Delegation for {searchVal}")
      plt.savefig("DelegationStat.png")
      plt.close()

      #puts the pie chart file into a box so that it can be dislplayed as the file that was created earlier
      img_label = QtWidgets.QLabel()
      pixmap = QtGui.QPixmap("DelegationStat.png")
      img_label.setPixmap(
          pixmap.scaled(
              400,
              400,
              QtCore.Qt.KeepAspectRatio,
              QtCore.Qt.SmoothTransformation,
          )
      )
      
      #creates the percentage to show in the progress bar if there are tasks assigned to that project 
      if overallProgress > 0:
        progressPercentage = int ((positiveProgress / overallProgress)*100)
      else:
        progressPercentage = 0

      #creating the progress bar with the information from the variables 
      progressBar = QtWidgets.QProgressBar()
      progressBar.setRange(0, 100)
      progressBar.setValue(progressPercentage)
      

      #adding the widgets to the layout and also showing the assign button after it was hidden 
      self.outputLayout.addWidget(img_label, alignment=QtCore.Qt.AlignCenter)
      self.outputLayout.addWidget(QtWidgets.QLabel(f"Project Progress ({positiveProgress}/{overallProgress} tasks completed):"))
      self.outputLayout.addWidget(progressBar)
      self.taskButton.show()

  """
  this function is called when a manager clicks on the assign task button 
  it gives you all the boxes to fill in to put a task on the file 
  """
  @QtCore.Slot()
  def assignTaskButton(self):
    #clears any task input which is already there 
    self.clearOutput()
    #this creates a grey box for the assign task boxes to go into
    self.formContainer = QtWidgets.QWidget()
    self.formContainer.setStyleSheet("background-color: #f2f2f2; border-radius: 5px; padding: 10px;")
    formLayout = QtWidgets.QVBoxLayout(self.formContainer)
    #text to ensure that he user knows the assigning tasks ar for the project they selected 
    formLayout.addWidget(QtWidgets.QLabel("Assign tasks for " + self.projectSearch.currentText()),alignment=QtCore.Qt.AlignCenter)

    #employee info filling in data area
    empRowLayout = QtWidgets.QHBoxLayout()
    self.employeeNameLabel = QtWidgets.QLabel(("Employee Name:"))
    self.employeeName = QtWidgets.QLineEdit()
    self.employeeName.setPlaceholderText("Enter name here")
    self.employeeName.setStyleSheet("background-color: #ffffff; border: 1px solid #b0b0b0; border-radius: 4px; padding: 5px;")
    empRowLayout.addWidget(self.employeeNameLabel)
    empRowLayout.addWidget(self.employeeName, 1)
    formLayout.addLayout(empRowLayout)

    #task description filling in data area
    taskRowLayout = QtWidgets.QHBoxLayout()
    self.taskDescriptionLabel = QtWidgets.QLabel(("Task Description:"))
    self.taskDescription = QtWidgets.QLineEdit()
    self.taskDescription.setPlaceholderText("Enter description here")
    self.taskDescription.setStyleSheet("background-color: #ffffff; border: 1px solid #b0b0b0; border-radius: 4px; padding: 5px;")
    taskRowLayout.addWidget(self.taskDescriptionLabel)
    taskRowLayout.addWidget(self.taskDescription, 1)
    formLayout.addLayout(taskRowLayout)
    
    #submit button so the task can update on the file
    self.taskSubmit = QtWidgets.QPushButton("Submit Task")
    self.taskSubmit.setStyleSheet("background-color: #555555; color: #ffffff; padding: 6px; border-radius: 4px;")
    formLayout.addWidget(self.taskSubmit)
    self.outputLayout.addWidget(self.formContainer)

    #when the submit button is clicked it calls this function 
    self.taskSubmit.clicked.connect(self.saveTaskClicked)


  """
  This function lets the task that the manager inputs be saved on a file so employees to do lists will be updated 
  it opens the file and updates it while making sure essential values are filled in 
  """
  @QtCore.Slot()
  def saveTaskClicked(self):
    #opens teh file and sets a varaible for if the employee exists 
    employeeFile = open("employee.txt","r")
    found = False
    #finds the inputted employee
    for line in employeeFile:
        cleanline = line.strip()
        record = cleanline.split(",")
        if len(record) >=2  :
          if record [0] == self.employeeName.text():
            found = True
            break
    #closes the file 
    employeeFile.close()
    #if the employee hasnt been found then the text box is cleared and a message is given 
    if found == False:
      self.outputLayout.addWidget(QtWidgets.QLabel("This employee hasn't been found"))
      self.employeeName.clear()
    
    #if the name has been found, then the task can be added to the delegation file safely 
    if found == True:
      #opens the file 
      delegationFile = open("projectDelegation.txt","a")
      #inputs a new line of data onto the file which takes the data from the text boxes the user has submitted 
      new_line = f"{self.projectSearch.currentText()},{self.employeeName.text()},{self.taskDescription.text()},{"In Progress"}\n"
      delegationFile.write(new_line)
      self.outputLayout.addWidget(QtWidgets.QLabel("The task was sucessfully added to the employees to-do list"))
      #clears the boxes ready for a new task 
      self.employeeName.clear()
      self.taskDescription.clear()
      #closes the file 
      delegationFile.close()
    
    
"""
calls the managers dashbaord widget in a window
"""
if __name__ == "__main__":
  app = QtWidgets.QApplication(sys.argv)
  widget = managersDashboard()
  widget.resize(800, 700)
  widget.show()
  sys.exit(app.exec())