#!/usr/bin/python2.5
# Copyright 2010 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

__author__ = 'kpy@google.com (Ka-Ping Yee) and many other Googlers'

import calendar
import cgi
import const
from datetime import datetime, timedelta
import httplib
import legacy_redirect
import logging
import model
import os
import pfif
import random
import re
import sys
import time
import traceback
import unicodedata
import urllib
import urlparse

from google.appengine.dist import use_library
use_library('django', '1.2')

import django.utils.html
from google.appengine.api import images
from google.appengine.api import mail
from google.appengine.api import memcache
from google.appengine.api import taskqueue
from google.appengine.api import users
from google.appengine.ext import webapp
import google.appengine.ext.webapp.template
import google.appengine.ext.webapp.util
from recaptcha.client import captcha

import config
import user_agents

from i18n_setup import ugettext as _

if os.environ.get('SERVER_SOFTWARE', '').startswith('Development'):
    # See http://code.google.com/p/googleappengine/issues/detail?id=985
    import urllib
    urllib.getproxies_macosx_sysconf = lambda: {}

ROOT = os.path.abspath(os.path.dirname(__file__))

# The domain name from which to send e-mail.
EMAIL_DOMAIN = 'appspotmail.com'  # All apps on appspot.com use this for mail.


# ==== Field value text ========================================================

def get_person_sex_text(person):
    """Returns the UI text for a person's sex field."""
    return const.PERSON_SEX_TEXT.get(person.sex or '')

def get_note_status_text(note):
    """Returns the UI text for a note's status field."""
    return const.NOTE_STATUS_TEXT.get(note.status or '')

def get_person_status_text(person):
    """Returns the UI text for a person's latest_status."""
    return const.PERSON_STATUS_TEXT.get(person.latest_status or '')

# Things that occur as prefixes of global paths (i.e. no repository name).
GLOBAL_PATH_RE = re.compile(r'^/(global|personfinder)(/?|/.*)$')


# ==== String formatting =======================================================

