from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker

ENGINE_URL=r"mssql+pymssql://filed_admin:dvserv3#rathena@stage1.ctonnmgtbe2i.eu-west-1.rds.amazonaws.com:1433/Dev3.Filed.ProductCatalogs2"

engine=create_engine(ENGINE_URL, echo=False)

Base=automap_base()
Base.prepare(engine, reflect=True)


FiledVariants=Base.classes.FiledVariants

Session=sessionmaker(bind=engine)

