__author__ = 'philroche'

import unittest
import json

from django.test import Client
from django.core.urlresolvers import reverse

from cached_hitcount.utils import is_cached_hitcount_enabled
from cached_hitcount.models import Hit
from cached_hitcount.utils import get_target_ctype_pk, get_hit_count
from cached_hitcount.tasks import persist_hits

class CachedHitCountTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        #create a model to use to test hits
        self._clear_old_hits()
        self._create_sample_model()

    def _clear_old_hits(self):
        Hit.objects.all().delete()

    def _create_sample_model(self):
        self.sample_model = Hit()
        self.sample_model.object_pk = 435
        ctype, object_pk = get_target_ctype_pk(self.sample_model)
        self.sample_model.content_type = ctype
        self.sample_model.save()

    def test_enabled(self):
        self.assertTrue(is_cached_hitcount_enabled)

    def test_can_add_to_cache(self):
        #$.post( '/hits/',{ object_pk : '1', ctype_pk :  '8', csrfmiddlewaretoken: 'fcvMlt1fkwY8qK5NFgazvxy5iaWGGha8'},'json');
        json_string = { 'object_pk' : '%s' % str(self.sample_model.pk), 'ctype_pk' :  '%s' % str(self.sample_model.content_type.pk), 'csrfmiddlewaretoken': 'fcvMlt1fkwY8qK5NFgazvxy5iaWGGha8'}
        response = self.client.post(reverse('update_hit_count_ajax'),
                            json_string,
                            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        response_data = json.loads(response.content)
        self.assertEqual(response_data["status"],"success")


    def test_can_persist(self):
        self.test_can_add_to_cache()
        try:
            persist_hits()
        except Exception:
            self.fail("persist_hits raised Exception unexpectedly!")


    def test_can_read(self):
        self.test_can_persist()#this will reset the memcached hit count to 0
        self._clear_old_hits()
        self._create_sample_model()
        self.test_can_persist()
        hit_count = get_hit_count(self.sample_model)
        self.assertEqual(hit_count, "1")

if __name__ == '__main__':
    unittest.main()