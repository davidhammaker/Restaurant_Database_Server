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

                output += "<h3><a href=\"/restaurants/create\">Create New Restaurant</a></h3>"

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

                output = "<html><body>Are you sure?"
                output += "<br><form method=\"POST\">" \
                          "<input name=\"delete\" type=\"radio\" value=\"No\" checked>No<br>" \
                          "<input name=\"delete\" type=\"radio\" value=\"Yes\">Yes<br>" \
                          "<input type=\"submit\" value=\"Submit\">" \
                          "</form></body></html>"

                self.wfile.write(output.encode())
                print("Delete")

            elif "create" in self.path:
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()

                output = "<html><body>Enter the name of your new restaurant:<br>" \
                         "<form method=\"POST\">" \
                         "<input name=\"create\" type=\"text\"><input type=\"submit\" value=\"Submit\">" \
                         "</form></body></html>"

                self.wfile.write(output.encode())

        except IOError:
            self.send_error(404, "File Not Found: {}".format(self.path))

    def do_POST(self):
        """
        Handles POST requests.
        """
        try:
            length = int(self.headers.get('content-length', 0))
            data = self.rfile.read(length).decode()
            print(parse_qs(data))

            post_goal = ""
            for key in parse_qs(data):
                post_goal = key
                print(post_goal)

            if post_goal == "edit_name":
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

            elif post_goal == "delete":
                delete_answer = parse_qs(data)["delete"][0]
                print(delete_answer)

                self.send_response(200)
                self.send_header('content-type', 'text/html; charset=utf-8')
                self.end_headers()

                output = ""
                if delete_answer == "Yes":
                    all_restaurants = session.query(Restaurant).all()
                    delete_restaurant_id = int(str.split(self.path, "/")[-2])
                    delete_restaurant = session.query(Restaurant).filter_by(id=delete_restaurant_id).one()

                    print("id: {}".format(delete_restaurant_id))
                    print("restaurant: {}".format(delete_restaurant.name))

                    session.delete(delete_restaurant)
                    session.commit()

                    output = "<html><body>\"{}\" has been deleted.".format(delete_restaurant.name)

                elif delete_answer == "No":
                    output = "<html><body>The restaurant has NOT been deleted."

                output += "<br><a href=\"/restaurants\">Return to restaurants</a></body></html>"

                self.wfile.write(output.encode())

            elif post_goal == "create":
                new_restaurant_name = parse_qs(data)["create"][0]
                print(new_restaurant_name)

                self.send_response(200)
                self.send_header('content-type', 'text/html; charset=utf-8')
                self.end_headers()

                new_restaurant = Restaurant(name = new_restaurant_name)
                session.add(new_restaurant)
                session.commit()

                output = "<html><body>" + new_restaurant_name + " has been created."
                output += "<br><a href=\"/restaurants\">Return to restaurants</a></body></html>"

                self.wfile.write(output.encode())

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
