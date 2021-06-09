import exercise
from users import *
from exercise import *


class ActivityForm:
    def __init__(self):

        sg.theme('TanBlue')

        global data
        global dSelected
        data = []

        col_headings = ['Exercise name', 'Repetitions', 'Exercise date']
        d0 = ['', '', '', '', '']
        data.append(d0)

        self.menu_health = [
            ['Open', ['User', 'Exercise']],
            ['Exit', ['Exit']]
        ]

        self.frameUser = [
            [sg.Text('Users', size=(12, 1)),
             sg.Combo(values=[], size=(10, 1), enable_events=True, tooltip='Users', key='selUSER', readonly=True)],
            [sg.Text('Name: ', size=(12, 1)), sg.Input(size=(20, 1), key='name', disabled=True)],
            [sg.Text('Surname: ', size=(12, 1)), sg.Input(size=(20, 1), key='surname', disabled=True)],
            [sg.Text('Age ', size=(12, 1)), sg.Input(size=(20, 1), key='age', disabled=True)],
            [sg.Text('Gender: ', size=(12, 1)), sg.Radio('Female', 'R', size=(10, 1), key='female', disabled=True),
             sg.Radio('Male', 'R', size=(10, 1), key='male', disabled=True)],
            [sg.Text('Weight (kg): ', size=(12, 1)), sg.Input(size=(20, 1), key='weight', disabled=True)],
            [sg.Text('Height (cm): ', size=(12, 1)), sg.Input(size=(20, 1), key='height', disabled=True)],
            [sg.Text('BMI: ', size=(15, 1)), sg.Text(size=(20, 1), justification='right', key='bmi')]
        ]

        self.frameExercise = [
            [sg.Text('Exercise', size=(10, 1)),
             sg.Combo(values=[], size=(24, 10), enable_events=True, key='selEXERCISE', readonly=True,
                      tooltip='Exercises')],
            [sg.Text('Reps', size=(10, 1)), sg.Input(size=(13, 1), key='selREP', enable_events=True)],
            [sg.Text('')],
            [sg.CalendarButton('Exercise Date', target='input', key='date'),
             sg.Button(button_text='OK', key='OK')],
            [sg.In('', size=(20, 1), key='input')],
            [sg.Text('')],
            [sg.Text('')],
            [sg.Text('')],
        ]

        self.frameSchedule = [
            [sg.Table(values=data[0:][:], headings=col_headings, key='TABLE', num_rows=10, enable_events=True,
                      justification='center',
                      auto_size_columns=True)],
            [sg.Text('', size=(20, 1)), sg.Button(button_text='Add', key='ADD', size=(8, 1)),
             sg.Button(button_text='Close', key='DONE', size=(8, 1)),
             sg.Button(button_text='Get Data', key='GET_DATA', size=(8, 1)),
             ]
        ]

        self.frameEditForms = [
            [sg.Button(button_text='Edit exercise', key='EDIT_EXERCISE', size=(12, 1))],
            [sg.Button(button_text='Edit user', key='EDIT_USER', size=(12, 1))],
        ]

        self.layout = [
            [sg.Menu(self.menu_health, tearoff=False, visible=True)],
            [
                sg.Frame('', self.frameExercise, title_color='blue'),
                sg.Frame('', self.frameUser, title_color='blue')
            ],
            [
                sg.Frame('', self.frameSchedule, title_color='blue', size=(10, 1)),
                sg.Frame('', self.frameEditForms, title_color='blue', size=(10, 1))
            ],
            [sg.Text('')]
        ]

        self.window = sg.Window('Exercise tracker').Layout(self.layout).Finalize()

        self.users_populate()
        self.exercises_populate()

        while True:
            event, values = self.window.Read()
            if event == 'User':
                UserForm()
            elif event == 'Exercise':
                ExerciseForm()
            elif event == 'Exit':
                break
            elif event == 'selUSER':
                self.user_selected(values)
            elif event == 'selEXERCISE':
                self.exercise_selected(values)
            elif event == 'selREP':
                self.rep_selected(values)
            elif event == 'OK':
                print(values['input'][0:10])
                dSelected = values['input'][0:10]
            elif event == 'ADD':
                self.add_health(values)
            elif event == 'TABLE':
                self.row_selected(values)
            elif event == 'UPDATE':
                self.update_health(values)
            elif event == 'DELETE':
                self.delete_health(values)
            elif event == 'EDIT_EXERCISE':
                ExerciseForm()
            elif event == 'EDIT_USER':
                UserForm()
            elif event == 'GET_DATA':
                self.users_populate()
                self.exercises_populate()
            elif event == 'DONE':
                break
            else:
                break
        self.window.Close()

    def users_populate(self):
        dataU = []
        conn = None

        try:
            conn = psycopg2.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD,
                                    port=PORT)
            cur = conn.cursor()

            select_users = 'SELECT * FROM "Users" ORDER BY id'
            cur.execute(select_users)
            self.rowsU = cur.fetchall()

            dataU.clear()
            for row in self.rowsU:
                dataU.append(row[0:3])

            self.window.FindElement('selUSER').Update(values=dataU)

        except (Exception, psycopg2.DatabaseError) as error:
            sg.Popup("Populate Users", str(error))

        finally:
            if conn is not None:
                cur.close()
                conn.close()

    def exercises_populate(self):
        dataE = []
        conn = None

        try:
            conn = psycopg2.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD,
                                    port=PORT)

            cur = conn.cursor()

            select_exercises = 'SELECT * FROM "Exercises" ORDER BY id'
            cur.execute(select_exercises)
            self.rows = cur.fetchall()

            dataE.clear()
            for row in self.rows:
                dataE.append(row[0:2])

            self.window.FindElement('selEXERCISE').Update(values=dataE)

        except (Exception, psycopg2.DatabaseError) as error:
            sg.Popup("Populate Exercises", str(error))

        finally:
            if conn is not None:
                cur.close()
                conn.close()

    def user_selected(self, values):
        global idSelected
        idSelected = values['selUSER'][0]
        for row in self.rowsU:
            if (idSelected == row[0]):
                self.window.FindElement("name").Update(str(row[1]))
                self.window.FindElement("surname").Update(str(row[2]))
                if str(row[3]).lower() == "male":
                    self.window.FindElement("male").Update(value="True")
                elif str(row[3]).lower() == "female":
                    self.window.FindElement("female").Update(value="True")
                self.window.FindElement("age").Update(str(row[4]))
                self.window.FindElement("weight").Update(str(row[5]))
                self.window.FindElement("height").Update(str(row[6]))
                self.window.FindElement("bmi").Update(str(row[7]))
                break
        self.table_populate()

    @staticmethod
    def exercise_selected(values):
        global idexSelected
        global nameSelected

        idexSelected = values['selEXERCISE'][0]
        nameSelected = values['selEXERCISE'][1]

    def rep_selected(self, values):
        global rpSelected
        rpSelected = values['selREP']

    def table_populate(self):
        conn = None
        data[:] = []
        self.window.Element('TABLE').Update(values=data)
        try:
            conn = psycopg2.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD,
                                    port=PORT)
            cur = conn.cursor()

            select_user_exercises = 'SELECT * FROM "Activity" WHERE user_id = %s ORDER BY id'
            cur.execute(select_user_exercises, (idSelected,))
            self.hRows = cur.fetchall()
            for row in self.hRows:
                print(row)
                selectExercise = 'SELECT * FROM "Exercises" WHERE id=%s'
                cur.execute(selectExercise, (row[2],))
                rowExercise = cur.fetchone()

                d = [rowExercise[1], row[3], row[4]]
                data.append(d)
                self.window.Element('TABLE').Update(values=data)

        except (Exception, psycopg2.DatabaseError) as error:
            sg.Popup("Populate Table", str(error))

        finally:
            if conn is not None:
                cur.close()
                conn.close()

    def add_health(self, values):
        conn = None

        try:
            conn = psycopg2.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD,
                                    port=PORT)
            cur = conn.cursor()
            print(values)
            user_id = idSelected
            exercise_id = idexSelected
            rep = rpSelected
            exercise_date = values["input"]
            health_insert = 'INSERT INTO "Activity" (user_id, exercise_id, rep, exercise_date) VALUES(%s, %s, %s, %s)'
            health_rec = (user_id, exercise_id, rep, exercise_date)
            cur.execute(health_insert, health_rec)
            conn.commit()

            self.table_populate()

        except (Exception, psycopg2.DatabaseError) as error:
            sg.Popup("Add Activity report", str(error))

        finally:
            if conn is not None:
                cur.close()
                conn.close()

    @staticmethod
    def row_selected(values):
        global rowInd
        global rowValues

        rowInd = values['TABLE'][0]
        rowValues = data[rowInd]

    def update_health(self, values):
        rowValues[3] = rpSelected
        rowValues[4] = dSelected
        conn = None

        try:
            conn = psycopg2.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD,
                                    port=PORT)
            cur = conn.cursor()

            health_update = 'UPDATE "Activity" SET rep=%s, exercise_date=%s WHERE id=%s'
            cur.execute(health_update, (rowValues[3], rowValues[4], rowValues[0]))
            conn.commit()

            data[rowInd] = rowValues
            self.window.Element('TABLE').Update(values=data)

        except (Exception, psycopg2.DatabaseError) as error:
            sg.Popup("Update health report", str(error))

        finally:
            if conn is not None:
                cur.close()
                conn.close()

    def delete_health(self, values):
        conn = None
        try:
            conn = psycopg2.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD,
                                    port=PORT)
            cur = conn.cursor()

            health_delete = 'DELETE FROM "Activity" WHERE id=%s'
            cur.execute(health_delete, (rowValues[0],))
            conn.commit()

            del data[rowInd]
            self.window.Element('TABLE').Update(values=data)

        except (Exception, psycopg2.DatabaseError) as error:
            sg.Popup("Delete Activity report", str(error))

        finally:
            if conn is not None:
                cur.close()
                conn.close()


if __name__ == '__main__':
    ActivityForm()
