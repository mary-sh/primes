# -*- coding: utf-8 -*-
from __future__ import absolute_import

from celery import shared_task
from celery.result import AsyncResult
from django.core.exceptions import ObjectDoesNotExist

from utils.logger import log
from generation import settings
from generation.models import GeneratorStatus, MaxIndex
from generation.algorithm import generate_primes


@shared_task()
def controller():
    mp = MaxIndex.update()
    log('controller started, %s' % mp)
    gs = GeneratorStatus.objects.filter(status=False)
    not_ready_count = gs.count()
    for g in gs:
        state = AsyncResult(g.task_id).state
        if state != 'STARTED':
            log('%s in %s' % (g, state))
            generator.delay(g.min_value, True)
        else:
            log('%s is not finished yet!' % g)
    try:
        mn = max([gs.latest().min_value if gs else 0,
                  GeneratorStatus.objects.filter(
                      status=True).latest().min_value])
    except ObjectDoesNotExist:
        mn = -settings.INTERVAL_LENGTH

    for i in range(1, settings.MAX_GENERATORS_COUNT - not_ready_count + 1):
        generator.delay(mn + i * settings.INTERVAL_LENGTH, False)


@shared_task()
def generator(mn, force):
    mx, task_id = mn + settings.INTERVAL_LENGTH, generator.request.id
    gs, created = GeneratorStatus.objects.get_or_create(min_value=mn)
    if gs.status is True or (not force and gs.task_id != task_id):
        return
    gs.task_id = task_id
    gs.save()
    log("%s started" % gs)
    generate_primes(mn, mx)
    gs.status = True
    gs.save()
