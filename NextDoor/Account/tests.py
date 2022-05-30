from django.contrib.auth import get_user_model
from django.test import TestCase,SimpleTestCase
from django.urls import reverse, resolve
from .form import CustomUserCreationForm, MessageForm, CommentForm, RequestForm# new
from .views import *
from .models import MessageModel,CommentModel,RequestModel,SupportTicketModel,UserTicketModel
from .url import *
from django.urls import reverse,resolve




class CustomUserTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username='Bob',
            email='Bob@email.com',
            password='testBob123'
        )

        self.assertEqual(user.username, 'Bob')
        self.assertEqual(user.email, 'Bob@email.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            username='Ashe',
            email='Ashe@email.com',
            password='testAshe123'
        )

        self.assertEqual(admin_user.username, 'Ashe')
        self.assertEqual(admin_user.email, 'Ashe@email.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)


class SignupTests(TestCase):  # new
    username = 'BobTheTester'
    email = 'newuser@email.com'

    def setUp(self):
        url = reverse('signup')
        self.response = self.client.get(url)

    def test_signup_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'Account/signup.html')
        self.assertContains(self.response, 'Sign Up')
        self.assertNotContains(
            self.response, 'invalid Page.')

    def test_signup_form(self):  # new
        form = self.response.context.get('form')

        self.assertIsInstance(form, CustomUserCreationForm)
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_signup_view(self): # new
        view = resolve('/Account/signup/')
        self.assertEqual(
        view.func.__name__,
        SignupPageView.as_view().__name__)




