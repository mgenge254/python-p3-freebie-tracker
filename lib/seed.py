#!/usr/bin/env python3

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Base, Company, Dev, Freebie


engine = create_engine("sqlite:///freebies.db")
Base.metadata.create_all(engine) 
Session = sessionmaker(bind=engine)
session = Session()


session.query(Freebie).delete()
session.query(Company).delete()
session.query(Dev).delete()
session.commit()

company1 = Company(name="Rubics", founding_year=2000)

company2 = Company(name="Steelmugs", founding_year=2010)

dev1 = Dev(name="Leo")
dev2 = Dev(name="Eli")

freebie1 = Freebie(item_name="Plate", value=10, company=company1, dev=dev1)
freebie2 = Freebie(item_name="Mug", value=5, company=company2, dev=dev2)


session.add_all([company1, company2, dev1, dev2, freebie1, freebie2])
session.commit()


print("\n- All Companies:")
for company in session.query(Company).all():
    print(f"{company.id}: {company.name}, Founded: {company.founding_year}")


print("\n- All Devs:")
for dev in session.query(Dev).all():
    print(f"{dev.id}: {dev.name}")


print("\n- All Freebies:")
for freebie in session.query(Freebie).all():
    print(f"{freebie.id}: {freebie.item_name} (Value: {freebie.value}), Given by {freebie.company.name} to {freebie.dev.name}")

session.close() 

print("\nDatabase seeded successfully!")
