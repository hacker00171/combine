from marshmallow import Schema, fields
from marshmallow_sqlalchemy.fields import Nested
from models import Product,Order,Category,User,Address
from sqlalchemy.orm import sessionmaker

import json
from sqlalchemy.orm import Session
from database import engine
Session = sessionmaker(bind=engine)
session = Session()


# class AddressSchema(Schema):
#     id = fields.Integer()
#     street = fields.String()
#     city = fields.String()
#     state = fields.String()
#     zipcode = fields.Integer()
#     country = fields.String()

# class CategorySchema(Schema):
#     id = fields.Integer()
#     product_name = fields.String()

# class OrderSchema(Schema):
#     id = fields.Integer()
#     quantity = fields.Integer()

# # class ProductSchema(Schema):
# #     id = fields.Integer()
# #     name = fields.String()
# #     price = fields.Integer()
# #     stock = fields.Integer()
# #     brand = fields.String()
# #     model = fields.String()
# #     warranty = fields.String()

# #     category = fields.Nested('CategorySchema')
# #     orders = fields.List(fields.Nested('OrderSchema', exclude=('product',)))



# class ProductSchema(Schema):
#     id = fields.Integer()
#     name = fields.String()
#     price = fields.Integer()
#     stock = fields.Integer()
#     brand = fields.String()
#     model = fields.String()
#     warranty = fields.String()

#     # Nested relationships
#     category = fields.Nested(CategorySchema)
#     orders = fields.List(fields.Nested(OrderSchema))

# class UserSchema(Schema):
#     id = fields.Integer()
#     name = fields.String()
#     email = fields.String()
#     phone = fields.String()

#     # Nested relationships
#     orders = fields.List(fields.Nested(OrderSchema))
#     address = fields.List(fields.Nested(AddressSchema))




# result=session.query(Product).all()
# print(result)
# output=ProductSchema(many=True).dump(result)
# print(output)





class ProductSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    price = fields.Integer()
    stock = fields.Integer()
    brand = fields.String()
    model = fields.String()
    warranty = fields.String()
    category = fields.Nested('CategorySchema')

class CategorySchema(Schema):
    id = fields.Integer()
    name = fields.String()
    products = fields.List(fields.Nested('ProductSchema'))

class UserSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    email = fields.String()
    phone = fields.String()
    orders = fields.List(fields.Nested('OrderSchema'))
    addresses = fields.List(fields.Nested('AddressSchema'))

class OrderSchema(Schema):
    id = fields.Integer()
    quantity = fields.Integer()
    user = fields.Nested('UserSchema')
    product = fields.Nested('ProductSchema')

class AddressSchema(Schema):
    id = fields.Integer()
    street = fields.String()
    city = fields.String()
    state = fields.String()
    zipcode = fields.Integer()
    country = fields.String()

# Create tables in the database

# Example usage: querying and serializing data
products = session.query(Product).all()
product_schema = ProductSchema(many=True)
output = product_schema.dump(products)



with open("sample1.json","w") as json_file:
    json.dump(output,json_file,indent=5)








