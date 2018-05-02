from django.core import mail

from hc.test import BaseTestCase
from hc.accounts.models import Member
from hc.api.models import Check


class ProfileTestCase(BaseTestCase):

    def test_it_sends_set_password_link(self):
        self.client.login(username="alice@example.org", password="password")

        form = {"set_password": "1"}
        r = self.client.post("/accounts/profile/", form)
        assert r.status_code == 302

        # profile.token should be set now
        self.alice.profile.refresh_from_db()
        token = self.alice.profile.token        
        self.assertIsNotNone(token)
        self.assertGreater(len(token), 0)

        ### Assert that the email was sent and check email content
        self.assertGreater(len(mail.outbox), 0)
        self.assertIn('set a password for your account on healthchecks.io', mail.outbox[0].body)
        self.assertIn('Set password on healthchecks.io', mail.outbox[0].subject)

    def test_it_sends_report(self):
        check = Check(name="Test Check", user=self.alice)
        check.save()

        self.alice.profile.send_report()

        self.assertGreater(len(mail.outbox), 0)
        self.assertIn('This is a monthly report sent by healthchecks.io', mail.outbox[0].body)
        self.assertIsNot('', mail.outbox[0].subject)


    def test_it_adds_team_member(self):
        self.client.login(username="alice@example.org", password="password")

        form = {"invite_team_member": "1", "email": "frank@example.org"}
        r = self.client.post("/accounts/profile/", form)
        assert r.status_code == 200

        member_emails = set()
        for member in self.alice.profile.member_set.all():
            member_emails.add(member.user.email)

        self.assertTrue(len(member_emails), 2)
        self.assertIn(form['email'], member_emails)
        self.assertTrue("frank@example.org" in member_emails)
       

        
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('alice@example.org invites you to their healthchecks.io account', mail.outbox[0].body)

    def test_add_team_member_checks_team_access_allowed_flag(self):
        self.client.login(username="charlie@example.org", password="password")

        form = {"invite_team_member": "1", "email": "frank@example.org"}
        r = self.client.post("/accounts/profile/", form)
        assert r.status_code == 403

    def test_it_removes_team_member(self):
        self.client.login(username="alice@example.org", password="password")

        form = {"remove_team_member": "1", "email": "bob@example.org"}
        r = self.client.post("/accounts/profile/", form)
        assert r.status_code == 200

        self.assertEqual(Member.objects.count(), 0)

        self.bobs_profile.refresh_from_db()
        self.assertEqual(self.bobs_profile.current_team, None)

    def test_it_sets_team_name(self):
        self.client.login(username="alice@example.org", password="password")

        form = {"set_team_name": "1", "team_name": "Alpha Team"}
        r = self.client.post("/accounts/profile/", form)
        assert r.status_code == 200

        self.alice.profile.refresh_from_db()
        self.assertEqual(self.alice.profile.team_name, "Alpha Team")

    def test_set_team_name_checks_team_access_allowed_flag(self):
        self.client.login(username="charlie@example.org", password="password")

        form = {"set_team_name": "1", "team_name": "Charlies Team"}
        r = self.client.post("/accounts/profile/", form)
        assert r.status_code == 403

    def test_it_switches_to_own_team(self):
        self.client.login(username="bob@example.org", password="password")

        self.client.get("/accounts/profile/")

        # After visiting the profile page, team should be switched back
        # to user's default team.
        self.bobs_profile.refresh_from_db()
        self.assertEqual(self.bobs_profile.current_team, self.bobs_profile)

    def test_it_shows_badges(self):
        self.client.login(username="alice@example.org", password="password")
        Check.objects.create(user=self.alice, tags="foo a-B_1  baz@")
        Check.objects.create(user=self.bob, tags="bobs-tag")

        r = self.client.get("/accounts/profile/")
        self.assertContains(r, "foo.svg")
        self.assertContains(r, "a-B_1.svg")

        # Expect badge URLs only for tags that match \w+
        self.assertNotContains(r, "baz@.svg")

        # Expect only Alice's tags
        self.assertNotContains(r, "bobs-tag.svg")

    ### Test it creates and revokes API key
    def test_revoking_of_apikey(self):
        """test revoking of api key"""
        self.client.login(username='alice@example.org', password='password')
        form={"revoke_api_key": "API_Key"}
        result = self.client.post('/accounts/profile/', form)
        self.assertEqual(result.status_code, 200)
        self.alice.profile.refresh_from_db()
        api_key = self.alice.profile.api_key
        self.assertEqual(api_key, "")
        self.assertContains(result, "The API key has been revoked!")

    def test_change_reporting_interval(self):
        """testing successful change of report interval"""
        self.client.login(username="alice@example.org", password="password")
        form = {"reports_allowed":7}
        result = self.client.post('/accounts/profile/', form)
        self.assertEqual(200, result.status_code) 