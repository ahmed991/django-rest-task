from django.contrib.auth.models import User
from rest_framework.test import APIClient
from django.test import TestCase


test_create_object = {
    "name": "Unit test municipality",
    "code": "UnitTEST1",
    "geom": {
        "type": "MultiPolygon",
        "coordinates": [[[[6.8638226363766535, 52.22593356417747],
                          [6.8638226363766535, 52.22336306334935],
                          [6.867694876080947,  52.22336306334935],
                          [6.867694876080947,  52.22593356417747],
                          [6.8638226363766535, 52.22593356417747]]]]
    }
}
class MunicipalityTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_municipality(self):
        response = self.client.post('/api/municipalities/', test_create_object, format='json')
        self.assertEqual(response.status_code, 201)

    def test_list_municipality(self):
        response = self.client.get('/api/municipalities/')
        self.assertEqual(response.status_code, 200)
