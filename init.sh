# clone libs
git clone https://github.com/mogui/pyorient pyorient_lib
cd ./pyorient_lib; git co v1.4.5; cd ..
git clone https://github.com/mongodb/mongo-python-driver

# start orientdb
docker run -d -p 2424:2424 -p 2480:2480 --name tt_orient joaodubas/orientdb

# start mongo
docker run -d -p 27020:27017 --name tt_mongo mongo:latest
