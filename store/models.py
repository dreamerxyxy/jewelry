from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Address(models.Model):
    user = models.ForeignKey(User, verbose_name="Kulllanıcı Adı", on_delete=models.CASCADE)
    locality = models.CharField(max_length=150, verbose_name="En Yakın Konum")
    city = models.CharField(max_length=150, verbose_name="Şehir")
    state = models.CharField(max_length=150, verbose_name="Durum")

    def __str__(self):
        return self.locality


class Category(models.Model):
    title = models.CharField(max_length=50, verbose_name="Kategori Başlığı")
    slug = models.SlugField(max_length=55, verbose_name="Kategori Bilgisi")
    description = models.TextField(blank=True, verbose_name=" Kategori Tanımı")
    category_image = models.ImageField(upload_to='category', blank=True, null=True, verbose_name=" Kategori Resmi")
    is_active = models.BooleanField(verbose_name="Aktif ?")
    is_featured = models.BooleanField(verbose_name="Özellikli ?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncelleme Tarihi")

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ('-created_at',)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = u"Kategoriler"
        verbose_name = u"Kategori"


class Product(models.Model):
    title = models.CharField(max_length=150, verbose_name="Ürün başlığı")
    slug = models.SlugField(max_length=160, verbose_name=" Ürün Bilgisi")
    sku = models.CharField(max_length=255, unique=True, verbose_name="Benzersiz Ürün Kimliği (BÜK)")
    short_description = models.TextField(verbose_name="Kısa Açıklama")
    detail_description = models.TextField(blank=True, null=True, verbose_name="Detay Açıklama")
    product_image = models.ImageField(upload_to='product', blank=True, null=True, verbose_name="Ürün Resmi")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Fiyatı")
    category = models.ForeignKey(Category, verbose_name="Ürün Kategorisi", on_delete=models.CASCADE)
    is_active = models.BooleanField(verbose_name="Aktif mi ?")
    is_featured = models.BooleanField(verbose_name="Özellikli mi ?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncelleme Tarihi")

    class Meta:
        verbose_name_plural = 'Products'
        ordering = ('-created_at',)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = u"Ürünler"
        verbose_name = u"Ürün"


class Cart(models.Model):
    user = models.ForeignKey(User, verbose_name="Kullanıcı Adı", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name="Ürün Adı", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, verbose_name="Miktar")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncelleme Tarihi")

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name_plural = u"Sepetler"
        verbose_name = u"Sepet"

    # Creating Model Property to calculate Quantity x Price
    @property
    def total_price(self):
        return self.quantity * self.product.price


STATUS_CHOICES = (
    ('Pending', 'Askıda'),
    ('Accepted', 'Sipariş Alınmış'),
    ('Packed', 'Paketlendi'),
    ('On The Way', 'Yolda'),
    ('Delivered', 'Teslim Edilmiş'),
    ('Cancelled', 'İptal')
)


class Order(models.Model):
    user = models.ForeignKey(User, verbose_name="Kullanıcı Adı", on_delete=models.CASCADE)
    address = models.ForeignKey(Address, verbose_name="Ev Adresi", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name="Ürün Adı", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name="Miktar")
    ordered_date = models.DateTimeField(auto_now_add=True, verbose_name="Sipariş Tarihi")
    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=50,
        default="Pending"
    )

    class Meta:
        verbose_name_plural = u"Siparişler"
        verbose_name = u"Sipariş"


DEFAULT_STATUS = 'draft'
STATUS = [
    ('draft', 'Taslak'),
    ('published', 'Yayınlandı'),
    ('deleted', 'Silindi'),
]


class Carousel(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    subtitle = models.CharField(max_length=200, blank=True, null=True)
    cover_image = models.ImageField(
        upload_to='carousel',
        null=True,
        blank=True,
    )
    status = models.CharField(
        default=DEFAULT_STATUS,
        choices=STATUS,
        max_length=10
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = u"Karsilamalar"
        verbose_name = u"Karsilama"


class Subscribe(models.Model):
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural = u"Abonelikler"
        verbose_name = u"Abonelik"
