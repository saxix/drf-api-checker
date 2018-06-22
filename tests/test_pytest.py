from django.urls import reverse

from drf_api_checker.pytest import contract, frozenfixture
from drf_api_checker.recorder import Recorder


class MyRecorder(Recorder):
    def assert_timestamp(self, response, stored, path):
        assert response


@frozenfixture
def frozen_detail(db):
    from demo.factories import DetailFactory
    return DetailFactory()


@contract(recorder_class=MyRecorder)
def test_url_get(frozen_detail):
    url = reverse("master-list")
    return url

#
# @contract(recorder_class=MyRecorder, method='put')
# def test_url_put(frozen_detail):
#     url = reverse("master-update", args=[frozen_detail.pk])
#     return url, {"name": "name1"}
#
#
# @contract(recorder_class=MyRecorder, method='post')
# def test_url_post(frozen_detail):
#     url = reverse("master-create")
#     return url, {"name": "name1"}
#
#
# @contract(recorder_class=MyRecorder, method='delete', allow_empty=True)
# def test_url_delete(frozen_detail):
#     url = reverse("master-delete", args=[frozen_detail.pk])
#     return url
