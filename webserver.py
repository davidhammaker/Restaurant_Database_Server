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
                    output += "<p>" + restaurant.name + "</p>"
                output += "</body></html>"

                self.wfile.write(output.encode())
                print(output)
                return

        except IOError:
            self.send_error(404, "File Not Found: {}".format(self.path))

    def do_POST(self):
        """
        Handles POST requests.
        """
        try:
            length = int(self.headers.get('content-length', 0))
            data = self.rfile.read(length).decode()
            message = parse_qs(data)["message"][0]

            self.send_response(301)
            self.send_header('content-type', 'text/html; charset=utf-8')
            self.end_headers()

            output = ""

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
