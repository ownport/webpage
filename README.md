webpage
=======

The collection of tools for making webpage archive

## Install dependencies

```
$ make update-packages
```

## For developers

```
$ make update-dev-packages
```

### Tests

All tests are performing with local server

To run dev server in console
```
$ ./tests/scripts/dev-serv.py --logfile=tests/dev-server.log --datapath=tests/data/
Bottle v0.12.7 server starting up (using WSGIRefServer())...
Listening on http://localhost:8888/
Hit Ctrl-C to quit.
```

To run dev server as daemon
```
$ ./tests/scripts/dev-serv.sh 
 * Usage: dev-serv.sh {start|stop|restart|reload|force-reload|status}
$
```

To run unittests
```
$ make test-all
```

To run unittests with coverage
```
$ make test-all-with-coverage
```
