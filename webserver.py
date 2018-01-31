from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import os
import cgi
#database query
from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
from restaurant import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()
"""Query all of the restaurant name """





class WebServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path.endswith("/restaurant"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            message = "<html><body>%s</body></html>"
            newRestaurant = "<a href = '/restaurant/new'>Make New Restaurant Here</a><br>"
            item= "<li>%s</li>"
            output_item = ""
            output_message=""
            output_body = ""
            results = session.query(Restaurant)
            for result in results:
              output_item += item % result.name
              output_item += "<br>"
              output_item += "<a href = '/restaurant/%s/edit'> Edit </a>" %result.id
              output_item += "<br>"
              output_item += "<a href ='#'> Delete</a>"
            output_body = newRestaurant + output_item
            output_message =message % output_body
            self.wfile.write(output_message)
            print message
            return
        if self.path.endswith("/restaurant/new"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            message = """
            <html>
            <body>
            <form method = 'POST' enctype='multipart/form-data' action = '/restaurant/new'>
            <h2> Add a restaurant </h2>
            <input type="text" name="restaurant">
            <button>Add</button>
            </form>
            </body>
            </html>
            """
            self.wfile.write(message)
            return
        if self.path.endswith("/edit"):
            print self.path
            restaurantIDPath = self.path.split("/")[2]
            myRestaurantQuery = session.query(Restaurant).filter_by(
            id=restaurantIDPath).one()
            print "restaurantIDPath is" + restaurantIDPath
            print myRestaurantQuery
            if myRestaurantQuery:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                message="""
                <html>
                <body>
                <form method = 'POST' enctype='multipart/form-data' action = '/restaurant/%s/edit'> %restaurantIDPath
                <h2> '%s'</h2> % myRestaurantQuery.name
                <input type="text" name="renameRestaurant">
                <button>Rename</button>
                </form>
                </body>
                </html>
                """
            self.wfile.write(message)
            return
    def do_POST(self):
        try:
            if self.path.endswith("/restaurant/new"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('restaurant')

                    # Create new Restaurant Object
                    newRestaurant = Restaurant(name=messagecontent[0])
                    session.add(newRestaurant)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurant')
                    self.end_headers()

        except:
            pass
def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()
