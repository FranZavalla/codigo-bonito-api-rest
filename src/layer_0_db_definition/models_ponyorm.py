from pony.orm import Database, Required

db = Database()


class Product(db.Entity):
    _table_ = "product"

    name = Required(str)
    price = Required(float)
