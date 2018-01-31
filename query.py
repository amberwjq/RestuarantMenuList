from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
from restaurant import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()
"""Query all of the restaurant name """
restaurant = session.query(Restaurant).first()
print restaurant.name
items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
output = ''
for i in items:
    output += i.name
    output += '</br>'
print output    
