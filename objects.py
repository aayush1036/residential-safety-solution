class Vehicle:
    def __init__(self,manufacturer=None, model=None,license_no=None, lot_no=None, society=None):
        self.manufacturer = manufacturer
        self.model = model 
        self.license_no = license_no
        self.society = society
        self.parking_lot_number = lot_no
            
    def make_entry(self,connection):
        connection = connection
        query = f"""INSERT INTO VEHICLES (MANUFACTURER, MODEL, LICENSE_NO, SOCIETY, PARKING_LOT_NO) VALUES 
        ('{self.manufacturer}', '{self.model}', '{self.license_no}', '{self.society}' ,'{self.parking_lot_number}')"""
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        connection.close()
    
    def remove(self,connection):
        connection = connection
        query = f"DELETE FROM VEHICLES WHERE PARKING_LOT_NO = '{self.parking_lot_number}'"
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        connection.close()
        
class Person:
    def __init__(self, name=None, age=None, gender=None,contact_no=None, society=None, flat_no=None, aadhar_no=None) -> None:
        self.name = name 
        self.age = age 
        self.gender = gender 
        self.contact_no = contact_no
        self.society = society
        self.flat_no = flat_no
        self.aadhar_no = aadhar_no
        
    def make_entry(self, connection):
        connection = connection
        query = f"""INSERT INTO PERSON (PERSON_NAME, AGE, GENDER, CONTACT_NO, SOCIETY, FLAT_NO, AADHAR_NO) VALUES 
        ('{self.name}', {self.age}, '{self.gender}', '{self.contact_no}','{self.society}' ,'{self.flat_no}', '{self.aadhar_no}')"""
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        connection.close()
    
    def remove(self, connection):
        connection = connection
        query = f"DELETE FROM PERSON WHERE AADHAR_NO = '{self.aadhar_no}'"
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        connection.close()