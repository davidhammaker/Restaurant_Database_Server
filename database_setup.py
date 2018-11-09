# Configuration Part 1:
# Provide functions for manipulating runtime environment:
import sys

# Help with writing mapper code:
from sqlalchemy import Column, ForeignKey, Integer, String

# Use in configuration code and class code:
from sqlalchemy.ext.declarative import declarative_base

# Create foreign key relationships, for use in creating mapper:
from sqlalchemy.orm import relationship

# Use in config. code at the end of the file:
from sqlalchemy import create_engine


# Create an instance of 'declarative_base' class, which lets SQLAlchemy know
# that our classes are special SQLAlchemy classes that correspond to tables
# in our database:
Base = declarative_base()


# Class (Restaurant):
class Restaurant(Base):

    # Table:
    __tablename__ = 'restaurant'

    # Mapper:
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)


# Class (MenuItem):
class MenuItem(Base):

    # Table:
    __tablename__ = 'menu_item'

    # Mapper:
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    course = (Column(String(250)))
    description = Column(String(250))
    price = Column(String(8))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)


# Configuration Part 2:
# Create an instance of 'create_engine' and point it to the database we want
# to use:
engine = create_engine('sqlite:///restaurantmenu.db')

# This goes into the database and adds the classes (that we will create) as
# new tables in our database:
Base.metadata.create_all(engine)