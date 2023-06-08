# Detecting tool crack on cnc machine using machine learning.

## How does it work
Train the model weight on google colab and upload the weight to roboflow, as roboflow provide convenience for the users by using their api, from there we can use django Get function to get json code and parse the information and obtain the information we need to display on the website such as the accuracy.

We also implement server side code to get command from the web to halt the machine and sending back machine status to the webserver  

