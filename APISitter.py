import datetime


class APISitter(object):
    ''' Class for maintaining an expiring API key '''

    def __init__(self, timeout, fn, *args):
        '''
        timeout (int): time in seconds that API key stays valid
        fn (function): function used to get API key from server
        *args: args passed to fn when called
        '''

        if not callable(fn):
            raise TypeError('Passed function is not callable.')

        if not isinstance(timeout, int):
            raise TypeError('Passed timeout is not an integer.')

        self.timeout = timeout
        self.fn = fn
        self.fn_args = args
        self._api_token = None
        self._token_birth = datetime.datetime.now()

    @property
    def key(self):
        now = datetime.datetime.now()

        if self._api_token is None:
            self._token_birth = now
            self._api_token = self.fn(*self.fn_args)
        elif (now - self._token_birth).total_seconds() > self.timeout:
            self._token_birth = now
            self._api_token = self.fn(*self.fn_args)

        return self._api_token

    @key.setter
    def key(self, k):
        self._api_token = k

    @property
    def time_remaining(self):
        return self.timeout - (datetime.datetime.now() - self._token_birth).total_seconds()

    @time_remaining.setter
    def time_remaining(self, seconds):
        self._token_birth = datetime.datetime.now() + datetime.timedelta(seconds=seconds - self.timeout)



