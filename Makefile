

clean:
	@echo "Cleaning up build, *.pyc files..."
	@find . -name '*.pyc' -exec rm -rf {} \;
	@rm -rf build

kill:
	@echo "Killing mobile-social-share server..."
	@-ps aux | egrep 'mss/start.py' | egrep -v grep | awk '{ print $$2 }' | xargs kill -9
	
start-memcached:
	@echo "Starting memcached..."
	@memcached -d 512
	
stop-memcached:
	@echo "Killing memcached..."
	@-ps aux | egrep 'memcached -d 512' | egrep -v grep | awk '{ print $2 }' | xargs kill -9 2> /dev/null; true

start-be:
	@echo "Starting mobile-social-share server..."
	@cd mss && python start.py --env='LOCAL' > /dev/null 2>&1 &
	
start-local:
	@echo "Starting mobile-social-share server..."
	@cd mss && python start.py --env='LOCAL'

stop-be:
	@echo "Stopping mobile-social-share server..."
	@-ps -ef | egrep 'start.py' | egrep -v egrep | tr -s ' ' | cut -f 3 -d ' ' | xargs sudo kill

start-nginx:
	@echo "Starting nginx..."
	@sudo /opt/nginx/sbin/nginx -c `pwd`/conf/nginx-mobile-social-share.conf

stop-nginx:
	@echo "Stopping nginx..."
	@sudo /opt/nginx/sbin/nginx -c `pwd`/conf/nginx-mobile-social-share.conf -s stop 2> /dev/null; true

start: start-nginx start-be
	@echo "========================="
	@echo "Suite mobile-social-share started!!!"
	@echo "========================="

stop: stop-nginx stop-be
	@echo "========================="
	@echo "Suite mobile-social-share stopped!!!"
	@echo "========================="
	@sleep 2

db: drop_db create_db migrate_db

drop_db:
	@echo -n $(red)
	@echo "Dropping database..."
	@echo -n $(white)
	@mysql -u root -e 'DROP DATABASE IF EXISTS mss;'
	@echo -n $(normal)

create_db:
	@echo "Creating database..."
	@echo -n $(white)
	@mysql -u root -e 'CREATE DATABASE IF NOT EXISTS mss;'
	@echo -n $(green)
	@echo 'Database `mss` created!'
	@echo -n $(normal)
	
migrate_db:
	@echo "Migrating mss"
	@echo -n $(white)
	@db-migrate -c migrations/local.conf
	@echo -n $(green)
	@echo "Database migrated!"
	@echo -n $(green)
	@echo "DONE"
	@echo -n $(normal)
	
unit: clean
	@echo "Running unit tests..."
	@export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/mss  &&  \
		cd mss && \
	    nosetests -s --verbose --with-coverage --cover-package=mss tests/unit/*
	
functional: clean start-memcached
	@echo "Running functional tests..."
	@export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/mss  &&  \
		cd mss && \
	    nosetests -s --verbose --with-coverage --cover-package=mss tests/functional/*
	    
start-beanstalkd:
	@echo "Starting beanstalkd..."
	@beanstalkd -d

stop-beanstalkd:
	@echo "Stopping beanstalkd..."
#   -ps -ef | egrep 'beanstalkd -d' | egrep -v egrep | tr -s ' ' | cut -f 3 -d ' ' | xargs kill
	@killall beanstalkd 2> /dev/null; true
	    
doc:
	cd docs && make html && open build/html/index.html

#epydoc:
#    epydoc --html -o docs/epydoc --name "Mobile Social Share" mss && open docs/epydoc/index.html