from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qsl, urlparse


class WebRequestHandler(BaseHTTPRequestHandler):
    def url(self):
        return urlparse(self.path)

    def query_data(self):
        return dict(parse_qsl(self.url().query))
        

    def do_GET(self):
        if self.path == '/' or self.path == '/home.html':
            self.path = '/home.html'
            file = open(self.path[1:])
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(file.read().encode('utf-8'))        

        elif 'autor' in self.query_data():
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(self.get_html_dinamico().encode("utf-8"))
            
        elif self.path in self.contenido:
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(self.contenido[self.path].encode("utf-8"))

        else:
            self.send_error(404, "Error 404")

    def get_response(self):
        return f"""
    <h1> Hola Web </h1>
    <p> URL Parse Result : {self.url()}         </p>
    <p> Path Original: {self.path}         </p>
    <p> Headers: {self.headers}      </p>
    <p> Query: {self.query_data()}   </p>
    """
        
    def get_html_dinamico(self):
        return f"""
        <h1> Proyecto: {self.url().path} Autor: {self.query_data()['autor']}  </h1>
        """
   
    # ---- Diccionario con sitios 

    contenido = {
        '/': """<html>...</html>""",
        
        '/proyecto/1': """
    <html>
      <h1>Proyecto: web-uno</h1>
        <h1>Web estatica - App de recomendacion de libros</h1>
    </html>""",
        
        '/proyecto/2': """
    <html>
        <h1>Proyecto: web-dos</h1>
        <h1>Web app - Peliculas y series por ver</h1>
    </html>""",
        
        '/proyecto/3': """
    <html>
        <h1>Proyecto: web-tres</h1>
        <h1>Web app - Foto22, web ara gestion de fotos</h1>
    </html>""",
    }

if __name__ == "__main__":
    print("Starting server")
    server = HTTPServer(("0.0.0.0", 8000), WebRequestHandler)
    server.serve_forever()
