from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from model import Product
from database import session, engine
import database_models
from sqlalchemy.orm import Session

app= FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_origins=["http://localhost:3000"],
  allow_credentials=True,  
    allow_methods=["*"],
    allow_headers=["*"],
)

database_models.Base.metadata.create_all(bind=engine)

@app.get("/")
def greet():
  return "welcome everyone"

products =[
  Product(id=1,name='mobile',price='17000',description= 'good quality',quantity=2),
  Product(id=2,name='laptop',price='7000',description= 'good quality',quantity=2),
  Product(id=3,name='tablet',price='10000',description= 'good quality',quantity=2),
  Product(id=5,name='tv',price='34000',description= 'good quality',quantity=2)
]

def get_db():
  db= session()
  try:
    yield db 
  finally:
    db.close()

def init_db():
    db = session()
    try:
        # Check if DB is already populated
        if db.query(database_models.Product).count() == 0:
            for product in products:
                db.add(database_models.Product(
                    id=product.id,
                    name=product.name,
                    price=product.price,
                    description=product.description,
                    quantity=product.quantity
                ))
            db.commit()
    finally:
        db.close()

@app.on_event("startup")
def startup_event():
  init_db()

@app.get("/products")
def get_all_products(db: Session=Depends(get_db)):
  
  db_products = db.query(database_models.Product).all()
  return db_products

@app.get("/products/{id}")
def get_product(id:int ,db: Session=Depends(get_db)):
  db_product = db.query(database_models.Product).filter(database_models.Product.id ==id).first()
  if db_product:
    return db_product
  return {"product not found"}

@app.post("/products")
def add_product(product: Product,db: Session=Depends(get_db)):
  db.add(database_models.Product(
                    id=product.id,
                    name=product.name,
                    price=product.price,
                    description=product.description,
                    quantity=product.quantity
                ))
  db.commit()
  return product

@app.put("/products/{id}")
def update_product(id:int , product:Product,db: Session=Depends(get_db)):
  db_product = db.query(database_models.Product).filter(database_models.Product.id ==id).first()
  if db_product:
    db_product.name= product.name
    db_product.price= product.price
    db_product.description= product.description
    db_product.quantity= product.quantity
    db.commit()
    return product

  else:
    return "product not found"

@app.delete("/products/{id}")
def delete_product(id:int, db: Session=Depends(get_db)):
  db_product = db.query(database_models.Product).filter(database_models.Product.id ==id).first()
  if db_product:
    db.delete(db_product)
    db.commit()
    return "product deleted"
  else:
    return "product not found"