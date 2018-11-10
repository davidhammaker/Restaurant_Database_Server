#!/usr/bin/env python3
"""
This module provides a server through which a user may access a restaurant/menu database.
"""
# Import modules and classes for server functionality
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

# Import necessary modules and classes for SQLAlchemy interaction
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem

# Start an SQLAlchemy session
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()


class WebserverHandler(BaseHTTPRequestHandler):
    """
    Handles GET and POST requests.
    """
    def do_GET(self):
        """
        Handles GET requests.

        Specifically handles "/restaurant" path to print restaurant names.
        """
        try:
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()

                all_restaurants = session.query(Restaurant).all()

                output = "<html><body><h3>All Restaurants:</h3>"

                for restaurant in all_restaurants:
                    restaurant_url = str(restaurant.id) + "/" + restaurant.name.replace("'", "").replace(" ", "")
                    output += "<p>" + restaurant.name
                    output += "<br><a href=\"/restaurants/edit/" + restaurant_url + "\">Edit</a>"
                    output += "<br><a href=\"/restaurants/delete/" + restaurant_url + "\">Delete</a>"
                    output += "</p>"
                output += "</body></html>"

                self.wfile.write(output.encode())
                print(output)
                return

            elif "edit" in self.path:
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()

                output = "<html><body>Enter new restaurant name:<br>"

                all_restaurants = session.query(Restaurant).all()
                edit_restaurant = int(str.split(self.path, "/")[-2])
                old_restaurant = ""
                for restaurant in all_restaurants:
                    if restaurant.id == edit_restaurant:
                        old_restaurant = restaurant.name

                output += "<form method=\"POST\">" \
                          "<input name=\"edit_name\" type=\"text\" action=\"d" + self.path + "\" " \
                          "value=\"" + old_restaurant + "\"><input type=\"submit\" value=\"Submit\"></form>"
                output += "</body></html>"

                self.wfile.write(output.encode())


            elif "delete" in self.path:
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()

                self.wfile.write("<html><body>Delete</body></html>".encode())
                print("Delete")

        except IOError:
            self.send_error(404, "File Not Found: {}".format(self.path))

    def do_POST(self):
        """
        Handles POST requests.
        """
        try:
            length = int(self.headers.get('content-length', 0))
            data = self.rfile.read(length).decode()
            edit_name = parse_qs(data)["edit_name"][0]

            self.send_response(200)
            self.send_header('content-type', 'text/html; charset=utf-8')
            self.end_headers()

            all_restaurants = session.query(Restaurant).all()
            edit_restaurant = int(str.split(self.path, "/")[-2])
            restaurant_rename = session.query(Restaurant).filter_by(id=edit_restaurant).one()
            restaurant_rename.name = edit_name
            session.add(restaurant_rename)
            session.commit()

            output = "<html><body>Restaurant Edited: " + edit_name
            output += "<br><a href=\"/restaurants\">Return to Restaurants</a></body></html>"

            self.wfile.write(output.encode())
            print(output)

        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebserverHandler)
        print("Web server running on port {}.".format(port))
        server.serve_forever()

    except KeyboardInterrupt:
        print("\nKeyboard interruption. Stopping web server.")
        server.socket.close()


if __name__ == '__main__':
    main()