# Create a class to test RequestModel model
class RequestModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='Bob', password='testBob123')
        self.request = RequestModel.objects.create(
            user=self.user,
            title='Test Request',
            description='Test Description',
        )

    def test_request_model(self):
        self.assertEqual(self.request.title, 'Test Request')
        self.assertEqual(self.request.description, 'Test Description')
        self.assertEqual(self.request.user, self.user)

    def test_request_model_str(self):
        self.assertEqual(str(self.request), 'Test Request')

    # Test RequesetForm
    def test_request_form(self):
        form = RequestForm(data={
            'title': 'Test Request',
            'description': 'Test Description',
        })
        self.assertTrue(form.is_valid())

    def test_request_form_invalid(self):
        form = RequestForm(data={
            'title': '',
            'description': 'Test Description',
        })
        self.assertFalse(form.is_valid())

    def test_request_form_invalid_title(self):
        form = RequestForm(data={
            'title': '',
            'description': 'Test Description',
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['title'], [u'This field is required.'])

    def test_request_form_invalid_description(self):
        form = RequestForm(data={
            'title': 'Test Request',
            'description': '',
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['description'], [u'This field is required.'])


# Create a class to test MessageModel model
class MessageModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='Bob', password='testBob123')
        # create another user
        self.user2 = get_user_model().objects.create_user(
            username='Bob2', password='testBob123')
        # create a message bob sends to bob2
        self.message = MessageModel.objects.create(
            sender=self.user,
            receiver=self.user2,
            message='Test Description',
        )

    def test_message_model(self):
        self.assertEqual(self.message.message, 'Test Description')
        self.assertEqual(self.message.sender, self.user)
        self.assertEqual(self.message.receiver, self.user2)

    def test_message_model_str(self):
        self.assertEqual(str(self.message), 'Test Description')

    # Test MessageForm
    def test_message_form(self):
        form = MessageForm(data={
            'message': 'Test Description',
        })
        self.assertTrue(form.is_valid())

    def test_message_form_invalid(self):
        form = MessageForm(data={
            'message': '',
        })
        self.assertFalse(form.is_valid())

    def test_message_form_invalid_message(self):
        form = MessageForm(data={
            'message': '',
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['message'], [u'This field is required.'])



# test CommentModel
class CommentModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='Bob', password='testBob123')
        # create a request for bob
        self.request = RequestModel.objects.create(
            title='Test Request',
            description='Test Description',
            user=self.user,
        )
        # create a comment for bob
        self.comment = CommentModel.objects.create(
            user=self.user,
            request=self.request,
            comment='Test Comment',
        )

    def test_comment_model(self):
        self.assertEqual(self.comment.comment, 'Test Comment')
        self.assertEqual(self.comment.user, self.user)
        self.assertEqual(self.comment.request, self.request)

    def test_comment_model_str(self):
        self.assertEqual(str(self.comment), 'Test Comment')

    # Test CommentForm
    def test_comment_form(self):
        form = CommentForm(data={
            'comment': 'Test Comment',
        })
        self.assertTrue(form.is_valid())

    def test_comment_form_invalid(self):
        form = CommentForm(data={
            'comment': '',
        })
        self.assertFalse(form.is_valid())

    def test_comment_form_invalid_comment(self):
        form = CommentForm(data={
            'comment': '',
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['comment'], [u'This field is required.'])


# UserProfile model test
class UserProfileTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='Bob', password='testBob123')
        # create userprofile for bob
        self.userprofile = UserProfile.objects.create(
            user=self.user,
            first_name='Bob',
            last_name='Bob',
            bio='Test Bio',
        )

    def test_userprofile_model(self):
        self.assertEqual(self.userprofile.user, self.user)
        self.assertEqual(self.userprofile.first_name, 'Bob')
        self.assertEqual(self.userprofile.last_name, 'Bob')
        self.assertEqual(self.userprofile.bio, 'Test Bio')

    # Test UserProfileForm
    def test_userprofile_form(self):
        form = UserProfileForm(data={
            'first_name': 'Bob',
            'last_name': 'Bob',
            'bio': 'Test Bio',
        })
        self.assertTrue(form.is_valid())


# test SupportTicketModel
class SupportTicketModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='Bob', password='testBob123')

        self.request_user = UserProfile.objects.create(
            user=self.user,
            first_name='Bob',
            last_name='Bob',
            bio='Test Bio',
        )
        # create a request_user for bob
        self.request = RequestModel.objects.create(
            title='Test Request',
            description='Test Description',
            user=self.user,
        )
        # create a comment for bob
        self.comment = CommentModel.objects.create(
            user=self.user,
            request=self.request,
            comment='Test Comment',
        )
        # create a message for bob
        self.message = MessageModel.objects.create(
            sender=self.user,
            receiver=self.user,
            message='Test Description',
        )
        self.description = 'Test Description'

        self.supportticket = SupportTicketModel.objects.create(
            user =self.user,
            request_user=self.request_user,
            request=self.request,
            comment = self.comment,
            message = self.message,
            description= self.description,
        )

    def test_supportticket_model(self):
        self.assertEqual(self.supportticket.comment, self.comment)
        self.assertEqual(self.supportticket.user, self.user)
        self.assertEqual(self.supportticket.request, self.request)
        self.assertEqual(self.supportticket.request_user, self.request_user)
        self.assertEqual(self.supportticket.message, self.message)
        self.assertEqual(self.supportticket.description, 'Test Description')

    def test__SupportTicket_model_str(self):
        self.assertEqual(str(self.description), 'Test Description')

    # Test CommentForm
    def test_SupportTicket_form(self):
        form = SupportTicketForm(data={
            'description':'Test Description',
        })
        self.assertTrue(form.is_valid())


# test UserTicketModel
class UserTicketModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='Bob', password='testBob123')

        self.request_user = UserProfile.objects.create(
            user=self.user,
            first_name='Bob',
            last_name='Bob',
            bio='Test Bio',
        )
        self.description = 'Test Description'

        self.userticket = UserTicketModel.objects.create(
            user =self.user,
            request_user=self.request_user,
            description= self.description,
        )

    def test_userticket_model(self):
        self.assertEqual(self.userticket.user, self.user)
        self.assertEqual(self.userticket.request_user, self.request_user)
        self.assertEqual(self.userticket.description, 'Test Description')

    def test__userticket_model_str(self):
        self.assertEqual(str(self.description), 'Test Description')

    # Test CommentForm
    def test_userticket_form(self):
        form = UserTicketForm(data={
            'description':'Test Description',
        })
        self.assertTrue(form.is_valid())


