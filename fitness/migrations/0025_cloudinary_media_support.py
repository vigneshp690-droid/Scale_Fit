from django.db import migrations, models


try:
    import cloudinary.models
except ImportError:
    cloudinary = None


def optional_cloudinary_field(resource_type='image', folder='', **kwargs):
    if cloudinary:
        return cloudinary.models.CloudinaryField(resource_type=resource_type, folder=folder, **kwargs)
    return models.FileField(**kwargs)


class Migration(migrations.Migration):

    dependencies = [
        ('fitness', '0024_seed_meal_macro_nutrition'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitesettings',
            name='favicon',
            field=models.ImageField(blank=True, null=True, upload_to='cloudinary/site_settings/'),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='site_logo',
            field=models.ImageField(blank=True, null=True, upload_to='cloudinary/site_settings/'),
        ),
        migrations.AlterField(
            model_name='programitem',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='cloudinary/program_images/'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to='cloudinary/profile_images/'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='trainer_image',
            field=optional_cloudinary_field(blank=True, folder='cloudinary/trainer_images', max_length=255, null=True, resource_type='image', verbose_name='trainer_image'),
        ),
        migrations.AlterField(
            model_name='workoutitem',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='cloudinary/workout_images/'),
        ),
        migrations.AddField(
            model_name='workoutitem',
            name='video',
            field=optional_cloudinary_field(blank=True, folder='cloudinary/workout_videos', max_length=255, null=True, resource_type='video', verbose_name='video'),
        ),
    ]
