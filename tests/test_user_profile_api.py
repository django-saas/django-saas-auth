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

    def test_update_invalid_picture(self):
        self.force_login()
        data = {'picture': 'foo'}
        resp = self.client.patch('/api/user/', data)
        self.assertEqual(resp.status_code, 400)

    def test_update_profile_picture(self):
        self.force_login()
        resp = self.client.patch(
            '/api/user/profile/',
            {'picture': 'https://example.com/foo.png'},
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data['picture'], 'https://example.com/foo.png')
