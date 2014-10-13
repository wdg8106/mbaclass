import os, datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings
from member.models import Member

class Command(BaseCommand):
    help = 'Import Member Info'

    def handle(self, *args, **options):
        fname = os.path.join(settings.BASE_DIR, 'etc/4class.csv')
        lines = file(fname).readlines()[1:2]
        now = timezone.now()
        for line in lines:
            l = line.split(',')
            try:
                Member.objects.get(number=l[0])
            except Exception:
                member = Member(username=l[1], email=l[3], classnum=4, number=l[0], weixin='xx', mobile=l[2], \
                  birthday=datetime.date.today(), gender='m',is_active=True,
                          is_superuser=False, last_login=now)
                member.set_password('123')
                member.save()
                print 'create %s' % l[1]