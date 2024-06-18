from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


from marshmallow import Schema, fields
from marshmallow_sqlalchemy.fields import Nested
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

import json
from sqlalchemy.orm import Session,sessionmaker
from database import engine
Session = sessionmaker(bind=engine)
session = Session()



# from schema import UserSchema,ProductSchema,AddressSchema,OrderSchema,CategorySchema

Base = declarative_base()#used need to know

class Product(Base):
    __tablename__="products"

    id=Column(Integer,primary_key=True)
    name=Column(String,nullable=False)
    category=Column(Integer,ForeignKey("categorys.id"),nullable=False)
    price=Column(Integer,nullable=False)
    stock=Column(Integer,nullable=False)
    brand=Column(String,nullable=False)
    model=Column(String,nullable=False)
    warranty=Column(String,nullable=False)

    order=relationship("Order",back_populates="product")
    c_name=relationship("Category",back_populates="cat_name")



class User(Base):
    __tablename__="users"

    id=Column(Integer,primary_key=True)
    name=Column(String,nullable=False)
    email=Column(String,nullable=False)
    phone=Column(String,nullable=False)

    orders=relationship("Order",back_populates="user")
    addres=relationship("Address",back_populates="address")



class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    
    quantity = Column(Integer, nullable=False)

    user = relationship("User", back_populates="orders")
    product = relationship("Product", back_populates="order")


class Category(Base):
    __tablename__="categorys"

    id=Column(Integer,primary_key=True)
    product_name=Column(String,nullable=False)

    cat_name=relationship("Product",back_populates="c_name")


class Address(Base):
    __tablename__="address"

    id=Column(Integer,primary_key=True)
    street=Column(String,nullable=False)
    city=Column(String,nullable=False)
    state=Column(String,nullable=False)
    zipcode=Column(Integer,nullable=False)
    country=Column(String,nullable=False)

    user_id =Column(Integer, ForeignKey("users.id"),nullable=False)

    address=relationship("User",back_populates="addres")







