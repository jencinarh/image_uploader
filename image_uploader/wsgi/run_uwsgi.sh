
# This should be mounted in the production server with the correct user
# in order to use the correct privileges.
# It can be done installing python and uwsgi system-wide.
# 
# For local environments is harder to maintain because of the user privileges.
# However starting a local server with the correct DNS (in the hosts) and pointing
# to the correct confi files should not be too hard.
# 
# For now the connection between nginx and uwsgi is done by means of a socket. 
# At first glance the architecture does not need another server to serve static files
# because all the hard computation will be done in another server.
# 
# If it's not the case and both the web server and the computation server are the same
# it may need some kind of limitation or to think about different machines
# handling the different applications.
# uwsgi --socket /tmp/mDag_web.socket --wsgi-file ../mDag/mDag/test.py --chmod-socket=777

# NOTE: in order to run this you need to have the virtualenv enabled or, at least, have
#       a full fledged python environment installed

# This does not work with sym links 
export DJANGO_PROJ_PATH=$(dirname $(dirname $(realpath "$0")))
echo $DJANGO_PROJ_PATH
uwsgi --ini uwsgi.ini
