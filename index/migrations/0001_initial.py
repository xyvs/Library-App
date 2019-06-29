# Generated by Django 2.2.2 on 2019-06-29 18:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('image', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('isbn', models.CharField(max_length=100)),
                ('goodreads_id', models.PositiveIntegerField()),
                ('image', models.URLField()),
                ('description', models.TextField(blank=True, null=True)),
                ('release_date', models.DateField(blank=True, null=True)),
                ('publisher', models.CharField(max_length=100)),
                ('language_code', models.CharField(max_length=3)),
                ('number_of_pages', models.PositiveIntegerField()),
                ('format_of_release', models.CharField(max_length=100)),
                ('category', models.CharField(blank=True, choices=[('biography ', 'Biography'), ('classic', 'Classic'), ('comics', 'Comics/Graphic novel'), ('crime', 'Crime/detective'), ('essay ', 'Essay'), ('fable', 'Fable'), ('fairy-tailr', 'Fairy tale'), ('fan-fiction', 'Fan fiction'), ('fantasy', 'Fantasy'), ('folklore', 'Folklore'), ('historical-fiction', 'Historical fiction'), ('horror', 'Horror'), ('humor', 'Humor'), ('journalism', 'Journalism'), ('lab-report ', 'Lab report'), ('legend', 'Legend'), ('magical-realism', 'Magical realism'), ('manual', "Owner's manual"), ('memoir', 'Memoir'), ('meta-fiction', 'Meta fiction'), ('mystery', 'Mystery'), ('mythology', 'Mythology'), ('mythopoeia', 'Mythopoeia'), ('narrative-nonfiction', 'Narrative nonfiction/personal narrative'), ('picture-book', 'Picture book'), ('realistic-fiction', 'Realistic fiction'), ('reference', 'Reference book'), ('science-fiction', 'Science fiction'), ('self-help', 'Self-help book'), ('short-story', 'Short story'), ('speech', 'Speech'), ('suspense', 'Suspense/thriller'), ('swashbuckler', 'Swashbuckler'), ('tall-tale', 'Tall tale'), ('textbook ', 'Textbook'), ('western', 'Western')], max_length=100)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_edited', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-date_added'],
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True, max_length=500)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('rents_available', models.PositiveIntegerField(default=2)),
                ('active', models.BooleanField(default=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_number', models.PositiveIntegerField()),
                ('address', models.CharField(max_length=100)),
                ('number', models.PositiveIntegerField()),
                ('locations', models.CharField(max_length=250)),
                ('cp', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Serie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.URLField()),
                ('description', models.TextField()),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_edited', models.DateTimeField(auto_now=True)),
                ('books', models.ManyToManyField(related_name='series', to='index.Book')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100)),
                ('review', models.TextField()),
                ('liked', models.BooleanField()),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='index.Book')),
                ('likes', models.ManyToManyField(blank=True, related_name='reviews_liked', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='index.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('isbn', models.CharField(max_length=100)),
                ('goodreads_id', models.PositiveIntegerField()),
                ('image', models.URLField()),
                ('description', models.TextField(blank=True, null=True)),
                ('release_date', models.DateField(blank=True, null=True)),
                ('publisher', models.CharField(max_length=100)),
                ('language_code', models.CharField(max_length=3)),
                ('number_of_pages', models.PositiveIntegerField()),
                ('format_of_release', models.CharField(max_length=100)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('author', models.ManyToManyField(blank=True, to='index.Author')),
                ('requested_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requests', to='index.Profile')),
            ],
            options={
                'ordering': ['-date_added'],
            },
        ),
        migrations.CreateModel(
            name='Rent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('date_rented', models.DateField(auto_now_add=True)),
                ('returned', models.BooleanField(default=False)),
                ('returned_date', models.DateField(blank=True, null=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='index.Book')),
                ('returned_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='index.Profile')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rents', to='index.Profile')),
            ],
            options={
                'ordering': ['-date_rented', '-pk'],
            },
        ),
        migrations.AddField(
            model_name='profile',
            name='user_details',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='index.UserDetails'),
        ),
        migrations.CreateModel(
            name='New',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('image', models.URLField()),
                ('body', models.TextField()),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_edited', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='index.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.URLField()),
                ('description', models.TextField()),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_edited', models.DateTimeField(auto_now=True)),
                ('books', models.ManyToManyField(related_name='collections', to='index.Book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='collections', to='index.Profile')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='book',
            name='added_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='books_added', to='index.Profile'),
        ),
        migrations.AddField(
            model_name='book',
            name='author',
            field=models.ManyToManyField(blank=True, to='index.Author'),
        ),
        migrations.AddField(
            model_name='book',
            name='bookmarks',
            field=models.ManyToManyField(blank=True, related_name='bookmarks', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='book',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
