![Logo](https://raw.githubusercontent.com/sawyersteven/APISitter/master/img/Logo_wide.png)

# APISitter
Let APISitter renew your expiring api keys for you.

### Installation
APISitter has been tested on Python 3.4.0

Install via pip with `pip install APISitter`

### Usage

Instantiate APISitter using `APISitter(timeout, fn, *args)`

&emsp;&emsp;`timeout` int: Seconds after which api key will expire. It is best to set this to be slightly shorter than the actual expiration time, ie a 10-minute key should have a timeout of 545 seconds.

&emsp;&emsp;`fn` function: Called to get key from server. Pass any method that returns a your api key. This method will be called again any time you access APISitter.key and the timeout has elapsed.

&emsp;&emsp;`*args`: Arguments to pass to fn when it is called.

    from APISitter import APISitter
    import requests

    def get_api_key(username, password):
        ''' Your method to get a key from the server '''
        return requests.post('https://apiendpoint.com/key', {'user': username, 'pass', password}).text

    api_sitter = APISitter(600, get_api_key, 'JohnZoidberg', 'supersecretpassword')

    # Make an api request
    response = requests.post('https://apiendpoint.com/dosomething?apikey={}'.format(api_sitter.key))

The APISitter class offers two properties with which you may interact.

&emsp;&emsp;`APISitter.key` Get the api key returned by 'get_api_key'

&emsp;&emsp;`APISitter.key = 'set_a_key_manually'` Manually set the key. Will be overwritten after timeout has elapsed.

&emsp;&emsp;`APISitter.time_remaining` Get remaining lifespan of api key in seconds. This is calculated on-demand and will return a negative value if the key has expired.

&emsp;&emsp;`APISitter.time_remaining = 1200` Manually set time left before api key expires. This is temporary and only affects the current api key.

&emsp;&emsp;`APISitter.timeout = 300` Set the expiration time of the api key. This is the same as `timeout` passed when instantiating APISitter.


### How It Works

Every time you ask for your api key APISitter checks to see if it has expired and gets a new key if required.

APISitter is lazy and only retreives a new key when you need it.

APISitter makes no attempt to catch exceptions. Always use good practices when creating your key retreiving methods.

