curl -i http://localhost:5000/starplus/api/v1.0/storecodes
curl -i http://localhost:5000/starplus/api/v1.0/rdplogin/TEST01/AAA1/2
curl -i http://159.203.41.250:5000/starplus/api/v1.0/storecodes
curl -i http://159.203.41.250:5000/starplus/api/v1.0/rdplogin/TEST01/AAA1/2

#OLD WAYTesting the POST command
curl -i -H "Content-Type application/json" -X POST http://localhost:5000/starplus/api/v1.0/register/TEST01/2/216.123.248.66/192.168.0.12

#Testing the register via a get command
curl -i -H "Content-Type application/json" http://localhost:5000/starplus/api/v1.0/register/TEST01/2/216.123.248.66/192.168.0.12

