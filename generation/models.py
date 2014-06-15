from django.db import models

from generation import settings

class Prime(models.Model):
    value = models.BigIntegerField(null=False, blank=False, unique=True)

    class Meta:
        get_latest_by = "value"
        ordering = ["value"]

    def __str__(self):
        return 'id=%s, value=%s' % (self.id, self.value)

    @staticmethod
    def get_values():
        return [p["value"] for p in Prime.objects.all().values('value')]

    @staticmethod
    def get(index):
        try:
            return Prime.objects.all()[index-1].value
        except IndexError:
            return None


class MaxIndex(models.Model):
    index = models.BigIntegerField(blank=False, null=False)
    dt = models.DateTimeField(auto_now=True)

    class Meta:
        get_latest_by = "dt"
        ordering = ["dt"]

    @staticmethod
    def update():
        primes = Prime.objects.all()
        if not primes:
            index = -1
        else:
            min_not_ready_status = GeneratorStatus.objects.filter(status=False)
            if min_not_ready_status:
                min_value = min_not_ready_status[0].min_value
                if min_value > 0:
                    index = Prime.objects.filter(value__lte=min_value).count()
                else:
                    index = -1
            else:
                index = primes.count()
        mi = MaxIndex.objects.create(index=index)
        mi.save()
        return mi

    @staticmethod
    def get():
        return MaxIndex.objects.latest()

    def __str__(self):
        return 'date: %s, count: %s' % (self.dt.strftime("%b %d %Y %H:%M:%S"),
                                     self.index)


class GeneratorStatus(models.Model):
    min_value = models.BigIntegerField(null=False, blank=False, unique=True)
    task_id = models.CharField(max_length = 50, blank=True, null=True)
    status = models.BooleanField(default=False)

    class Meta:
        get_latest_by = "min_value"
        ordering = ["min_value"]

    def __str__(self):
        return '[%i, %i]%s%s' % (
            self.min_value, self.min_value + settings.INTERVAL_LENGTH,
            ': DONE' if self.status else '', ', TASKED' if self.task_id else '')
