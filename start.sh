docker run -v `pwd`:/app -it --rm --link tt_mongo --link tt_orient -w=/app ubuntu:14.04 python3 test.py mongo_select
docker run -v `pwd`:/app -it --rm --link tt_mongo --link tt_orient -w=/app ubuntu:14.04 python3 test.py orient_select
