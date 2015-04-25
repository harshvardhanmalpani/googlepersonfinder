<font color='red' size='4'>The code repository and all the wiki articles have been migrated to GitHub (<a href='https://github.com/google/personfinder/wiki/DeploymentGuide'>direct link</a>).</font>


# How to set up your own instance of Person Finder #

## Introduction ##

Google's instance of Person Finder runs at http://google.org/personfinder, but you can also use the source code to set up your own completely independent instance.  In order to deploy Person Finder at a new URL for the first time, you need to create a new App Engine app, push the code to it, and then carry out a few configuration steps.

## Details ##

In order to deploy on appspot.com you'll need an application id.  You can create one at https://appengine.google.com/.  On the application create page (https://appengine.google.com/start/createapp) you can pick the application identifier (appid) and set some other options.  In particular we recommend picking "High Replication" under storage options.

Check out the source code, and then change the application field in app.yaml to your new application ID.

Once that's configured, you can upload the code for the new application.  From the root directory you can use the gae tool to perform an upload:
```
tools/gae update app
```

You can access your new release at: http://application-id.appspot.com

Once the application is up and running, you should use the console application to set some basic configuration values.

```
./tools/console application-id.appspot.com
```

From the console you'll need to create the first repo:
```
 Repo(key_name='test').put() 
```

Once thats done, new repos can be created from the admin page at http://test.application-id.appspot.com/admin

From the console set the following:
```
Secret((key_name=u'analytics_id', value=u'<analytics id>').put()  
```

_See https://www.google.com/analytics/ for how to use Google Analytics and to get an an analytics ID.  This will let you measure the usage of your app._

```
config.set(captcha_private_key=u'private key')
config.set(captcha_public_key=u'public key' 
```

_See https://www.google.com/recaptcha/admin/list to get ReCAPTCHA keys. This is necessary for the CAPTCHA tests that users have to complete in order to do certain actions like deleting or subscribing to records._

```
config.set(language_api_key=u'<google api key>')
```

_See http://code.google.com/apis/loader/signup.html for directions on getting an API key. This is used to enable the use of Google Translate to translate notes._