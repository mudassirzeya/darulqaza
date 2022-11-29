from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):
    USERTYPE = (
        ('law', 'law'),
        ('admin', 'admin'),
    )
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE
    )
    profile_pic = models.ImageField(
        default="profile1.jpg", null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    password = models.CharField(max_length=20, null=True, blank=True)
    user_type = models.CharField(max_length=100, blank=True, choices=USERTYPE)
    date_of_joining = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)


class Court(models.Model):
    court_name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self) -> str:
        return self.court_name


class CaseType(models.Model):
    case_type = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self) -> str:
        return self.case_type


class Judge(models.Model):
    user = models.ForeignKey(
        UserProfile, null=True, blank=True, on_delete=models.CASCADE)
    court = models.ManyToManyField(
        Court, blank=True)
    added_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self) -> str:
        return self.user.user.get_full_name()


class Case(models.Model):
    CASESTATUS = (
        ('اندراج معاملہ', 'اندراج معاملہ'),
        ('اطلاع اول بنام فریق دوم مع مثنی  درخواست فریق اول',
         'اطلاع اول بنام فریق دوم مع مثنی  درخواست فریق اول'),
        ('فریق دوم  کو اطلاع موصول ہوئی', 'فریق دوم  کو اطلاع موصول ہوئی'),
        ('فریق دوم کو اطلاع موصول نہیں ہوئی',
         'فریق دوم کو اطلاع موصول نہیں ہوئی'),
        ('ادخال بیان تحریری من جانب فریق ثانی',
         'ادخال بیان تحریری من جانب فریق ثانی'),
        ('اطلاع بنام فریق اول برائے طلبی پتہ فریق دوم و  متعلقین ومعززین فریق دوم',
         'اطلاع بنام فریق اول برائے طلبی پتہ فریق دوم و  متعلقین ومعززین فریق دوم'),
        ('اطلاع ثانی بنام فریق دوم / متعلقین  و معززین فریق دوم مع مثنی درخواست',
         'اطلاع ثانی بنام فریق دوم / متعلقین  و معززین فریق دوم مع مثنی درخواست'),
        ('تاریخ سماعت اول', 'تاریخ سماعت اول'),
        ('حاضری فریقین مع گواہان  و اندراج بیانات',
         'حاضری فریقین مع گواہان  و اندراج بیانات'),
        ('حاضری فریق اول فقط مع گواہان واندراج بیانات',
         'حاضری فریق اول فقط مع گواہان واندراج بیانات'),
        ('حاضری فریق دوم فقط مع گواہا ن و اندراج بیانات',
         'حاضری فریق دوم فقط مع گواہا ن و اندراج بیانات'),
        ('ا طلاع ثالث بنام فریق دوم', 'ا طلاع ثالث بنام فریق دوم'),
        ('اشتہار مفقود الخبر ی در اخبار نقیب',
         'اشتہار مفقود الخبر ی در اخبار نقیب'),
        ('تاریخ سماعت دوم', 'تاریخ سماعت دوم'),
        ('حاضری فریقین مع گواہان  و اندراج بیانات',
         'حاضری فریقین مع گواہان  و اندراج بیانات'),
        ('حاضری فریق اول فقط مع گواہان واندراج بیانات',
         'حاضری فریق اول فقط مع گواہان واندراج بیانات'),
        ('حاضری فریق دوم فقط مع گواہا ن و اندراج بیانات',
         'حاضری فریق دوم فقط مع گواہا ن و اندراج بیانات'),
        ('تاریخ سماعت سوم', 'تاریخ سماعت سوم'),
        ('حاضری فریقین مع گواہان  و اندراج بیانات',
         'حاضری فریقین مع گواہان  و اندراج بیانات'),
        ('حاضری فریق اول فقط مع گواہان واندراج بیانات',
         'حاضری فریق اول فقط مع گواہان واندراج بیانات'),
        ('حاضری فریق دوم فقط مع گواہا ن و اندراج بیانات',
         'حاضری فریق دوم فقط مع گواہا ن و اندراج بیانات'),
        ('تصفیہ', 'تصفیہ'),
        ('خارج بلا تجویز', 'خارج بلا تجویز'),
        ('مصالحت بذریعہ  خلع/ طلاق/ رخصتی', 'مصالحت بذریعہ  خلع/ طلاق/ رخصتی'),
        ('آخری حکم', 'آخری حکم'),
        ('ارسال مثل مرکزی دار القضاء', 'ارسال مثل مرکزی دار القضاء')
    )
    judge = models.ForeignKey(
        Judge, null=True, blank=True, on_delete=models.CASCADE)
    case_type = models.ForeignKey(
        CaseType, null=True, blank=True, on_delete=models.SET_NULL
    )
    court = models.ForeignKey(
        Court, null=True, blank=True, on_delete=models.SET_NULL)
    case_num = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateField(auto_now_add=False, null=True, blank=True)
    accused = models.TextField(null=True, blank=True)
    plaintiff = models.TextField(null=True, blank=True)
    aditional_text = models.TextField(null=True, blank=True)
    status = models.CharField(
        max_length=100, null=True, blank=True, choices=CASESTATUS)
    added_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)


class TimeLine(models.Model):
    user = models.ForeignKey(
        UserProfile, null=True, blank=True, on_delete=models.CASCADE)
    case = models.ForeignKey(
        Case, null=True, blank=True, on_delete=models.CASCADE)
    aditional_text = models.TextField(null=True, blank=True)
    added_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
