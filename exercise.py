import PySimpleGUI as sg
import psycopg2

from constants import HOST, DATABASE, USER, PORT, PASSWORD


class ExerciseForm:
    def __init__(self):

        sg.theme('TanBlue')

        # design the form
        self.frame = [
            [sg.Text('Exercises', justification='Right', size=(45, 1))],
            [sg.Text('Name of Exercise:', size=(6, 1)), sg.InputText(size=(24, 1), key='name'),
             sg.Text(''), sg.Combo(values=[], size=(24, 10), enable_events=True, key='selExercise', readonly=True)],
            [sg.Text('')],
            [sg.Text('')],
            [sg.Text('')]
        ]

        self.layout = [
            [sg.Text('')],
            [sg.Frame('', self.frame, title_color='blue')],
            [sg.Text('')],
            [sg.Text('', size=(8, 1)),
             sg.Button(button_text='Add', key='add', size=(8, 1)),
             sg.Button(button_text='Update', key='update', size=(8, 1)),
             sg.Button(button_text='Delete', key='delete', size=(8, 1)),
             sg.Button(button_text='Close', key='close', size=(8, 1))
             ]
        ]

        # Create the form
        self.window = sg.Window('Exercise').Layout(self.layout).Finalize()
        self.populate_exercises()
        self.rows = []

        # Read the form
        while True:
            event, values = self.window.Read()

            if event == 'add':
                self.add_exercise(values)
            elif event == 'selExercise':
                self.select_exercise(values)
            elif event == 'update':
                self.update_exercise(values)
            elif event == 'delete':
                self.delete_exercise()
            elif event == 'close':
                break

        self.window.Close()

    def add_exercise(self, values):
        conn = None

        try:
            conn = psycopg2.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD,
                                    port=PORT)
            cur = conn.cursor()
            exercise_name = str(values['name'])

            exercise_insert = 'INSERT INTO "Exercises" (exercise_name) VALUES(%s);'
            exercise_rec = (exercise_name,)
            cur.execute(exercise_insert, exercise_rec)
            conn.commit()

            x = f'Exercise called {exercise_name} is inserted into the list of performed exercises'
            sg.Popup(x)

            self.clear_fields()
            self.populate_exercises()

        except (Exception, psycopg2.DatabaseError) as error:
            sg.Popup("addExercise", str(error))

        finally:
            if conn is not None:
                cur.close()
                conn.close()

    def populate_exercises(self):

        data = []
        conn = None

        try:
            conn = psycopg2.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD,
                                    port=PORT)
            cur = conn.cursor()

            select_exercises = 'SELECT id FROM "Exercises"'
            print(select_exercises)
            cur.execute(select_exercises)
            self.rows = cur.fetchall()

            data.clear()
            for row in self.rows:
                data.append(row[0:2])

            self.window.FindElement("selExercise").Update(values=data)

            self.clear_fields()

        except (Exception, psycopg2.DatabaseError) as error:
            sg.Popup("Populate Exercises", str(error))

        finally:
            if conn is not None:
                cur.close()
                conn.close()

    def select_exercise(self, values):
        global idexSelected
        print(values)
        idexSelected = values['selExercise'][0]

        for row in self.rows:
            if (idexSelected == row[0]):
                self.window.FindElement("name").Update(str(row[0]))
                break

    def update_exercise(self, values):
        conn = None

        try:
            conn = psycopg2.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD,
                                    port=PORT)
            cur = conn.cursor()

            exercise_name = str(values['name'])
            exercise_update = 'UPDATE "Exercises" SET exercise_name=%s WHERE id=%s'
            cur.execute(exercise_update, (exercise_name, idexSelected))
            conn.commit()

            x = f"Exercise {exercise_name} is updated"
            sg.Popup(x)
            self.clear_fields()
            self.populate_exercises()

        except (Exception, psycopg2.DatabaseError) as error:
            sg.Popup("Update", str(error))

        finally:
            if conn is not None:
                cur.close()
                conn.close()

    def delete_exercise(self):
        conn = None

        try:
            conn = psycopg2.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD,
                                    port=PORT)
            cur = conn.cursor()

            exercise_delete = 'DELETE FROM "Exercises" WHERE id=%s'
            cur.execute(exercise_delete, (idexSelected,))
            conn.commit()

            sg.Popup("Exercise is deleted")
            self.clear_fields()
            self.populate_exercises()

        except (Exception, psycopg2.DatabaseError) as error:
            sg.Popup("Delete Exercise", str(error))

        finally:
            if conn is not None:
                cur.close()
                conn.close()

    def clear_fields(self):
        self.window.FindElement("name").Update('')


if __name__ == '__main__':
    ExerciseForm()
