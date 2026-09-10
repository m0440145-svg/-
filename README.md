# منصة مراسلات - Django/PostgreSQL

نظام جمعية الإحسان لإدارة الصادر والوارد. إعداد الإنتاج يعتمد Django 5.2 وPostgreSQL وجلسات داخلية وصلاحيات خادمية.

## تشغيل محلي للاختبار

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
USE_SQLITE_FOR_TESTS=1 .venv/bin/python backend/manage.py migrate
USE_SQLITE_FOR_TESTS=1 .venv/bin/python backend/manage.py loaddata departments
USE_SQLITE_FOR_TESTS=1 DJANGO_DEBUG=1 .venv/bin/python backend/manage.py runserver
```

## نشر Ubuntu وPostgreSQL

1. أنشئ مستخدمًا وقاعدة PostgreSQL بترميز UTF-8.
2. انسخ المشروع إلى `/srv/morasalat` وأنشئ البيئة الافتراضية وثبت `requirements.txt`.
3. انسخ `.env.example` إلى `.env` وغيّر السر وكلمة مرور قاعدة البيانات والنطاق.
4. نفذ `.venv/bin/python backend/manage.py migrate` ثم `loaddata departments` و`collectstatic`.
5. أنشئ المدير بأمر `createsuperuser`، ثم اضبط دوره وقسمه من Django Admin. لا تستخدم كلمة مرور افتراضية منشورة.
6. ضع مجلد المرفقات خارج جذر الويب واضبطه للقراءة والكتابة بواسطة `www-data`.
7. ثبت ملفي `deploy/morasalat.service` و`deploy/nginx.conf` ثم فعّل HTTPS.
8. فعّل نسخًا يومية مشفرة عبر `pg_dump` واختبر الاستعادة دوريًا.

## التحقق

```bash
USE_SQLITE_FOR_TESTS=1 .venv/bin/python backend/manage.py check
USE_SQLITE_FOR_TESTS=1 .venv/bin/python backend/manage.py test
```

قبل الإنتاج يجب تشغيل مجموعة الاختبارات نفسها على PostgreSQL فعلي، وفحص السجلات، وضبط النسخ الاحتياطي وHTTPS. قاعدة الاختبار المحلية لا تعد بديلًا عن اختبار PostgreSQL.
