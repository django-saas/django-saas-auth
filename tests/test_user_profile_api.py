from saas_base.test import SaasTestCase


class TestUserProfileAPI(SaasTestCase):
    user_id = SaasTestCase.OWNER_USER_ID

    def test_fetch_user(self):
        self.force_login()
        user = self.get_user()
        user.first_name = 'Foo'
        user.save()
        resp = self.client.get('/api/user/')
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data['name'], user.get_full_name())

    def test_update_picture(self):
        self.force_login()
        resp = self.client.patch(
            '/api/user/profile/',
            {'picture': 'https://example.com/foo.png'},
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data['picture'], 'https://example.com/foo.png')
