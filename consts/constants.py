METHOD_HEAD = 'HEAD'
METHOD_GET = 'GET'
ALLOWED_METHODS = [METHOD_HEAD, METHOD_GET]

STATUS_OK = '200 OK'
STATUS_BAD_RESPONSE = '400 Bad Response'
STATUS_FORBIDDEN = '403 Forbidden'
STATUS_NOTFOUND = '404 NotFound'
STATUS_NOT_ALLOWED = '405 NotAllowed'

CONTENT_TYPE = {
            'html': 'text/html',
            'css': 'text/css',
            'js': 'text/javascript',
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'png': 'image/png',
            'gif': 'image/gif',
            'swf': 'application/x-shockwave-flash'
        }