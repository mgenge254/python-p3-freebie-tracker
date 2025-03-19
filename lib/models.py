from sqlalchemy import ForeignKey, Column, Integer, String, MetaData
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)
Base = declarative_base(metadata=metadata)

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    founding_year = Column(Integer, nullable=False)

    freebies = relationship("Freebie", back_populates="company")

    def __repr__(self):
        return f'<Company {self.name} (Founded: {self.founding_year})>'

    @property
    def devs(self):
        return {freebie.dev for freebie in self.freebies}

    def give_freebie(self, dev, item_name, value):
        return Freebie(item_name=item_name, value=value, company=self, dev=dev)

    @classmethod
    def oldest_company(cls, session):
        return session.query(cls).order_by(cls.founding_year.asc()).first()

class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    freebies = relationship("Freebie", back_populates="dev")

    def __repr__(self):
        return f'<Dev {self.name}>'

    @property
    def companies(self):
        return {freebie.company for freebie in self.freebies}

    def received_one(self, item_name):
        return any(freebie.item_name == item_name for freebie in self.freebies)

    def give_away(self, new_dev, freebie):
        if freebie.dev == self:
            freebie.dev = new_dev
            return True
        return False


class Freebie(Base):

    __tablename__ = 'freebies'
    
    id = Column(Integer, primary_key=True)
    item_name = Column(String, nullable=False)
    value = Column(Integer, nullable=False)

    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    dev_id = Column(Integer, ForeignKey('devs.id'), nullable=False)

    company = relationship("Company", back_populates="freebies")
    dev = relationship("Dev", back_populates="freebies")

    def __repr__(self):
        return f'<Freebie {self.item_name} (Value: {self.value})>'


    def print_details(self):

        return f"{self.dev.name} owns a {self.item_name} from {self.company.name}"