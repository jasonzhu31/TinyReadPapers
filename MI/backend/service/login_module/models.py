from django.db import models
import os

def user_directory_path(instance, filename):
    ext = filename.split('.').pop()
    filename = '{0}_picture.{1}'.format(instance.usr_id, ext)
    return os.path.join(instance.usr_id, filename) # 系统路径分隔符差异，增强代码重用性

# Create your models here.
class usr_info(models.Model):
    username = models.CharField('用户id',max_length=20, unique=True)
    email = models.EmailField('用户邮箱', null=True, unique=True)
    password = models.CharField('用户密码', max_length=256)
    last_path = models.CharField('上一次打开文件', max_length=1024, default='')


class ConfirmString(models.Model):
    code = models.CharField(max_length=256, verbose_name='confirm code')
    usr_email = models.EmailField('用户邮箱', null=True,unique=True)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.usr_email + ': ' + self.code

    class Meta:
        ordering = ['-created_time']
        verbose_name = 'Confirm Code'
        verbose_name_plural = 'Confirm Codes'
