clean:
	@echo "Cleaning up build, *.pyc files..."
	@find . -name '*.pyc' -exec rm -rf {} \;
	@rm -rf build

kill:
	@echo "Killing mobile-social-share server..."
	@-ps aux | egrep 'mss/start.py' | egrep -v grep | awk '{ print $$2 }' | xargs kill -9

start-be:
	@echo "Starting mobile-social-share server..."
	@python mss/start.py

stop-be:
	@echo "Stopping mobile-social-share server..."
	@-ps -ef | egrep 'mss/start.py' | egrep -v egrep | tr -s ' ' | cut -f 3 -d ' ' | xargs sudo kill

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