# integration test support ticket and user ticket
class SupportTicketIntegrationTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='Bob', password='testBob123')

        self.request_user = UserProfile.objects.create(
            user=self.user,
            first_name='Bob',
            last_name='Bob',
            bio='Test Bio',
        )
        self.description = 'Test Description'

        self.supportticket = SupportTicketModel.objects.create(
            user =self.user,
            request_user=self.request_user,
            description= self.description,
        )

        self.userticket = UserTicketModel.objects.create(
            user =self.user,
            request_user=self.request_user,
            description= self.description,
        )

    def test_supportticket_integration(self):
        self.assertEqual(self.supportticket.user, self.user)
        self.assertEqual(self.supportticket.request_user, self.request_user)
        self.assertEqual(self.supportticket.description, 'Test Description')

    def test_userticket_integration(self):
        self.assertEqual(self.userticket.user, self.user)
        self.assertEqual(self.userticket.request_user, self.request_user)
        self.assertEqual(self.userticket.description, 'Test Description')



# integration test user profile and comment
class UserProfileIntegrationTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='Bob', password='testBob123')

        self.request_user = UserProfile.objects.create(
            user=self.user,
            first_name='Bob',
            last_name='Bob',
            bio='Test Bio',
        )
        self.description = 'Test Description'

        self.comment = CommentModel.objects.create(
            user=self.user,
            request=self.request_user,
            comment='Test Comment',
        )

    def test_userprofile_integration(self):
        self.assertEqual(self.comment.user, self.user)
        self.assertEqual(self.comment.request, self.request_user)
        self.assertEqual(self.comment.comment, 'Test Comment')


# Integration test user profile and request
class UserProfileIntegrationTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='Bob', password='testBob123')

        self.request_user = UserProfile.objects.create(
            user=self.user,
            first_name='Bob',
            last_name='Bob',
            bio='Test Bio',
        )
        self.description = 'Test Description'

        self.request = RequestModel.objects.create(
            title='Test Request',
            description='Test Description',
            user=self.user,
        )

    def test_userprofile_integration(self):
        self.assertEqual(self.request.user, self.user)
        self.assertEqual(self.request.description, 'Test Description')
        self.assertEqual(self.request.title, 'Test Request')


# Integration test request and comment
class RequestIntegrationTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='Bob', password='testBob123')

        self.request_user = UserProfile.objects.create(
            user=self.user,
            first_name='Bob',
            last_name='Bob',
            bio='Test Bio',
        )
        self.description = 'Test Description'

        self.request = RequestModel.objects.create(
            title='Test Request',
            description='Test Description',
            user=self.user,
        )

        self.comment = CommentModel.objects.create(
            user=self.user,
            request=self.request,
            comment='Test Comment',
        )

    def test_request_integration(self):
        self.assertEqual(self.request.user, self.user)
        self.assertEqual(self.request.description, 'Test Description')
        self.assertEqual(self.request.title, 'Test Request')

    def test_comment_integration(self):
        self.assertEqual(self.comment.user, self.user)
        self.assertEqual(self.comment.request, self.request)
        self.assertEqual(self.comment.comment, 'Test Comment')



# Integration test support ticket and request
class SupportTicketIntegrationTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='Bob', password='testBob123')

        self.request_user = UserProfile.objects.create(
            user=self.user,
            first_name='Bob',
            last_name='Bob',
            bio='Test Bio',
        )
        self.description = 'Test Description'

        self.supportticket = SupportTicketModel.objects.create(
            user =self.user,
            request_user=self.request_user,
            description= self.description,
        )

        self.request = RequestModel.objects.create(
            title='Test Request',
            description='Test Description',
            user=self.user,
        )

    def test_supportticket_integration(self):
        self.assertEqual(self.supportticket.user, self.user)
        self.assertEqual(self.supportticket.request_user, self.request_user)
        self.assertEqual(self.supportticket.description, 'Test Description')

    def test_request_integration(self):
        self.assertEqual(self.request.user, self.user)
        self.assertEqual(self.request.description, 'Test Description')
        self.assertEqual(self.request.title, 'Test Request')


