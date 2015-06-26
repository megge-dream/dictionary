from noseapp_requests import make_config, RequestsEx
from noseapp import Suite
from noseapp import NoseApp
from noseapp.case import step
from noseapp import ScreenPlayCase
import random, string


class MyTestApplication(NoseApp):

    def initialize(self):
        self.setup_case_settings()

    def setup_case_settings(self):
        endpoint = make_config()
        endpoint.configure(
            base_url='http://127.0.0.1:5000/',
            key='localhost'
        )
        requests_ex = RequestsEx(endpoint)
        global api
        api = requests_ex.get_endpoint_session('localhost')


def create_app(config=None, argv=None, plugins=None):
    return MyTestApplication(
        config=config, argv=argv, plugins=plugins,
    )


suite = Suite(__name__)


@suite.register
class TestPostMethod(ScreenPlayCase):
    test_key = None

    def random_word(self, length):
        return ''.join(random.choice(string.lowercase) for i in range(length))

    def begin(self):
        data = api.get('dictionary').json()
        self.test_key = self.random_word(10)
        while self.test_key in data.keys():
            self.test_key = self.random_word(10)

    @step(1, 'POST method with unique key')
    def step_one(self):
        r = api.post('dictionary', {"key": self.test_key, "value": "target"}).json()
        assert r['result'] == "target"

    @step(2, 'POST method with exist key')
    def step_two(self):
        assert api.post('dictionary', {"key": self.test_key, "value": "target"}).status_code == 409

    @step(3, 'POST method without value in json')
    def step_three(self):
        assert api.post('dictionary', {"key": "mail.ru"}).status_code == 400

    @step(4, 'POST method without key in json')
    def step_four(self):
        assert api.post('dictionary', {"value": "target"}).status_code == 400

    def finalize(self):
        api.delete('dictionary/' + self.test_key)


@suite.register
class TestGetMethod(ScreenPlayCase):
    test_key = None

    def random_word(self, length):
        return ''.join(random.choice(string.lowercase) for i in range(length))

    def begin(self):
        data = api.get('dictionary').json()
        self.test_key = self.random_word(10)
        while self.test_key in data.keys():
            self.test_key = self.random_word(10)
        api.post('dictionary', {"key": self.test_key, "value": "target"})

    @step(1, 'GET method for existed key')
    def step_one(self):
        r = api.get('dictionary/' + self.test_key).json()
        assert r['result'] == "target"

    @step(2, 'GET method for non-existent key')
    def step_two(self):
        api.delete('dictionary/' + self.test_key)
        assert api.get('dictionary/111').status_code == 404


@suite.register
class TestPutMethod(ScreenPlayCase):
    test_key = None

    def random_word(self, length):
        return ''.join(random.choice(string.lowercase) for i in range(length))

    def begin(self):
        data = api.get('dictionary').json()
        self.test_key = self.random_word(10)
        while self.test_key in data.keys():
            self.test_key = self.random_word(10)
        api.post('dictionary', {"key": self.test_key, "value": "target"})

    @step(1, 'PUT method with exist key')
    def step_one(self):
        r = api.put('dictionary/' + self.test_key, {"value": "target"}).json()
        assert r['result'] == "target"

    @step(2, 'POST method without value in json')
    def step_two(self):
        assert api.put('dictionary/' + self.test_key, {}).status_code == 400

    @step(3, 'PUT method with non-existent key')
    def step_three(self):
        api.delete('dictionary/' + self.test_key)
        assert api.put('dictionary/' + self.test_key, {"value": "target"}).status_code == 404


@suite.register
class TestDeleteMethod(ScreenPlayCase):
    test_key = None

    def random_word(self, length):
        return ''.join(random.choice(string.lowercase) for i in range(length))

    def begin(self):
        data = api.get('dictionary').json()
        self.test_key = self.random_word(10)
        while self.test_key in data.keys():
            self.test_key = self.random_word(10)
        api.post('dictionary', {"key": self.test_key, "value": "target"})

    @step(1, 'DELETE method for existed key')
    def step_one(self):
        r = api.delete('dictionary/' + self.test_key).json()
        assert r['result'] is None

    @step(2, 'DELETE method for non-existent key')
    def step_two(self):
        r = api.delete('dictionary/' + self.test_key).json()
        assert r['result'] is None


api = {}
app = create_app()
app.register_suite(suite)
app.run()
