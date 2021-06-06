import PySimpleGUI as sg
import psycopg2

from constants import HOST, DATABASE, USER, PASSWORD, PORT


class UserForm:
    def __init__(self):
        sg.theme('TanBlue')

        self.frame_layout = [
            [sg.Text('Users', justification='right', size=(60, 1))],
            [sg.Text('Name: ', size=(12, 1)), sg.Input(size=(20, 1), key='name'),
             sg.Text('', size=(12, 1)), sg.Combo([], size=(20, 1), enable_events=True, key='selUser', readonly=True)],
            [sg.Text('Surname: ', size=(12, 1)), sg.Input(size=(30, 1), key='surname')],
            [sg.Text('Age: ', size=(12, 1)), sg.Input(size=(30, 1), key='age')],
            [sg.Text('Gender: ', size=(12, 1)),
             sg.Radio('Female', 'R', size=(10, 1), key='female'),
             sg.Radio('Male', 'R', size=(10, 1), key='male')],
            [sg.Text('Weight (kg): ', size=(12, 1)), sg.Input(size=(30, 1), key='weight')],
            [sg.Text('Height (cm): ', size=(12, 1)), sg.Input(size=(30, 1), key='height')],
            [sg.Text('BMI: ', size=(15, 1)), sg.Text(size=(20, 1), justification='right', key='bmi')],
            [sg.Text('')]
        ]

        self.layout = [
            [sg.Frame('', self.frame_layout, title_color='blue')],
            [sg.Text('')],
            [sg.Text('', size=(8, 1)), sg.Button('Add', size=(8, 1), key='add'),
             sg.Button('Update', size=(8, 1), key='update'),
             sg.Button('Delete', size=(8, 1), key='delete'),
             sg.Button('Close', size=(8, 1), key='close'),
             sg.Button('Populate', size=(8, 1), key='populate')],
            [sg.Text('')]
        ]

        self.window = sg.Window('User Form').Layout(self.layout).Finalize()

        self.populate_users()

        while True:
            event, values = self.window.Read()
            if event == 'add':
                self.add_user(values)
            elif event == 'selUser':
                self.select_user(values)
            elif event == 'populate':
                self.populate_users()
            elif event == 'update':
                self.update_user(values)
            elif event == 'delete':
                self.delete_user()
            elif event == 'close':
                break

        self.window.Close()

    def add_user(self, values):
        conn = None

        try:
            conn = psycopg2.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD,
                                    port=PORT)

            cur = conn.cursor()

            # get values from the form
            name = str(values['name'])
            surname = str(values['surname'])
            age = str(values['age'])
            gender = ""

            if values['female']:
                gender = "Female"
            elif values['male']:
                gender = "male"

            weight = str(values['weight'])
            height = str(values['height'])
            weightInt = float(values['weight'])
            heightInt = float(values['height']) / 100
            bmiInt = (weightInt / (heightInt * heightInt))
            bmi = str(weightInt / (heightInt * heightInt))

            # define Insert sting
            userInsert = 'INSERT INTO "Users" (name,surname,age,gender,weight,height,bmi) VALUES (%s,%s,%s,%s,%s,%s,%s)'
            userRec = (name, surname, age, gender, weight, height, bmi)
            cur.execute(userInsert, userRec)
            conn.commit()

            a = 'BMI MEANING'
            if (bmiInt < 18.5):
                a = 'Underweight'
            elif (bmiInt >= 18.5) and (bmiInt <= 24.9):
                a = 'Normal weight'
            elif (bmiInt >= 25) and (bmiInt <= 29.9):
                a = 'Overweight'
            elif (bmiInt >= 30):
                a = 'Obese'

            x = f"User {surname} is inserted into database, BMI: {bmi}, according to BMI, you are {a}"
            sg.Popup(x)

            # clear
            self.clear_fields()
            self.populate_users()

        except (Exception, psycopg2.DatabaseError) as error:
            sg.Popup("addUser", str(error))

        finally:
            if conn is not None:
                cur.close()
                conn.close()

    def populate_users(self):

        data = []
        conn = None

        try:
            conn = psycopg2.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD,
                                    port=PORT)
            cur = conn.cursor()

            selectUsers = 'SELECT * FROM "Users" ORDER BY id'
            cur.execute(selectUsers)
            self.rows = cur.fetchall()

            # data[:] = []
            data.clear()
            for row in self.rows:
                data.append(row[0:3])

            self.window.FindElement("selUser").Update(values=data)

            self.clear_fields()

        except (Exception, psycopg2.DatabaseError) as error:
            sg.Popup("Populate", str(error))

        finally:
            if conn is not None:
                cur.close()
                conn.close()

    def select_user(self, values):
        global idSelected

        idSelected = values['selUser'][0]

        for row in self.rows:
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

    def update_user(self, values):
        conn = None

        try:
            conn = psycopg2.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD,
                                    port=PORT)
            cur = conn.cursor()

            name = str(values['name'])
            surname = str(values['surname'])
            age = str(values['age'])

            selectUser = 'SELECT * FROM "Users" WHERE id=%s'
            cur.execute(selectUser, (idSelected,))
            self.row = cur.fetchone()

            if values['female']:
                gender = "Female"
            else:
                gender = "male"

            weight = str(values['weight'])
            height = str(values['height'])
            weightInt = float(values['weight'])
            heightInt = float(values['height']) / 100
            bmi = str(weightInt / (heightInt * heightInt))

            userUpdate = 'UPDATE "Users" SET name=%s, surname=%s, age=%s, gender=%s, weight=%s, height=%s, bmi=%s WHERE id=%s'
            cur.execute(userUpdate, (name, surname, age, gender, weight, height, bmi, idSelected))
            conn.commit()

            x = "Record " + name + " " + surname + " is updated, BMI: " + bmi
            sg.Popup(x)
            self.clear_fields()
            self.populate_users()

        except (Exception, psycopg2.DatabaseError) as error:
            sg.Popup("Update", str(error))

        finally:
            if conn is not None:
                cur.close()
                conn.close()

    def delete_user(self):
        conn = None

        try:
            conn = psycopg2.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD,
                                    port=PORT)
            cur = conn.cursor()

            userDelete = 'DELETE FROM "Users" WHERE id=%s'
            cur.execute(userDelete, (idSelected,))
            conn.commit()

            sg.Popup("Record is deleted")
            self.clear_fields()
            self.populate_users()

        except (Exception, psycopg2.DatabaseError) as error:
            sg.Popup("Delete", str(error))

        finally:
            if conn is not None:
                cur.close()

                conn.close()

    def clear_fields(self):
        self.window.FindElement("name").Update('')
        self.window.FindElement('surname').Update('')
        self.window.FindElement("age").Update('')
        self.window.FindElement("female").Update(value='True')
        self.window.FindElement("height").Update('')
        self.window.FindElement("weight").Update('')
        self.window.FindElement("bmi").Update('')


if __name__ == '__main__':
    UserForm()
