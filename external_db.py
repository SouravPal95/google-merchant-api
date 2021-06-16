from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker


engine=create_engine(
    r"mssql+pymssql://filed_admin:dvserv3#rathena@stage1.ctonnmgtbe2i.eu-west-1.rds.amazonaws.com:1433/Dev3.Filed.ProductCatalogs2",
    echo=False
)

Base=automap_base()
Base.prepare(engine, reflect=True)


FiledVariants=Base.classes.FiledVariants

Session=sessionmaker(bind=engine)
"""
session=Session()

test_variant = session.query(FiledVariants).get(3250)
print(test_variant.Id, test_variant.FiledProductId)
print(test_variant.filedproducts.Id, test_variant.filedproducts.Brand)


print("Relationships:")
from sqlalchemy.inspection import inspect
i = inspect(FiledVariants)
for relation in i.relationships:
    print(relation)
print()

print(test_variant.__dict__)"""




