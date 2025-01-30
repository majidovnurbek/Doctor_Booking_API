from django.test import TestCase
from .models import Doctor
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class DoctorModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email="testuser@example.com", password="password123")
        self.doctor = Doctor.objects.create(
            user=self.user,
            specialization="Cardiologist",
            experience=10,
            location="New York",
            clinic_name="Healthy Heart Clinic",
            cunsultation_fee=100.00,
            is_consultation_fee=True,
            avaible_today=True,
            rating_percentage=95,
            patient_stories=50
        )

    def test_doctor_creation(self):
        self.assertEqual(self.doctor.user.email, "testuser@example.com")
        self.assertEqual(self.doctor.specialization, "Cardiologist")
        self.assertEqual(self.doctor.experience, 10)

    def test_str_method(self):
        self.assertEqual(str(self.doctor), "Cardiologist")


##################################################################################
from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import News
from django.core.files.uploadedfile import SimpleUploadedFile

CustomUser = get_user_model()


class NewsModelTest(TestCase):
    def setUp(self):
        # Test uchun foydalanuvchi yaratamiz
        self.user = CustomUser.objects.create_user(email="testuser@example.com", password="password123")

        # Dummy tasvir yaratamiz
        self.test_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\xff\x00\x00\x00\x00\x00\xff\xff\xff\x21\xf9\x04\x01\x00\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x4c\x01\x00\x3b',
            content_type='image/jpeg'
        )

        # News modeli uchun test ma'lumotlarini yaratamiz
        self.news = News.objects.create(
            user=self.user,
            title="Test News Title",
            img=self.test_image
        )

    def test_news_creation(self):
        # News modeli to'g'ri yaratilganligini tekshirish
        self.assertEqual(self.news.user.email, "testuser@example.com")
        self.assertEqual(self.news.title, "Test News Title")
        self.assertIsNotNone(self.news.created_at)
        self.assertTrue(self.news.img.name.startswith("test_image"))

    def test_str_method(self):
        # __str__ metodi to'g'ri ishlayotganligini tekshirish
        self.assertEqual(str(self.news), "Test News Title")
