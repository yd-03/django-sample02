from django.test import TestCase
from django.urls import reverse
from nippo.models import NippoModel


class NippoTestCase(TestCase):
    def setUp(self):
        """テスト実行前に実行される初期化処理"""
        obj = NippoModel(title="testTitle1", content="testContent1")
        obj.save()

    def test_saved_single_object(self):
        """テストデータが1つ保存されているかどうか"""
        qs_counter = NippoModel.objects.count()
        self.assertEqual(qs_counter, 1)

    def test_response_404(self):
        """データが存在しない場合のレスポンスが404であるかどうか"""
        detail_url = reverse("nippo-detail", kwargs={"pk": 100})
        detail_response = self.client.get(detail_url)
        update_url = reverse("nippo-update", kwargs={"pk": 100})
        update_response = self.client.get(update_url)
        delete_url = reverse("nippo-delete", kwargs={"pk": 100})
        delete_response = self.client.get(delete_url)
        self.assertEqual(detail_response.status_code, 404)
        self.assertEqual(update_response.status_code, 404)
        self.assertEqual(delete_response.status_code, 404)

    def test_create_on_createView(self):
        """データが1件追加されるかどうか"""
        url = reverse("nippo-create")
        create_data = {"title": "title_from_test", "content": "content_from_test"}
        response = self.client.post(url, create_data)
        qs_counter2 = NippoModel.objects.count()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(qs_counter2, 2)
