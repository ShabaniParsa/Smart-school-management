from pdfEx import PDF
import json
class ClassCalculator():
    def __init__(self,Company = "Python") -> None:

        '''This class is designed for the best possible management of schools or educational institutions.
        It is recommended that only the management of the complex use this service in order to protect and respect the rights of teachers and students.
        Otherwise, our company does not have any responsibility for the failure to respect the rights of teachers and students.'''

        try:
            with open("information.json") as file:
                fl = json.load(file)
                try:
                    self.Teachers = fl['Teachers']
                    self.Students = fl['Students']
                    self.Company = fl['Company']
                except:
                    self.Teachers = {}
                    self.Students = {}
                    self.Company = Company
        except:
            open("informaion.json",'w')
            self.Teachers = {}
            self.Students = {}
            self.Company = Company
    
    def RegisterTeacher(self,id:str,name:str,percent:int):
        '''To register or log in as a new teacher to your program, you must use this method.
        You must enter the ID, name, and the percentage of your maximum salary received by each student.'''

        id = str(id)
        self.Teachers.setdefault(id,{"name":name,"students":{},"price_percent":percent,"invoice":0})
        self.UpdateJson()

    def RegisterStudent(self,id:str,name:str,teacher_id:int,price:int,date:int):

        '''To register a student, you must use this method.
        You must enter the student's ID, name, instructor ID, full tuition amount, and duration of teaching with that instructor.
        To enroll a student in another class, you must first delete (expell) the student and then re-register him/her.'''

        id = str(id)
        if teacher_id in list(self.Teachers.keys()):
            self.Students.setdefault(id,{"name":name,"teacher_id":teacher_id,"price":price,'date':date})
            self.Teachers[teacher_id]["students"].setdefault(id,{"all_price":price,"get":0,"done":0})
            self.UpdateJson()
        else:
            raise KeyError("Teacher doesnt found!!!")


    def Persent(self,id:str):

        '''To register a student in person, you must use this method.
        In this method, when you register a student in person, the relevant teacher will receive the calculated salary for that session (in the invoice) according to a mathematical formula.'''

        id = str(id)
        if id in list(self.Students.keys()):
            if self.Teachers[self.Students[id]['teacher_id']]['students'][id]['done'] != self.Students[id]['date']:
                self.Teachers[self.Students[id]['teacher_id']]['students'][id]['get'] += ((self.Teachers[self.Students[id]['teacher_id']]['students'][id]['all_price']/100)*self.Teachers[self.Students[id]['teacher_id']]['price_percent'])/self.Students[id]['date']
                self.Teachers[self.Students[id]['teacher_id']]['invoice'] += ((self.Teachers[self.Students[id]['teacher_id']]['students'][id]['all_price']/100)*self.Teachers[self.Students[id]['teacher_id']]['price_percent'])/self.Students[id]['date']
                self.Teachers[self.Students[id]['teacher_id']]['students'][id]['done'] += 1
                self.UpdateJson()
            else:
                raise ValueError("Date of youre work is done!")
        else:
            raise KeyError("Student doesnt found!!!")

    def Absent(self,id:str):

        '''You should use this method to report the absence of a student.
        If a student is absent, that student's salary for that day will not be added to the teacher's invoice.'''

        id = str(id)
        if id in list(self.Students.keys()):
            if self.Teachers[self.Students[id]['teacher_id']]['students'][id]['done'] != self.Students[id]['date']:
                self.Teachers[self.Students[id]['teacher_id']]['students'][id]['done'] += 1
                self.UpdateJson()
            else:
                raise ValueError("Date of youre work is done!")
        else:
            raise KeyError("Student doesnt found!!!")


    def FireTeacher(self,id:str,new_sd_t_id:str):

        '''To fire a teacher or in other words, delete them from the database, you must use this method.
        You must enter a new teacher ID for the old students of the teacher being fired, otherwise you will encounter problems and errors.'''

        id = str(id)
        new_sd_t_id = str(new_sd_t_id)
        if id in list(self.Teachers.keys()):
            if new_sd_t_id in list(self.Teachers.keys()):
                for ids in list(self.Teachers[id]['students'].keys()):
                    self.Students[ids]['teacher_id'] = new_sd_t_id
                self.GetInvoice(id)
                del self.Teachers[id]
                self.UpdateJson()
            else:
                raise KeyError("The new teacher doesnt found and the fire process have failed.First add new teacher or fire students.")
        else:
            raise KeyError("Teacher doesnt found!!!")
            
    def FireStudent(self,id):

        '''To expel a student or in other words, delete a student from your database, you must use this method.'''

        id = str(id)
        if id in list(self.Students.keys()):
            del self.Teachers[self.Students[id]['teacher_id']]['students'][id]
            del self.Students[id]
            self.UpdateJson()
        else:
            raise KeyError("Student doesnt found!!!")
        
    def GetInvoice(self,id:str):

        '''To receive a teacher's invoice, you must use this method.
        This method, with the ID of the teacher you want, gives you an invoice for that teacher's salary and saves it in a file named (invoice.pdf).'''

        id = str(id)
        if id in list(self.Teachers.keys()):
            invoice = self.Teachers[id]['invoice']
            pdf = PDF()
            pdf.add_page()
            pdf.chapter_title(f"{self.Teachers[id]['name']} Invoice")
            pdf.chapter_body(f"Youre Invoice is: {invoice}Rial\nfrom {self.Company} Company.\nYou can send this invoice to your company's president or CEO to receive your salary!")
            pdf.output("Invoice.pdf")
        else:
            raise KeyError("Teacher doesnt found!!!")
    
    def UpdateJson(self):
        dics = {"Students":self.Students,"Teachers":self.Teachers,"Company":self.Company}
        with open("information.json",'w') as file:
            json.dump(dics,file,indent=3)

