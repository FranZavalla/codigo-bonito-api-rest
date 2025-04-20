from pony.orm import Database, Required

db = Database()

class Product(db.Entity):
    name = Required(str)
    description = Required(str)
    price = Required(float)
