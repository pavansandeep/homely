# homely

Need to add following in .bash_profile or .bashrc file of the system.
export DJANGO_SETTINGS_MODULE = 'homely.settings'

1. To create AUTH tables run manage.py syncdb

To create rental app specific migrations
1. Delete existing migrations in rental/migrations
2. run "python manage.py makemigrations"

To apply migrations
1. run "python manage.py migrate"
