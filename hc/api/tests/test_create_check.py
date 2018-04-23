import json

from hc.api.models import Channel, Check
from hc.test import BaseTestCase


class CreateCheckTestCase(BaseTestCase):
    URL = "/api/v1/checks/"

    def setUp(self):
        super(CreateCheckTestCase, self).setUp()

    def post(self, data, expected_error=None):
        r = self.client.post(self.URL, json.dumps(data),
                             content_type="application/json")
        possible_expected_errors = ["wrong api_key",
                                    "timeout is not a number",
                                    "name is not a string",
                                    "could not parse request body",
                                    "timeout is too small",
                                    "grace is too small"]

        if expected_error in possible_expected_errors:
            self.assertEqual(r.status_code, 400)
            
        return r

    def test_it_works(self):
        r = self.post({
            "api_key": "abc",
            "name": "Foo",
            "tags": "bar,baz",
            "timeout": 3600,
            "grace": 60
        })

        self.assertEqual(r.status_code, 201)
        doc = r.json()
        assert "ping_url" in doc
        self.assertEqual(doc["name"], "Foo")
        self.assertEqual(doc["tags"], "bar,baz")
        self.assertEqual(Check.objects.count(), 1)
        check = Check.objects.get()
        self.assertEqual(check.name, "Foo")
        self.assertEqual(check.tags, "bar,baz")
        self.assertEqual(check.timeout.total_seconds(), 3600)
        self.assertEqual(check.grace.total_seconds(), 60)
        self.assertEqual(check.n_pings, 0)
        self.assertEqual(check.last_ping, None)

    def test_it_accepts_api_key_in_header(self):
        payload = json.dumps({
            "name": "Foo"
        })

        r = self.client.post(self.URL,
                            HTTP_X_API_KEY="abc",
                            data = payload,
                            content_type='application/json')

        self.assertEqual(r.status_code, 201)

    def test_it_handles_missing_request_body(self):
        r = self.client.post(self.URL, content_type='application/json')       
        self.assertEqual(r.status_code, 400)
        self.assertEqual(json.loads(r.content.decode('utf-8'))['error'], "wrong api_key")

    def test_it_handles_invalid_json(self):
        r = self.client.post(self.URL)
        self.assertEqual(r.status_code, 400)
        self.assertEqual(json.loads(r.content.decode('utf-8'))['error'],
                        "could not parse request body")

    def test_it_rejects_wrong_api_key(self):
        response = self.post({"api_key": "wrong"},
                  expected_error="wrong api_key")    
        self.assertEqual(response.status_code, 400)

    def test_it_rejects_non_number_timeout(self):
        response = self.post({"api_key": "abc", "timeout": "oops"},
                  expected_error="timeout is not a number")
        self.assertEqual(response.status_code, 400)

    def test_it_rejects_non_string_name(self):
        response = self.post({"api_key": "abc", "name": False},
                  expected_error="name is not a string")       
        self.assertEqual(response.status_code, 400)

    def test_it_assigns_channels(self):
        r = self.post({
            "api_key": "abc",
            "name": "Foo",
            "tags": "bar,baz",
            "timeout": 3600,
            "grace": 60,
            "channels": "*"
        })

        self.assertEqual(r.status_code, 201)

    def test_timeout_too_small(self):
        r = self.post({
            "api_key": "abc",
            "name": "Foo",
            "tags": "bar,baz",
            "timeout": 59,
            "grace": 60
        })

        self.assertEqual(r.status_code, 400)
        self.assertEqual(json.loads(r.content.decode('utf-8'))['error'],
                        "timeout is too small")

    def test_timeout_too_large(self):
        r = self.post({
            "api_key": "abc",
            "name": "Foo",
            "tags": "bar,baz",
            "timeout": 604801,
            "grace": 60
        })
        
        self.assertEqual(r.status_code, 400)
        self.assertEqual(json.loads(r.content.decode('utf-8'))['error'],
                        "timeout is too large")


