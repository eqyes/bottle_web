<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Index Page</title>
  </head>
  <body>
  <h1>index page</h1>
  </body>
  %if username == None or username == '':
    <h2>welcome</h2>
  %else:
    <h2>welcome {{username}}</h2>
  %end
</html>