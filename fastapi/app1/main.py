
from sqlalchemy.orm import Session,sessionmaker
import models
from database import engine
from models import User,Product,Order,Address,Category

from schema import UserSchema,ProductSchema,AddressSchema,OrderSchema,CategorySchema


models.Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()
data = {
    "products": {
        1: {
            "name": "Laptop",
            "category": "Electronics",
            "price": 1200.00,
            "stock": 50,
            "details": {
                "brand": "BrandA",
                "model": "X123",
                "warranty": "2 years"
            }
        },
        2: {
            "name": "Smartphone",
            "category": "Electronics",
            "price": 800.00,
            "stock": 200,
            "details": {
                "brand": "BrandB",
                "model": "Y456",
                "warranty": "1 year"
            }
        },
        3: {
            "name": "Office Chair",
            "category": "Furniture",
            "price": 150.00,
            "stock": 100,
            "details": {
                "brand": "BrandC",
                "model": "OC789",
                "warranty": "3 years"
            }
        }
    },
    "users": {
        1: {
            "name": "Alice Smith",
            "email": "alice@example.com",
            "phone": "123-456-7890",
            "address": {
                "street": "123 Maple St",
                "city": "Springfield",
                "state": "IL",
                "zip": "62701",
                "country": "USA"
            },
            "orders": {
                1: 1,
                3: 2
            }
        },
        2: {
            "name": "Bob Johnson",
            "email": "bob@example.com",
            "phone": "234-567-8901",
            "address": {
                "street": "456 Oak St",
                "city": "Monroe",
                "state": "LA",
                "zip": "71201",
                "country": "USA"
            },
            "orders": {
                2: 1
            }
        },
        3: {
            "name": "Charlie Brown",
            "email": "charlie@example.com",
            "phone": "345-678-9012",
            "address": {
                "street": "789 Pine St",
                "city": "Lincoln",
                "state": "NE",
                "zip": "68501",
                "country": "USA"
            },
            "orders": {
                1: 2,
                2: 1,
                3: 1
            }
        }
    }
}




# for c_id,c_values in enumerate(data["products"].get("category")):
#     cat=Category(
#             id=c_id,
#             product_name=c_values
#         )

#     session.add(cat)
#     break



# for pkeys,pvalue in data["products"].items():
#     product=Product(
#         id=pkeys,
#         name=pvalue["name"],
#         category=Category.id,
#         price=pvalue["price"],
#         stock=pvalue["stock"],
#         brand=pvalue["details"]["brand"],
#         model=pvalue["details"]["model"],
#         warranty=pvalue["details"]["warranty"]

#     )
#     session.add(product)
#     session.commit()



for pkey, pvalue in data["products"].items():
    existing_category=session.query(Category).filter_by(product_name=pvalue["category"]).first()
    if existing_category:
        cat=existing_category
    else:
        cat=Category(product_name=pvalue["category"])
        session.add(cat)
        session.commit()

    product = Product(
        id=pkey,
        name=pvalue["name"],
        category=cat.id,
        price=pvalue["price"],
        stock=pvalue["stock"],
        brand=pvalue["details"]["brand"],
        model=pvalue["details"]["model"],
        warranty=pvalue["details"]["warranty"]
    )
    session.add(product)

session.commit()

    
for uid,uvalue in data["users"].items():
    
    address=Address(
        street=uvalue["address"]["street"],
        city=uvalue["address"]["city"],
        state=uvalue["address"]["state"],
        zipcode=uvalue["address"]["zip"],
        country=uvalue["address"]["country"],
        user_id=uid
        )
    users=User(
        id=uid,
        name=uvalue["name"],
        email=uvalue["email"],
        phone=uvalue["phone"],
        # address=uid        
    )
    session.add(users)
    session.add(address)  
  
  
    for oid, details in uvalue.get("orders",{}).items():

        order = session.query(Order).filter_by(id=oid,user_id=User.id, product_id=Product.id).first()
        if order:
            order.quantity += details
        else:
            new_order = Order(
                id=oid,
                user_id=uid,
                product_id=pkey,
                quantity=details
                )
            
        session.add(new_order)
        session.commit()


        # orders=Order(
        #     id=oid,
        #     user_id=uid,
        #     product_id=pkey,
        #     quantity=details
            
        # )
        # session.add(orders)
        # session.commit()



