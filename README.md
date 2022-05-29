# BotDisco Backend 🕺

# Prerequisites

Make sure you have [`python v3.8`](https://docs.python-guide.org/starting/installation/) and [`pipenv`](https://pipenv.pypa.io/en/latest/install/#installing-pipenv) installed.

# Installation

## Set up your Environment

Duplicate the `.env.template` file and rename it to `.env`

You'll need to fill in all of the environment values in the `.env` file. If someone on your team has already done this, ask them for their file! If this is the first time setting everything up, see below.

### TODO: How to get all env values

Once you've set all of those environment variables, you're ready to install.

## Install python dependencies

Get into the virtual environment.

    pipenv shell

Install all python dependencies.

    pipenv install -r requirements.txt

## Database

Migrate the database

    python manage.py migrate

Start the server

    python manage.py runserver

# Try it out

Check out [http://localhost:8000/api/v1/public](http://localhost:8000/api/v1/public) !

## Postman

[Postman](https://www.postman.com/) is a tool that lets you test out HTTP requests in development quickly. You can test authenticated calls too! Included with this repo is a postman file that you can add to Postman to get up a running quickly.

# Administration

**Note:** You can stop the running django server by pressing ctrl+c in the terminal.

## Create admin user

    python manage.py createsuperuser2 --noinput --username admin --email admin@example.com --password Test123!

**Note:** To start the server again, run: `python manage.py runserver`

## Admin Dashboard

Check out the admin dashboard [http://localhost:8000/admin](http://localhost:8000/admin) !

## Next Steps

1. Try creating an API key in the admin dashboard. Don't give it an expiration date to keep it always valid. As soon as you create an API key, you'll see it at the top of the page. You'll only see it once because it is hashed in the database, so make sure you copy it.. or create another.

2. Get the Postman file from someone. This has all of the Http requests you can try out. You'll need to add the API key to the X-Api-Key header.

# Development Tips

1.  When installing new Python packages, use pipenv like this:

        pipenv install example-package

    This adds the dependency to the Pipfile and only installs the library in your virtual environment.

2.  In VSCode, make sure your Python interpreter is selected to use the pipenv virtualenv. TODO add gif

3.  You can test Django models in a shell with:
    ```
    python .\manage.py shell
    import django
    from thetone_backend.app.models import User
    User.objects.all()
    ```
4.  Seed the Database using Django fixtures. Check out the `fixtures` folder.
    ```
    python manage.py loaddata runtime_groups user_roles fields
    ```

# Logging

Sentry makes logging with Django easy. With Sentry, you can view errors in a dashboard with the stacktrace of the error and the request that triggered the error.

If you already have a Sentry account and know how to create a new Sentry project, then the only thing you need to set is your `SENTRY_DSN_URL` in your `.env` file.

If this is your first time using Sentry...

1. [Create a Sentry account](https://sentry.io/signup/).
2. Select Django from the list of project types.
3. Sentry will give you a block of code to add to your settings file, but this has already been added. See it in `agrawat_backend/settings/dev.py`.
4. On this screen you'll notice that Sentry has a DSN URL. Copy and paste that as the value for `SENTRY_DSN_URL` in your `.env` file.
5. Start your Django server and go to [http://localhost:8000/sentry-debug/](http://localhost:8000/sentry-debug/). This will cause an error to be thrown, which will be logged in Sentry.
6. Take a few minutes to see how the error is logged in Sentry. It's really cool!

# How it works

All of the documentation below is to describe how this project works.

# Docker

## Installing Docker

Follow these steps [here](https://docs.docker.com/install/)

## Docker in Development

_You DON'T have to run Django in Docker to do development locally. You can just run Django locally from the terminal! Docker is only required for deployment in production._ But, here is how to see it running locally.

1. Make sure you have your `.env` file filled in first!
2. Make sure Docker is running locally.

### Start Docker on Linux

    sudo sh exec.sh

### Start Docker on Windows

    .\exec.ps1

If it's running correctly, you should be able to go to: [http://localhost:8000/api/v1/public](http://localhost:8000/api/v1/public)

## Docker in Production

In production, ElasticBeanstalk will see the Dockerfile and run it. The Dockerfile copies in the files, installs the python dependencies, and runs `run-prod.sh`. This script starts up the server with [`gunicorn`]('https://gunicorn.org/').

Gunicorn serves the Django application. It does what `python manage.py runserver` does, but for **production**. A lot of tutorials online use Django's `runserver` command in production, but this is not a good idea! So, what's the difference? Basically, `runserver` is optimized for development. So it's slower, less secure, and will auto update if the files update. Here's more [info]('https://stackoverflow.com/questions/35657332/django-difference-between-using-server-through-manage-py-and-other-servers-like').

# How to Deploy

How to install [ElasticBeanstalk CLI]('https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3-install.html').

I followed these steps to [initialize the EB CLI]('https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3-configuration.html'), but you'll see those commands below.

### Push any changes to source control

    git add .
    git commit -m 'your commit message'
    git push

### Deploy to Elastic Beanstalk

    eb deploy

_NOTE: `eb deploy` will only take the committed git files!_

# How AWS Deployment was Created

## Database connection

Instructions for how the connection to AWS RDS Postgres was made can be found [here](https://medium.com/swlh/creating-a-postgresql-db-on-aws-and-connecting-it-to-heroku-django-app-29603df20c2a)
Included in those instructions is how to connect to RDS using a local pgadmin tool.
TODO: add SSL connection in prod

## S3 Connection

The library used is called [django-storages](https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html). Check out their page for official documentation and what settings you can change. But check out [this tutorial](https://simpleisbetterthancomplex.com/tutorial/2017/08/01/how-to-setup-amazon-s3-in-a-django-project.html) on how to set up your IAM user and S3 bucket.

### Making S3 objects public

If you want all of the objects in S3 to be public, follow these steps:

`AWS_DEFAULT_ACL`='public-read'

`AWS_QUERYSTRING_AUTH` = False # Removes auth from query string

In order to allow this, I had to go to S3 bucket > permissions > Object Ownership > ACLs enabled. This lets the django-storages library set 'public-read' access on the S3 objects. If you don't need public-read, then don't enable.

## Elastic Beanstalk (EB) Setup

**DO NOT** run these commands unless you are creating a new environment + application. If you are just developing locally, don't run these! This will create a new EB deployment.

The below code shows how the prod-app and prod-env were set up. Elastic Beanstalk will create an EC2 instance and launch the Docker container of this project. You can configure the EC2 instance, logging, load balancing, env variables, health checking, alarms, etc. from the EB dashboard.

In the project root folder, create a new EB application named "prod-app":

```
eb init -p docker prod-app --interactive
```

In the interactive menu, you can give your ec2 instances ssh access to debug. This creates an EB environment named "prod-env" on a single t2.small EC2 instance in the us-east-1 region.

```
eb create prod-env -i t2.small -r us-east-1 --max-instances 1
```

This will create the environment and start building. We have to use t2.small because we get an out of memory error with t2.micro. After building you will need to add environment variables to the Configuration. Be sure to add DEPLOYMENT_ENVIRONMENT.

```
eb deploy
```

**IMPORTANT:** **Add your Environment Variables to Configuration > Software**

### HTTPS

Setting up HTTPS was done by following this [ Youtube Video](https://www.youtube.com/watch?v=BeOKTpFsuvk&ab_channel=WornOffKeys). NOTE: You have to use a custom domain in order to set up https. Don't try to set up https with the EB domain name AWS generates for you.. you're going to have a bad time. Just buy a cheap domain name.

### Troubleshooting EB

1. Check the logs in EB > Logs. Download the most recent 100 lines and skim through them.
2. Or, set up SSH to the EC2 instance by running `eb ssh --setup`. You can view the docker container and connect to the docker container like this: `sudo docker exec -it [container_id] /bin/bash`

# Emailing

This template uses [SendGrid]('https://sendgrid.com/') to send emails. If I were to stick with the AWS theme, I should've used AWS SES to send emails. However, I found SES to be very difficult to set up and lacking in deliverability rates. SendGrid, on the other hand, has a simple python API, simple set up, and a user-freindly interface for designing email templates + viewing metrics. Also, it's free to start like SES. You'll notice an Environment variable in `.env` for your SendGrid API key. I put the SendGrid template IDs in a python dictionary in app/constants.py so I can reference the template IDs by name.

# Authentication

Authentication is done with Auth0. Here is the [quick start guide]('https://auth0.com/docs/quickstart/backend/django/01-authorization') for how it was set up. Notice the `# Authentication` section of the `settings/base.py` file.

I also added API keys using [Django Rest Framework API Keys](https://florimondmanca.github.io/djangorestframework-api-key/). Auth0 and API keys can play nicely together.

API keys should be received in the Header in this format:

X-Api-Key: [API_KEY]

I recommend reading through this [entire page]('https://florimondmanca.github.io/djangorestframework-api-key/guide/') for the API library. They do a nice job of explaining how JWT auth and API keys can play together in Django. It's not as bad as you think. Check out `app/permissions.py`. They show how to have an API key belong to an Organization - which is implemented in this template! They also show how to modify settings and create API keys from the admin page. Although, in order to get the admin page to only show the real API key, I did a small modification in the `admin.py` file to unregister the unwanted API Key model.

# Django Architecture guide

Django Architecture was inspired by this [blog post.](https://alexkrupp.typepad.com/sensemaking/2021/06/django-for-startup-founders-a-better-software-architecture-for-saas-startups-and-consumer-apps.html) Not everything the blog posts suggests is used in this template. For example, I don't like how he uses Marshmallow for validation. But the big takeaways are:

- One app for the whole project.
- One `urls.py` file for all url endpoints.
- One views file for each model to receive from urls - named accordingly. Ex. `user_views.py`
- A service file for each model to do the work - named accordingly. Ex. `user_service.py`
- Use functions not classes
- Error handling

# Django Admin Dashboard

Previously in this README, were these instructions:

    python manage.py createsuperuser2 --noinput --username admin --email admin@example.com --password Test123!

Check out the admin page [http://localhost:8000/admin](http://localhost:8000/admin)

This `createsuperuser2` command is defined in `app/management/createsuperuser2.py`. This custom command is needed because if you try to run the standard `createsuperuser` command it will complain about the password field not being recognized.

Superusers can access the Admin page. Be careful who has access to the admin page! You can add Django models to the admin page by registering them under `app/admin.py`.

One weird thing about the admin page is that in production mode (DEBUG=False), Django doesn't serve the css files for the admin page. This template will serve the css files correctly. Here is what is done in the template to make this work:

- In production, this command is ran: `python manage.py collectstatic` (See it in `Dockerfile`!)
- Installed [`whitenoise`]('http://whitenoise.evans.io/en/stable/index.html') - a library that will serve these static files. (See it in `requirements.txt`)
- Set up `whitenoise`.

# Privacy Policy and Terms

Check out [termsfeed.com](termsfeed.com) to generate privacy policy and terms.

# Helpful SQL Query

This command is helpful if you need to delete your postgres database. It removes any connected sessions so you can delete the database.

    SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = 'TARGET_DB' -- ← change this to your DB AND pid <> pg_backend_pid();
