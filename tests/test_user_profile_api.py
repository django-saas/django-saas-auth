from django.test import override_settings
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
        self.assertIsNone(data['avatar'])

    @override_settings(SAAS_AUTH={'ENABLE_GRAVATAR': True})
    def test_fetch_gravatar(self):
        self.force_login()
        resp = self.client.get('/api/user/profile/')
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn('avatar', data)
        self.assertTrue(data['avatar'].startswith('https://gravatar.com/'))

    def test_update_user_with_profile_data(self):
        self.force_login()
        data = {
            'first_name': 'Foo',
            'last_name': 'Bar',
            'locale': 'zh-Hans',
        }
        resp = self.client.patch('/api/user/', data)
        self.assertEqual(resp.status_code, 200)
        result = resp.json()
        self.assertEqual(result['locale'], 'zh-Hans')

    def test_update_invalid_avatar(self):
        self.force_login()
        data = {'avatar': 'foo'}
        resp = self.client.patch('/api/user/', data)
        self.assertEqual(resp.status_code, 400)

    def test_update_avatar(self):
        self.force_login()
        resp = self.client.patch(
            '/api/user/profile/',
            {'avatar': 'https://example.com/foo.png'},
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data['avatar'], 'https://example.com/foo.png')
