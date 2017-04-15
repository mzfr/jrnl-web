default: run

.PHONY: run
run:
	@env/bin/python -m app

push: build
	rsync -avz -e ssh build/ dufferzafar@167.88.124.249:/home/dufferzafar/www/jrnl

.PHONY: build
build:
	@mkdir -p build
	@curl -sL http://0.0.0.0:7000/jrnl/idea -o build/idea.html
	@sed -ri 's|/static/bower/bootstrap/dist|https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.0.0-alpha.3|' build/idea.html

back-local:
	@rsync -av /mnt/Work/Documents/Journal/ /home/dufferzafar/dev/alpha/jrnl-web/_Help/journals/

back-remote:
	@rsync -av /mnt/Work/Documents/Journal/ dufferzafar@167.88.124.249:/home/dufferzafar/jrnls
