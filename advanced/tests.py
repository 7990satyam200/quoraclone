from django.urls import reverse
from django.test import TestCase

class HomeTests(TestCase):
    def test_home_view_status_code(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)


    class BoardTopicsTests(TestCase):
        def setUp(self):
            Board.objects.create(name='Django', description='Django board.')

        def test_board_topic_view_success_status_code(self):
            url = reverse('board_topics', kwargs={'pk': 1})
            response = self.client.get(url)
            self.assertEquals(response.status_code, 200)

        def test_board_topic_view_not_found_status_code(self):
            url = reverse('board_topics', kwargs={'pk': 99})
            response = self.client.get(url)
            self.assertEquals(response.status_code, 404)

        def test_board_topic_url_resolves_board_topics_view(self):
            view = resolve('/boards/1/')
            self.assertEquals(view.func, board_topics)

    class NewTopicTests(TestCase):
        def setUp(self):
            Board.objects.create(name='Django', description='Django board.')

        def test_new_topic_view_success_status_code(self):
            url = reverse('new_topic', kwargs={'pk': 1})
            response = self.client.get(url)
            self.assertEquals(response.status_code, 200)

        def test_new_topic_view_not_found_status_code(self):
            url = reverse('new_topic', kwargs={'pk': 99})
            response = self.client.get(url)
            self.assertEquals(response.status_code, 404)

        def test_new_topic_url_resolves_new_topic_view(self):
            view = resolve('/boards/1/new/')
            self.assertEquals(view.func, new_topic)

        def test_new_topic_view_contains_link_back_to_board_topics_view(self):
            new_topic_url = reverse('new_topic', kwargs={'pk': 1})
            board_topics_url = reverse('board_topics', kwargs={'pk': 1})
            response = self.client.get(new_topic_url)
            self.assertContains(response, 'href="{0}"'.format(board_topics_url))