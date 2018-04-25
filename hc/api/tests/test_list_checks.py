import json
from datetime import timedelta as td
from django.utils.timezone import now

from hc.api.models import Check
from hc.test import BaseTestCase

from dateutil import parser

class ListChecksTestCase(BaseTestCase):

    def setUp(self):
        super(ListChecksTestCase, self).setUp()

        self.now = now().replace(microsecond=0)

        self.a1 = Check(user=self.alice, name="Alice 1")
        self.a1.timeout = td(seconds=3600)
        self.a1.grace = td(seconds=900)
        self.a1.last_ping = self.now
        self.a1.n_pings = 1
        self.a1.status = "new"
        self.a1.save()

        self.a2 = Check(user=self.alice, name="Alice 2")
        self.a2.timeout = td(seconds=86400)
        self.a2.grace = td(seconds=3600)
        self.a2.last_ping = self.now
        self.a2.status = "up"
        self.a2.save()

    def get(self):
        return self.client.get("/api/v1/checks/", HTTP_X_API_KEY="abc")

    def test_it_works(self):
        r = self.get()
        
        self.assertEqual(r.status_code, 200)

        doc = r.json()
        self.assertTrue("checks" in doc)

        checks = {check["name"]: check for check in doc["checks"]}
        
        self.assertEqual(len(checks), 2)

        #Alice 1
        self.assertEqual(checks['Alice 1']['timeout'], 3600)
        self.assertEqual(checks['Alice 1']['grace'], 900)
        self.assertIn('http://', checks['Alice 1']['ping_url'])
        self.assertEqual(checks['Alice 1']['status'], 'new')
        self.assertEqual(self.now, parser.parse(checks['Alice 1']['last_ping']))
        self.assertEqual(checks['Alice 1']['n_pings'], 1)
        self.assertIn('pause', checks['Alice 1']['pause_url'])

        #Alice 2
        self.assertEqual(checks['Alice 2']['timeout'], 86400)
        self.assertEqual(checks['Alice 2']['grace'], 3600)
        self.assertIn('http://', checks['Alice 2']['ping_url'])
        self.assertEqual(checks['Alice 2']['status'], 'up')
        self.assertEqual(self.now, parser.parse(checks['Alice 2']['last_ping']))
        self.assertEqual(checks['Alice 2']['n_pings'], 0)
        self.assertIn('pause', checks['Alice 2']['pause_url'])

    def test_it_shows_only_users_checks(self):
        bobs_check = Check(user=self.bob, name="Bob 1")
        bobs_check.save()

        r = self.get()
        data = r.json()

        self.assertEqual(len(data["checks"]), 2)

        for check in data["checks"]:
            self.assertNotEqual(check["name"], "Bob 1")
            
    def test_it_accepts_request_api_key(self):
        r = self.client.generic("GET","/api/v1/checks/",
                        json.dumps({"api_key": "abc"}),
                        content_type="application/json")

        self.assertEqual(r.status_code, 200)
        self.assertIn("Alice", r.content.decode("utf-8"))     