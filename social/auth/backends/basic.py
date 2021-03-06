import www.auth

from ...providers.basic import models
from .. import protocols
from . import Backend

class User(models.User):
    class Meta:
        proxy = True

    AVATAR_URL = property(models.User.gravatar)

class Protocol(protocols.Protocol):
    def request(self, request, callback_url):
        #TODO get_redirect_url is not implemented at this moment
        return self.get_redirect_url(callback_url=callback_url)

    def callback(self, request):
        if not 'username' in request.REQUEST:
            raise errors.Error(_("No username provided in request!"))
        if not 'password' in request.REQUEST:
            raise errors.Error(_("No password provided in request!"))
        return {'username': request.REQUEST['username'],
                'password': request.REQUEST['password']}

class Backend(Backend):
    protocol = Protocol()

    def authenticate(self, username, password):
        return User.objects.authenticate(username, password)

