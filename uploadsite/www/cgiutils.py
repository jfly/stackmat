import os
import string

# Copied from http://code.activestate.com/recipes/52287-handling-urls-within-a-cgi-script/

def isSSL():
    """ Return true if we are on a SSL (https) connection. """
    return os.environ.get('SSL_PROTOCOL', '') != ''


def getScriptname():
    """ Return the scriptname part of the URL ("/path/to/my.cgi"). """
    return os.environ.get('SCRIPT_NAME', '')


def getPathinfo():
    """ Return the remaining part of the URL. """
    pathinfo = os.environ.get('PATH_INFO', '')

    # Fix for bug in IIS/4.0
    if os.name == 'nt':
        scriptname = getScriptname()
        if string.find(pathinfo, scriptname) == 0:
            pathinfo = pathinfo[len(scriptname):]                
    
    return pathinfo


def getQualifiedURL(uri = None):
    """ Return a full URL starting with schema, servername and port.

        *uri* -- append this server-rooted uri (must start with a slash)
    """
    schema, stdport = (('http', '80'), ('https', '443'))[isSSL()]
    host = os.environ.get('HTTP_HOST')
    if not host:
        host = os.environ.get('SERVER_NAME')
        port = os.environ.get('SERVER_PORT', '80')
        if port != stdport: host = host + ":" + port

    result = "%s://%s" % (schema, host)
    if uri: result = result + uri
    
    return result


def getBaseURL():
    """ Return a fully qualified URL to this script. """
    return getQualifiedURL(getScriptname())
