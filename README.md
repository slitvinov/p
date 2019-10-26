192.168.1.11:5000/apidocs
id: Rover05

curl -X GET "http://192.168.1.10:5000/" -H  "accept: application/json"
curl -X GET "http://192.168.1.11:5000/api/Rover05/image" -H  "accept: application/json" > p.jpeg
