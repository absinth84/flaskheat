# flaskheat


#Run Debug mode
env FLASK_APP=server.py flask run --debugger --reload
sudo docker run --name redis-flaskheat -v redis:/data -d -p 127.0.0.1:6379:6379 --rm redis