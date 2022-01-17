from django.contrib.auth.models import User
from .models import Post
from rest_framework import status
from rest_framework.test import APITestCase


class PostListViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username='testy_mc_testable', password='zesty-tester')

    def test_can_list_posts(self):
        testy_mc_testable = User.objects.get(username='testy_mc_testable')
        Post.objects.create(owner=testy_mc_testable, title='A zesty testy test!')
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_in_user_can_create_post(self):
        self.client.login(username='testy_mc_testable', password='zesty-tester')
        response = self.client.post('/posts/', {'title': 'A very zesty testy test!'})
        count = Post.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_logged_out_user_cannot_create_a_post(self):
        response = self.client.post('/posts/', {'title': 'An even more zesty test!'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PostDetailViewTests(APITestCase):
    def setUp(self):
        peter = User.objects.create_user(username='peter', password='pass')
        the_pan = User.objects.create_user(username='the_pan', password='pass')
        Post.objects.create(
            owner=peter, title='Peter wrote this', content='Peters content'
        )
        Post.objects.create(
            owner=the_pan, title='Pan wrote this', content='Pans content'
        )

    def test_can_retrieve_post_using_valid_id(self):
        response = self.client.get('/posts/1/')
        self.assertEqual(response.data['title'], 'Peter wrote this')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cannot_retrieve_post_using_invalid_id(self):
        response = self.client.get('/posts/129328423/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_own_post(self):
        self.client.login(username='peter', password='pass')
        response = self.client.put('/posts/1/', {'title': 'Tis the season to be jolly'})
        post = Post.objects.filter(pk=1).first()
        self.assertEqual(post.title, 'Tis the season to be jolly')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cannot_update_another_users_post(self):
        self.client.login(username='peter', password='pass')
        response = self.client.put('/posts/2/', {'title': 'Tsk tsk tsk...'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
