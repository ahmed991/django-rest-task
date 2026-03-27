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
test_create_object_2 = {
    "name": "Unit test municipality 2",
    "code": "UnitTEST2",
    "geom": {
        "type": "MultiPolygon",
        "coordinates": [[[[4.0, 51.0],
                          [4.0, 52.0],
                          [5.0, 52.0],
                          [5.0, 51.0],
                          [4.0, 51.0]]]]  # deliberately outside bbox
    }
}
bbox_string = '5.855075164747461,52.84452676586113,7.54824215650271,53.48934042770347'

patch_object = {
    "name": "Unit test municipality-rename",
    "code": "Unit-001"
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

    def test_bbox_municipality(self):
        self.client.post('/api/municipalities/', test_create_object, format='json')
        self.client.post('/api/municipalities/', test_create_object_2, format='json')
        response = self.client.get('/api/municipalities/bbox_filter/', {'in_bbox': bbox_string})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)

    def test_patch_municipality(self):
        response = self.client.post('/api/municipalities/', test_create_object, format='json')
        print(response.data)
        # id = response.data['properties']['id']
        # response = self.client.patch(f'/api/municipalities/{id}/', patch_object, format='json')
        # self.assertEqual(response.status_code, 200)




