from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker


engine=create_engine(
    r"mssql+pymssql://filed_admin:dvserv3#rathena@stage1.ctonnmgtbe2i.eu-west-1.rds.amazonaws.com:1433/Dev3.Filed.ProductCatalogs2",
    echo=True
)

Base=automap_base()
Base.prepare(engine, reflect=True)

FiledVariants=Base.classes.FiledVariants
FiledProducts=Base.classes.FiledProducts

Session=sessionmaker(bind=engine)




