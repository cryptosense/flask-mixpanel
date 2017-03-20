import uuid

from flask import current_app, request, session
from mixpanel import Mixpanel
from mixpanel_async import AsyncBufferedConsumer

BLACKLISTED_AGENT_STRINGS = (
    'Baiduspider',
    'Bing',
    'Googlebot',
    'UptimeRobot',
)


def get_random_id():
    return str(uuid.uuid4())


def get_instance():
    token = current_app.config.get('MIXPANEL_TOKEN')
    if token is None or 'distinct_id' not in session:
        return
    return Mixpanel(token, consumer=AsyncBufferedConsumer())


def is_blacklisted(blacklisted_strings, user_agent):
    return any(string in user_agent for string in blacklisted_strings)


def get_ip():
    return request.access_route[0]


def alias(alias_id, meta=None):
    mp = get_instance()
    if mp is None:
        return
    return mp.alias(alias_id, session['distinct_id'], meta)


def track(event_name, properties=None, meta=None):
    print("Mixpanel event: {}".format(event_name))
    mp = get_instance()
    if mp is None:
        return
    user_agent = request.headers.get('User-Agent')
    if user_agent and is_blacklisted(BLACKLISTED_AGENT_STRINGS, user_agent):
        return
    if properties is None:
        properties = {}
    app_id = current_app.config.get('MIXPANEL_APP_ID')
    properties.update({
        '$referrer': request.headers.get('Referer'),
        'ip': get_ip(),
        'user_agent': user_agent,
        'app_id': app_id,
    })
    if app_id is not None:
        event_name = '{}: {}'.format(app_id, event_name)

    return mp.track(session['distinct_id'], event_name, properties, meta)


def people_append(properties, meta=None):
    mp = get_instance()
    if mp is None:
        return
    if meta is None:
        meta = {}
    meta['$ip'] = get_ip()
    return mp.people_append(session['distinct_id'], properties, meta)


def people_set(properties, meta=None):
    mp = get_instance()
    if mp is None:
        return
    if meta is None:
        meta = {}
    meta['$ip'] = get_ip()
    return mp.people_set(session['distinct_id'], properties, meta)


def people_set_once(properties, meta=None):
    mp = get_instance()
    if mp is None:
        return
    if meta is None:
        meta = {}
    meta['$ip'] = get_ip()
    return mp.people_set_once(session['distinct_id'], properties, meta)
