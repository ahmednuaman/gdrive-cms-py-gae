# A Google Drive CMS
## Python GAE Version (2.7)
This is a simple CMS proof-of-concept that uses Google Drive as the CMS part. This means that you don't need to bother with testing different WYSIWYG editors, dealing with authentication, passwords and sessions. The original version written in PHP is here: [https://github.com/ahmednuaman/gdrive-cms-php](https://github.com/ahmednuaman/gdrive-cms-php)

## How can I use it?
1. Clone the app: `git clone git@github.com:ahmednuaman/gdrive-cms-py-gae.git` or [download the zip](https://github.com/ahmednuaman/gdrive-cms-py-gae/archive/master.zip).
2. Create your [Google App Engine](http://appengine.google.com) app.
3. Update the `app.yaml` and set your app's name (first line).
4. Copy `config.py.example` and fill it out.
5. In your Google App Engine app administration area add the email addresses of people you want to admin the site.
6. Test the app locally by running `dev_appserver.py -a '127.0.0.1' .` and visit [http://127.0.0.1:8080/admin/](http://127.0.0.1:8080/admin/) for the admin area and [http://127.0.0.1:8080/](http://127.0.0.1:8080/) for the front end.
7. Once you're happy deploy the app by running `appcfg.py update --oauth .` and sit back and relax

## But I have more questions!
Ok, well go and read the PHP readme, it's a lot more detailed: [https://github.com/ahmednuaman/gdrive-cms-php](https://github.com/ahmednuaman/gdrive-cms-php)
