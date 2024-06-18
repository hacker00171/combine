from click import DateTime
from sqlalchemy import Column, Integer, String, ForeignKey,DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime


SQLALCHEMY_DATABASE_URL='postgresql://postgres:1234@localhost/nested'
Base=declarative_base()

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

Base.metadata.create_all(bind=engine)

# Session = sessionmaker(bind=engine)
session = Session()


#class are created

class Clinic_Details(Base):
    __tablename__="clinic_details"

    id=Column(Integer, primary_key=True)
    name=Column(String)
    city=Column(String)
    state=Column(String)
    zipcode=Column(Integer)

    clinic_detail=relationship("Doctor_Details",back_populates="d_clinic")
    patient_detail=relationship("Patients_Details",back_populates="p_clinics")


class Doctor_Details(Base):
    __tablename__="doctors"

    id=Column(Integer,primary_key=True)
    clinic_id=Column(Integer,ForeignKey("clinic_details.id"))
    name=Column(String)
    speciality=Column(String)
    patients_id=Column(Integer,ForeignKey("patients.id"))

    d_clinic=relationship("Clinic_Details",back_populates="clinic_detail")
    d_patient=relationship("Patients_Details",back_populates="p_doctor")


class Patients_Details(Base):
    __tablename__="patients"

    id=Column(String,primary_key=True)
    name=Column(String)
    age=Column(Integer)
    clinic_id=Column(Integer,ForeignKey("clinic_details.id"))
    last_visit=Column(DateTime)
    doctor_id=Column(Integer,ForeignKey("doctors.id"))

    p_doctor=relationship("Doctor_Details",back_populates="d_patient")
    p_clinics=relationship("Clinic_Details",back_populates="clinic_detail")


    


data = {
    "Clinic_name": "ABC Medical Clinic",
    "location": {
        "city": "New York",
        "state": "NY",
        "zipcode": "10001"
    },
    "doctors": [
        {
            "name": "Dr. Smith",
            "specialty": "Cardiology",
            "patients": [
                {
                    "name": "John Doe",
                    "age": 45,
                    "gender": "Male",
                    "last_visit": "2024-06-10"
                },
                {
                    "name": "Jane Smith",
                    "age": 35,
                    "gender": "Female",
                    "last_visit": "2024-05-20"
                }
            ]
        },
        {
            "name": "Dr. Brown",
            "specialty": "Pediatrics",
            "patients": [
                {
                    "name": "Michael Johnson",
                    "age": 8,
                    "gender": "Male",
                    "last_visit": "2024-06-05"
                },
                {
                    "name": "Emily Davis",
                    "age": 10,
                    "gender": "Female",
                    "last_visit": "2024-06-12"
                }
            ]
        }
    ]
}


clinic = Clinic_Details(
    name=data["Clinic_name"],
    city=data["location"]["city"],
    state=data["location"]["state"],
    zipcode=data["location"]["zipcode"]
)
session.add(clinic)
session.commit()  


for dvalue in data["doctors"]:
    doctor=Doctor_Details(
        name=dvalue["name"],
        clinic_id=Clinic_Details.id,
        speciality=dvalue["speciality"]
    )
    session.add(doctor)


    for pvalue in dvalue.get("patients",{}):
        
        date= pvalue["last_visit"]
        format='%Y-%m-%d'

        patient=Patients_Details(
        name=pvalue["name"],
        age=pvalue["age"],
        gender=pvalue["gender"],
        clinic_id=Clinic_Details.id,
        doctor_id=Doctor_Details.id,
        last_vist=datetime.strptime(date,format)
        )
        session.commit()




    