# Integration test user ticket and user profile
class UserTicketIntegrationTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='Bob', password='testBob123')

        self.request_user = UserProfile.objects.create(
            user=self.user,
            first_name='Bob',
            last_name='Bob',
            bio='Test Bio',
        )
        self.description = 'Test Description'

        self.userticket = UserTicketModel.objects.create(
            user =self.user,
            request_user=self.request_user,
            description= self.description,
        )

        self.request = RequestModel.objects.create(
            title='Test Request',
            description='Test Description',
            user=self.user,
        )

    def test_userticket_integration(self):
        self.assertEqual(self.userticket.user, self.user)
        self.assertEqual(self.userticket.request_user, self.request_user)
        self.assertEqual(self.userticket.description, 'Test Description')

    def test_request_integration(self):
        self.assertEqual(self.request.user, self.user)
        self.assertEqual(self.request.description, 'Test Description')
        self.assertEqual(self.request.title, 'Test Request')







class TestUrls(SimpleTestCase):

    def test_Rulse_url_is_resolved(self):
        url = reverse('Rulse')
        self.assertEqual(resolve(url).func,Rulse)

    def test_user_profile_url_is_resolved(self):
        url = reverse('user_profile', args=['fake_id'])
        self.assertEqual(resolve(url).func,user_profile)

    def test_edit_profile_url_is_resolved(self):
        url = reverse('edit_profile', args=['fake_id'])
        self.assertEqual(resolve(url).func,edit_profile)

    def test_delete_user_url_is_resolved(self):
        url = reverse('delete_user', args=['fake_id'])
        self.assertEqual(resolve(url).func,delete_user)

    def test_create_request_url_is_resolved(self):
        url = reverse('create_request', args=['fake_id'])
        self.assertEqual(resolve(url).func,create_request)

    def test_requests_url_is_resolved(self):
        url = reverse('requests', args=['fake_id'])
        self.assertEqual(resolve(url).func,requests)

    def test_messaging_url_is_resolved(self):
        url = reverse('messaging', args=['fake_id'])
        self.assertEqual(resolve(url).func,messaging)

    def test_inbox_url_is_resolved(self):
        url = reverse('inbox', args=['fake_id'])
        self.assertEqual(resolve(url).func,inbox)

    def test_user_ticket_url_is_resolved(self):
        url = reverse('user_ticket', args=['fake_id'])
        self.assertEqual(resolve(url).func,user_ticket)

    def test_messaging_read_url_is_resolved(self):
        url = reverse('messaging_read', args=['fake_id',1])
        self.assertEqual(resolve(url).func,messaging_read)

    def test_messaging_delete_url_is_resolved(self):
        url = reverse('messaging_delete', args=['fake_id',1])
        self.assertEqual(resolve(url).func,messaging_delete)

    def test_view_request_url_is_resolved(self):
        url = reverse('view_request', args=['fake_id',1])
        self.assertEqual(resolve(url).func,view_request)

    def test_delete_request_url_is_resolved(self):
        url = reverse('delete_request', args=['fake_id',1])
        self.assertEqual(resolve(url).func,delete_request)

    def test_close_request_url_is_resolved(self):
        url = reverse('close_request', args=['fake_id',1])
        self.assertEqual(resolve(url).func,close_request)

    def test_edit_request_url_is_resolved(self):
        url = reverse('edit_request', args=['fake_id',1])
        self.assertEqual(resolve(url).func,edit_request)

    def test_edit_comment_url_is_resolved(self):
        url = reverse('edit_comment', args=['fake_id',1])
        self.assertEqual(resolve(url).func,edit_comment)

    def test_support_ticket_is_resolved(self):
        url = reverse('support_ticket')
        self.assertEqual(resolve(url).func,support_ticket)

    def test_RemoveBan_is_resolved(self):
        url = reverse('RemoveBan')
        self.assertEqual(resolve(url).func,RemoveBan)

    def test_request_to_delete_is_resolved(self):
        url = reverse('request_to_delete')
        self.assertEqual(resolve(url).func,request_to_delete)

    def test_Open_support_tickets_is_resolved(self):
        url = reverse('Open_support_tickets')
        self.assertEqual(resolve(url).func,Open_support_tickets)

    def test_Banned_list_is_resolved(self):
        url = reverse('Banned_list')
        self.assertEqual(resolve(url).func,Banned_list)

    def test_change_status_ticket_url_is_resolved(self):
        url = reverse('change_status_ticket', args=[1])
        self.assertEqual(resolve(url).func,change_status_ticket)


