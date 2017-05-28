from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.listview import ListItemButton

import sqlite3


class StudentListButton(ListItemButton):
    pass


class StudentDB(BoxLayout):

    # Open or create DB
    conn = sqlite3.connect('student.db')

    # Create Cursor
    c = conn.cursor()

    # placeholder
    curr_student = 0

    first_name_text_input = ObjectProperty()
    last_name_text_input = ObjectProperty()
    student_list = ObjectProperty()

    def setup_db(self):

        # Create the table if it doesn't exist
        self.c.execute("CREATE TABLE if not exists Students(ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, " +
                       "FName TEXT NOT NULL, LName TEXT NOT NULL);")

        # save the database file
        self.conn.commit()

        # clear existing list
        self.student_list.adapter.data = ([])

        # update list of students
        allStudents = self.c.execute("Select FName, LName FROM Students")
        for row in allStudents:
            fName = row[0]
            lName = row[1]
            fullName = fName + " " + lName
            self.student_list.adapter.data.extend([fullName])

    def submit_student(self):
        # Get the student's name from textInputs
        fName = self.first_name_text_input.text
        lName = self.last_name_text_input.text
        student_name = fName + " " + lName

        try:
            # add entry to DB
            self.c.execute("INSERT INTO Students (FName, LName) VALUES ('" +
                           fName + "', '" +
                           lName + "')")
            self.conn.commit()
        except:
            print("Student not added to database. Please ensure that both First and Last names are given.")

        # Add to ListView
        self.student_list.adapter.data.extend([student_name])

        # Reset the ListView
        self.student_list._trigger_reset_populate()

    def delete_student(self):
        # If a list item is selected...
        if self.student_list.adapter.selection:

            # Get the text from the item selected
            selection = self.student_list.adapter.selection[0].text

            first_name, last_name = selection.split()

            # Remove the matching item from database
            self.c.execute("DELETE FROM Students WHERE FName = ? AND LName = ?", (first_name, last_name,))
            self.conn.commit()

            # Remove the matching item from ListView
            self.student_list.adapter.data.remove(selection)

            # Reset the ListView
            self.student_list._trigger_reset_populate()

    def replace_student(self):
        # If a list item is selected
        if self.student_list.adapter.selection:

            # Get the text from the item selected
            selection = self.student_list.adapter.selection[0].text
            first_name, last_name = selection.split()

            # Get the new student name from TextInputs
            new_first = self.first_name_text_input.text
            new_last = self.last_name_text_input.text

            # replace value in database
            self.c.execute("UPDATE Students SET FName = '" +
                           new_first +
                           "', LName = '" +
                           new_last +
                           "' WHERE FName = ? AND LName = ?", (first_name, last_name,))

            # update ListView by calling setup_db
            self.setup_db()

class StudentDBApp(App):
    def build(self):
        return StudentDB()

dbApp = StudentDBApp()
dbApp.run()
