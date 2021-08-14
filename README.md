Steps for installation:-
1) Pull the code
2) cd into the folder which was pulled
3) start a virtual environemnt in it (ensure that u have installed a virtaul environemnt first (if not then :- pip install virtualenv)) for ex by:- virtualenv env
then install django (pip install django)
then install django channels (pip install channels)
then install redis channels (pip install channels_redis)

The environemnt is set up:-

Also ensure that you are using the right python interpreter , that is the virtual environment one.
in vs code it can be checked in the bottom left corner, there will be something like python 3.x.x ensure that it has something at the end like (env) if not click on it and it will present a list of options and change it to one with something like (env) at teh end.

then u can run the server like python/py (whichever is your environemnt path) manage.py runserver

then open the localhost with port 8000