def format_utc_datetime(dt):
    if dt is None:
        return ''
    integer_dt = datetime(
        dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
    return integer_dt.isoformat() + 'Z'

def format_sitemaps_datetime(dt):
    integer_dt = datetime(
        dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
    return integer_dt.isoformat() + '+00:00'

def encode(string, encoding='utf-8'):
    """If unicode, encode to encoding; if 8-bit string, leave unchanged."""
    if isinstance(string, unicode):
        string = string.encode(encoding)
    return string

def urlencode(params, encoding='utf-8'):
    """Encode the key-value pairs in 'params' into a query string, applying
    the specified encoding to any Unicode strings and ignoring any keys that
    have value == None.  (urllib.urlencode doesn't support Unicode)."""
    keys = params.keys()
    keys.sort()  # Sort the keys to get canonical ordering
    return urllib.urlencode([
        (encode(key, encoding), encode(params[key], encoding))
        for key in keys if isinstance(params[key], basestring)])

def set_param(params, param, value):
    """Take the params from a urlparse and override one of the values."""
    # This will strip out None-valued params and collapse repeated params.
    params = dict(cgi.parse_qsl(params))
    if value is None:
        if param in params:
            del(params[param])
    else:
        params[param] = value
    return urlencode(params)


def set_url_param(url, param, value):
    """This modifies a URL setting the given param to the specified value.  This
    may add the param or override an existing value, or, if the value is None,
    it will remove the param.  Note that value must be a basestring and can't be
    an int, for example."""
    url_parts = list(urlparse.urlparse(url))
    url_parts[4] = set_param(url_parts[4], param, value)
    return urlparse.urlunparse(url_parts)

def anchor_start(href):
    """Returns the HREF escaped and embedded in an anchor tag."""
    return '<a href="%s">' % django.utils.html.escape(href)

def anchor(href, body):
    """Returns a string anchor HTML element with the given href and body."""
    return anchor_start(href) + django.utils.html.escape(body) + '</a>'

# ==== Validators ==============================================================

# These validator functions are used to check and parse query parameters.
# When a query parameter is missing or invalid, the validator returns a
# default value.  For parameter types with a false value, the default is the
# false value.  For types with no false value, the default is None.

def strip(string):
    # Trailing nulls appear in some strange character encodings like Shift-JIS.
    return string.strip().rstrip('\0')

def validate_yes(string):
    return (strip(string).lower() == 'yes') and 'yes' or ''

def validate_checkbox(string):
    return (strip(string).lower() == 'on') and 'yes' or ''

def validate_role(string):
    return (strip(string).lower() == 'provide') and 'provide' or 'seek'

def validate_int(string):
    return string and int(strip(string))

def validate_sex(string):
    """Validates the 'sex' parameter, returning a canonical value or ''."""
    if string:
        string = strip(string).lower()
    return string in pfif.PERSON_SEX_VALUES and string or ''

def validate_expiry(value):
    """Validates that the 'expiry_option' parameter is a positive integer.

    Returns:
      the int() value if it's present and parses, or the default_expiry_days
      for the repository, if it's set, otherwise -1 which represents the
      'unspecified' status.
    """
    try:
        value = int(value)
    except Exception, e:
        logging.debug('validate_expiry exception: %s', e)
        return None
    return value > 0 and value or None

APPROXIMATE_DATE_RE = re.compile(r'^\d{4}(-\d\d)?(-\d\d)?$')

def validate_approximate_date(string):
    if string:
        string = strip(string)
        if APPROXIMATE_DATE_RE.match(string):
            return string
    return ''

AGE_RE = re.compile(r'^\d+(-\d+)?$')
# Hyphen with possibly surrounding whitespaces.
HYPHEN_RE = re.compile(
    ur'\s*[-\u2010-\u2015\u2212\u301c\u30fc\ufe58\ufe63\uff0d]\s*',
    re.UNICODE)

def validate_age(string):
    """Validates the 'age' parameter, returning a canonical value or ''."""
    if string:
        string = strip(string)
        string = unicodedata.normalize('NFKC', unicode(string))
        string = HYPHEN_RE.sub('-', string)
        if AGE_RE.match(string):
            return string
    return ''

def validate_status(string):
    """Validates an incoming status parameter, returning one of the canonical
    status strings or ''.  Note that '' is always used as the Python value
    to represent the 'unspecified' status."""
    if string:
        string = strip(string).lower()
    return string in pfif.NOTE_STATUS_VALUES and string or ''

DATETIME_RE = re.compile(r'^(\d\d\d\d)-(\d\d)-(\d\d)T(\d\d):(\d\d):(\d\d)Z$')

def validate_datetime(string):
    if not string:
        return None  # A missing value is okay.
    match = DATETIME_RE.match(string)
    if match:
        return datetime(*map(int, match.groups()))
    raise ValueError('Bad datetime: %r' % string)

def validate_timestamp(string):
    try:
        return string and datetime.utcfromtimestamp(float(strip(string)))
    except:
        raise ValueError('Bad timestamp: %s' % string)

def validate_image(bytestring):
    try:
        image = ''
        if bytestring:
            image = images.Image(bytestring)
            image.width
        return image
    except:
        return False

def validate_version(string):
    """Version, if present, should be in pfif versions."""
    if string and strip(string) not in pfif.PFIF_VERSIONS:
        raise ValueError('Bad pfif version: %s' % string)
    return pfif.PFIF_VERSIONS[strip(string) or pfif.PFIF_DEFAULT_VERSION]

REPO_RE = re.compile('^[a-z0-9-]+$')
def validate_repo(string):
    string = (string or '').strip()
    if not string:
        return None
    if string == 'global':
        raise ValueError('"global" is an illegal repository name.')
    if REPO_RE.match(string):
        return string
    raise ValueError('Repository names can only contain '
                     'lowercase letters, digits, and hyphens.')

# ==== Other utilities =========================================================

def url_is_safe(url):
    current_scheme, _, _, _, _ = urlparse.urlsplit(url)
    return current_scheme in ['http', 'https']

def get_app_name():
    """Canonical name of the app, without HR s~ nonsense.  This only works in
    the context of the appserver (eg remote_api can't use it)."""
    from google.appengine.api import app_identity
    return app_identity.get_application_id()

def sanitize_urls(person):
    """Clean up URLs to protect against XSS."""
    if person.photo_url:
        if not url_is_safe(person.photo_url):
            person.photo_url = None
    if person.source_url:
        if not url_is_safe(person.source_url):
            person.source_url = None

def get_host(host=None):
    host = host or os.environ['HTTP_HOST']
    """Return the host name, without version specific details."""
    parts = host.split('.')
    if len(parts) > 3:
        return '.'.join(parts[-3:])
    else:
        return host

def optionally_filter_sensitive_fields(records, auth=None):
    """Removes sensitive fields from a list of dictionaries, unless the client
    has full read authorization."""
    if not (auth and auth.full_read_permission):
        filter_sensitive_fields(records)

def filter_sensitive_fields(records):
    """Removes sensitive fields from a list of dictionaries."""
    for record in records:
        if 'date_of_birth' in record:
            record['date_of_birth'] = ''
        if 'author_email' in record:
            record['author_email'] = ''
        if 'author_phone' in record:
            record['author_phone'] = ''
        if 'email_of_found_person' in record:
            record['email_of_found_person'] = ''
        if 'phone_of_found_person' in record:
            record['phone_of_found_person'] = ''

def get_secret(name):
    """Gets a secret from the datastore by name, or returns None if missing."""
    secret = model.Secret.get_by_key_name(name)
    if secret:
        return secret.secret

# a datetime.datetime object representing debug time.
_utcnow_for_test = None

def set_utcnow_for_test(now):
    """Set current time for debug purposes."""
    global _utcnow_for_test
    _utcnow_for_test = now

def get_utcnow():
    """Return current time in utc, or debug value if set."""
    global _utcnow_for_test
    return _utcnow_for_test or datetime.utcnow()

def get_utcnow_seconds():
    """Return current time in seconds in utc, or debug value if set."""
    now = get_utcnow()
    return calendar.timegm(now.utctimetuple()) + now.microsecond * 1e-6

def log_api_action(handler, action, num_person_records=0, num_note_records=0,
                   people_skipped=0, notes_skipped=0):
    """Log an api action."""
    log = handler.config and handler.config.api_action_logging
    if log:
        model.ApiActionLog.record_action(
            handler.repo, handler.params.key,
            handler.params.version.version, action,
            num_person_records, num_note_records,
            people_skipped, notes_skipped,
            handler.request.headers.get('User-Agent'),
            handler.request.remote_addr, handler.request.url)

def get_full_name(first_name, last_name, config):
    """Return full name string obtained by concatenating first_name and
    last_name in the order specified by config.family_name_first, or just
    first_name if config.use_family_name is False."""
    if config.use_family_name:
        separator = (first_name and last_name) and u' ' or u''
        if config.family_name_first:
            return separator.join([last_name, first_name])
        else:
            return separator.join([first_name, last_name])
    else:
        return first_name

def get_person_full_name(person, config):
    """Return person's full name.  "person" can be any object with "first_name"
    and "last_name" attributes."""
    return get_full_name(person.first_name, person.last_name, config)

def send_confirmation_email_to_record_author(handler, person,
                                             action, embed_url, record_id):
    """Send the author an email to confirm enabling/disabling notes
    of a record."""
    if not person.author_email:
        return handler.error(
            400,
            _('No author email for record %(id)s.') % {'id' : record_id})

    # i18n: Subject line of an e-mail message confirming the author
    # wants to disable notes for this record
    subject = _(
        '[Person Finder] Please confirm %(action)s status updates for record '
        '"%(first_name)s %(last_name)s"'
        ) % {'action': action, 'first_name': person.first_name,
             'last_name': person.last_name}

    # send e-mail to record author confirming the lock of this record.
    template_name = '%s_notes_email.txt' % action
    handler.send_mail(
        subject=subject,
        to=person.author_email,
        body=handler.render_to_string(
            template_name,
            author_name=person.author_name,
            first_name=person.first_name,
            last_name=person.last_name,
            site_url=handler.get_url('/'),
            embed_url=embed_url
        )
    )

def get_repo_url(request, repo, scheme=None):
    """Constructs the absolute root URL for a given repository."""
    req_scheme, req_netloc, req_path, _, _ = urlparse.urlsplit(request.url)
    prefix = req_path.startswith('/personfinder') and '/personfinder' or ''
    if req_netloc.split(':')[0] == 'localhost':
        scheme = 'http'  # HTTPS is not available when using dev_appserver
    return (scheme or req_scheme) + '://' + req_netloc + prefix + '/' + repo

def get_url(request, repo, action, charset='utf-8', scheme=None, **params):
    """Constructs the absolute URL for a given action and query parameters,
    preserving the current repo and the 'small' and 'style' parameters."""
    repo_url = get_repo_url(request, repo, scheme) + '/' + action.lstrip('/')
    params['small'] = params.get('small', request.get('small', None))
    params['style'] = params.get('style', request.get('style', None))
    query = urlencode(params, charset)
    return repo_url + (query and '?' + query or '')


# ==== Base Handler ============================================================

class Struct:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

global_cache = {}
global_cache_insert_time = {}


class BaseHandler(webapp.RequestHandler):
    # Handlers that don't need a repository name can set this to False.
    repo_required = True

    # Handlers that don't use a repository can set this to True.
    ignore_repo = False

    # Handlers that require HTTPS can set this to True.
    https_required = False

    # Set this to True to enable a handler even for deactivated repositories.
    ignore_deactivation = False

    auto_params = {
        'lang': strip,
        'query': strip,
        'first_name': strip,
        'last_name': strip,
        'alternate_first_names': strip,
        'alternate_last_names': strip,
        'sex': validate_sex,
        'date_of_birth': validate_approximate_date,
        'age': validate_age,
        'home_street': strip,
        'home_neighborhood': strip,
        'home_city': strip,
        'home_state': strip,
        'home_postal_code': strip,
        'home_country': strip,
        'author_name': strip,
        'author_phone': strip,
        'author_email': strip,
        'source_url': strip,
        'source_date': strip,
        'source_name': strip,
        'description': strip,
        'expiry_option': validate_expiry,
        'dupe_notes': validate_yes,
        'id': strip,
        'text': strip,
        'status': validate_status,
        'last_known_location': strip,
        'found': validate_yes,
        'email_of_found_person': strip,
        'phone_of_found_person': strip,
        'error': strip,
        'role': validate_role,
        'clone': validate_yes,
        'small': validate_yes,
        'style': strip,
        'add_note': validate_yes,
        'photo_url': strip,
        'photo': validate_image,
        'max_results': validate_int,
        'skip': validate_int,
        'min_entry_date': validate_datetime,
        'person_record_id': strip,
        'omit_notes': validate_yes,
        'id1': strip,
        'id2': strip,
        'id3': strip,
        'version': validate_version,
        'content_id': strip,
        'target': strip,
        'signature': strip,
        'flush_cache': validate_yes,
        'operation': strip,
        'confirm': validate_yes,
        'key': strip,
        'new_repo': validate_repo,
        'utcnow': validate_timestamp,
        'subscribe_email': strip,
        'subscribe': validate_checkbox,
        'suppress_redirect': validate_yes,
        'cursor': strip,
        'flush_config_cache': strip
    }

    def maybe_redirect_jp_tier2_mobile(self):
        """Returns a redirection URL based on the jp_tier2_mobile_redirect_url
        setting if the request is from a Japanese Tier-2 phone."""
        if (self.config and
            self.config.jp_tier2_mobile_redirect_url and
            not self.params.suppress_redirect and
            not self.params.small and
            user_agents.is_jp_tier2_mobile_phone(self.request)):
            # split off the path from the repo name.  Note that path
            # has a leading /, so we want to remove just the first component
            # and leave at least a '/' at the beginning.
            path = re.sub('^/[^/]*', '', self.request.path) or '/'
            # Except for top page, we propagate path and query params.
            redirect_url = (self.config.jp_tier2_mobile_redirect_url + path)
            query_params = []
            if path != '/':
                if self.repo:
                    query_params = ['subdomain=' + self.repo]
                if self.request.query_string:
                    query_params.append(self.request.query_string)
            return redirect_url + '?' + '&'.join(query_params)
        return ''

    def redirect(self, path, repo=None, **params):
        # This will prepend the repo to the path to create a working URL,
        # unless the path has a global prefix or is an absolute URL.
        if re.match('^[a-z]+:', path) or GLOBAL_PATH_RE.match(path):
            if params:
              path += '?' + urlencode(params, self.charset)
        else:
            path = self.get_url(path, repo, **params)
        return webapp.RequestHandler.redirect(self, path)

    def cache_key_for_request(self):
        # Use the whole URL as the key, ensuring that lang is included.
        # We must use the computed lang (self.env.lang), not the query
        # parameter (self.params.lang).
        url = set_url_param(self.request.url, 'lang', self.env.lang)

        # Include the charset in the key, since the <meta> tag can differ.
        return set_url_param(url, 'charsets', self.charset)

    def render_from_cache(self, cache_time, key=None):
        """Render from cache if appropriate. Returns true if done."""
        if not cache_time:
            return False

        now = time.time()
        key = self.cache_key_for_request()
        if cache_time > (now - global_cache_insert_time.get(key, 0)):
            self.write(global_cache[key])
            logging.debug('Rendering cached response.')
            return True
        logging.debug('Render cache missing/stale, re-rendering.')
        return False

    def render(self, name, cache_time=0, **values):
        """Renders the template, optionally caching locally.

        The optional cache is local instead of memcache--this is faster but
        will be recomputed for every running instance.  It also consumes local
        memory, but that's not a likely issue for likely amounts of cached data.

        Args:
            name: name of the file in the template directory.
            cache_time: optional time in seconds to cache the response locally.
        """
        if self.render_from_cache(cache_time):
            return
        values['env'] = self.env  # pass along application-wide context
        values['params'] = self.params  # pass along the query parameters
        values['config'] = self.config  # pass along the configuration
        # TODO(kpy): Remove "templates/" from all template names in calls
        # to this method, and have this method call render_to_string instead.
        response = webapp.template.render(os.path.join(ROOT, name), values)
        self.write(response)
        if cache_time:
            now = time.time()
            key = self.cache_key_for_request()
            global_cache[key] = response
            global_cache_insert_time[key] = now

    def render_to_string(self, name, **values):
        """Renders the specified template to a string."""
        return webapp.template.render(
            os.path.join(ROOT, 'templates', name), values)

    def error(self, code, message=''):
        self.info(code, message, style='error')

    def info(self, code, message='', message_html='', style='info'):
        is_error = 400 <= code < 600
        if is_error:
            webapp.RequestHandler.error(self, code)
        else:
            self.response.set_status(code)
        if not message and not message_html:
            message = '%d: %s' % (code, httplib.responses.get(code))
        try:
            self.render('templates/message.html', cls=style,
                        message=message, message_html=message_html)
        except:
            self.response.out.write(message)
        self.terminate_response()

    def terminate_response(self):
        """Prevents any further output from being written."""
        self.response.out.write = lambda *args: None
        self.get = lambda *args: None
        self.post = lambda *args: None

    def write(self, text):
        """Sends text to the client using the charset from select_charset()."""
        self.response.out.write(text.encode(self.env.charset, 'replace'))

    def get_url(self, action, repo=None, scheme=None, **params):
        """Constructs the absolute URL for a given action and query parameters,
        preserving the current repo and the 'small' and 'style' parameters."""
        return get_url(self.request, repo or self.env.repo, action,
                       charset=self.env.charset, scheme=scheme, **params)

    @staticmethod
    def add_task_for_repo(repo, name, action, **kwargs):
        """Queues up a task for an individual repository."""
        task_name = '%s-%s-%s' % (repo, name, int(time.time()*1000))
        path = '/%s/%s' % (repo, action)
        taskqueue.add(name=task_name, method='GET', url=path, params=kwargs)

    def send_mail(self, to, subject, body):
        """Sends e-mail using a sender address that's allowed for this app."""
        app_id = get_app_name()
        sender = 'Do not reply <do-not-reply@%s.%s>' % (app_id, EMAIL_DOMAIN)
        logging.info('Add mail task: recipient %r, subject %r' % (to, subject))
        taskqueue.add(queue_name='send-mail', url='/global/admin/send_mail',
                      params={'sender': sender,
                              'to': to,
                              'subject': subject,
                              'body': body})

    def get_captcha_html(self, error_code=None, use_ssl=False):
        """Generates the necessary HTML to display a CAPTCHA validation box."""

        # We use the 'custom_translations' parameter for UI messages, whereas
        # the 'lang' parameter controls the language of the challenge itself.
        # reCAPTCHA falls back to 'en' if this parameter isn't recognized.
        lang = self.env.lang.split('-')[0]

        return captcha.get_display_html(
            public_key=config.get('captcha_public_key'),
            use_ssl=use_ssl, error=error_code, lang=lang,
            custom_translations={
                # reCAPTCHA doesn't support all languages, so we treat its
                # messages as part of this app's usual translation workflow
                'instructions_visual': _('Type the two words:'),
                'instructions_audio': _('Type what you hear:'),
                'play_again': _('Play the sound again'),
                'cant_hear_this': _('Download the sound as MP3'),
                'visual_challenge': _('Get a visual challenge'),
                'audio_challenge': _('Get an audio challenge'),
                'refresh_btn': _('Get a new challenge'),
                'help_btn': _('Help'),
                'incorrect_try_again': _('Incorrect.  Try again.')
            }
        )

    def get_captcha_response(self):
        """Returns an object containing the CAPTCHA response information for the
        given request's CAPTCHA field information."""
        challenge = self.request.get('recaptcha_challenge_field')
        response = self.request.get('recaptcha_response_field')
        remote_ip = os.environ['REMOTE_ADDR']
        return captcha.submit(
            challenge, response, config.get('captcha_private_key'), remote_ip)

    def handle_exception(self, exception, debug_mode):
        logging.error(traceback.format_exc())
        self.error(500, _(
            'There was an error processing your request.  Sorry for the '
            'inconvenience.  Our administrators will investigate the source '
            'of the problem, but please check that the format of your '
            'request is correct.'))

    def to_local_time(self, date):
        """Converts a datetime object to the local time configured for the
        current repository.  For convenience, returns None if date is None."""
        # TODO(kpy): This only works for repositories that have a single fixed
        # time zone offset and never use Daylight Saving Time.
        if date:
            if self.config.time_zone_offset:
                return date + timedelta(0, 3600*self.config.time_zone_offset)
            return date

    def get_repo_menu_html(self):
        result = '''
<style>body { font-family: arial; font-size: 13px; }</style>
'''
        for option in self.env.repo_options:
            url = self.get_url('', repo=option.repo)
            result += '<a href="%s">%s</a><br>' % (url, option.title)
        return result

    def initialize(self, request, response, env):
        webapp.RequestHandler.initialize(self, request, response)
        self.params = Struct()
        self.env = env
        self.repo = env.repo
        self.config = env.config
        self.charset = env.charset

        # Log AppEngine-specific request headers.
        for name in self.request.headers.keys():
            if name.lower().startswith('x-appengine'):
                logging.debug('%s: %s' % (name, self.request.headers[name]))

        # Validate query parameters.
        for name, validator in self.auto_params.items():
            try:
                value = self.request.get(name, '')
                setattr(self.params, name, validator(value))
            except Exception, e:
                setattr(self.params, name, validator(None))
                return self.error(400, 'Invalid parameter %s: %s' % (name, e))

        if self.params.flush_cache:
            # Useful for debugging and testing.
            memcache.flush_all()
            global_cache.clear()
            global_cache_insert_time.clear()

        flush_what = self.params.flush_config_cache
        if flush_what == "all":
            logging.info('Flushing complete config_cache')
            config.cache.flush()
        elif flush_what != "nothing":
            config.cache.delete(flush_what)

        # Log the User-Agent header.
        sample_rate = float(
            self.config and self.config.user_agent_sample_rate or 0)
        if random.random() < sample_rate:
            model.UserAgentLog(
                repo=self.repo, sample_rate=sample_rate,
                user_agent=self.request.headers.get('User-Agent'), lang=lang,
                accept_charset=self.request.headers.get('Accept-Charset', ''),
                ip_address=self.request.remote_addr).put()

        # Check for SSL (unless running on localhost for development).
        if self.https_required and self.env.domain != 'localhost':
            if scheme != 'https':
                return self.error(403, 'HTTPS is required.')

        # Check for an authorization key.
        self.auth = None
        if self.params.key:
            if self.repo:
                # check for domain specific one.
                self.auth = model.Authorization.get(self.repo, self.params.key)
            if not self.auth:
                # perhaps this is a global key ('*' for consistency with config).
                self.auth = model.Authorization.get('*', self.params.key)

        # Handlers that don't need a repository configuration can skip it.
        if not self.repo:
            if self.repo_required:
                return self.error(400, 'No repository specified.')
            return
        # Everything after this requires a repo.

        # Reject requests for repositories that don't exist.
        if not model.Repo.get_by_key_name(self.repo):
            if legacy_redirect.do_redirect(self):
                return legacy_redirect.redirect(self)
            else:
                message_html = "No such domain <p>" + self.get_repo_menu_html()
                return self.info(404, message_html=message_html, style='error')

        # If this repository has been deactivated, terminate with a message.
        if self.config.deactivated and not self.ignore_deactivation:
            self.env.language_menu = []
            self.render('templates/message.html', cls='deactivation',
                        message_html=self.config.deactivation_message_html)
            self.terminate_response()

    def is_test_mode(self):
        """Returns True if the request is in test mode. Request is considered
        to be in test mode if the remote IP address is the localhost and if
        the 'test_mode' HTTP parameter exists and is set to 'yes'."""
        post_is_test_mode = validate_yes(self.request.get('test_mode', ''))
        client_is_localhost = os.environ['REMOTE_ADDR'] == '127.0.0.1'
        return post_is_test_mode and client_is_localhost
