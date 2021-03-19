from django.db import models
import json
from django.db.models.signals import post_save, pre_save

from django_celery_beat.models import (
    CrontabSchedule,  # IntervalSchedule
    PeriodicTask,
    PeriodicTasks,
)

from .my_celery.tasks import perform_scrape, company_granular_price_scrape_task

STOCK_MARKET_LOOKUP_SOURCES = (
    ('finnhub', 'Finnhub API'),
)


class Stock(models.Model):
    periodic_task = models.ForeignKey(PeriodicTask, null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=220)
    ticker = models.CharField(max_length=20)
    description = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    scraping_scheduler_enabled = models.BooleanField(default=False)
    has_granular_scraping = models.BooleanField(default=False)
    one_off_scrape = models.BooleanField(default=False)

    # default_service
    # events per minute

    def scrape(self):
        return company_granular_price_scrape_task.delay(self.id, service='finnhub') #Непонятно что

    def enable_periodic_task(self, save=True):
        instance_id = self.id
        ticker = self.ticker
        task_name = f'company-{ticker}-{instance_id}'.lower()
        if not self.periodic_task:
            schedule, _ = CrontabSchedule.objects.get_or_create(minute='*', hour='*', day_of_week='*', day_of_month='*', month_of_year='*')
            obj, _ = PeriodicTask.objects.get_or_create(
                crontab=schedule,
                kwargs=json.dumps({
                    'instance_id': instance_id,
                    'service': 'finnhub'
                }),
                name=task_name,
                task='stocks.tasks.company_granular_price_scrape_task'
            )
            obj.enabled = True
            obj.save()
            PeriodicTasks.update_changed()
            self.periodic_task = obj
            if save:
                self.save()
        return self.periodic_task

    def disable_periodic_task(self, save=True):
        if self.periodic_task:
            obj = self.periodic_task
            obj.delete()
            PeriodicTasks.update_changed()
            self.periodic_task = None
            if save:
                self.save()
        return self.periodic_task

    def __str__(self):
        return f"{self.name} ({self.ticker})"

    class Meta:
        ordering = ['name']
        verbose_name = 'Stock'
        verbose_name_plural = 'Stocks'


def company_pre_save(sender, instance, *args, **kwargs):
    if instance.id:
        if instance.one_off_scrape:
            instance.one_off_scrape = False
            instance.scrape()
        if instance.scraping_scheduler_enabled and not instance.periodic_task:
            instance.enable_periodic_task(save=False)
        if instance.scraping_scheduler_enabled is False and instance.periodic_task:
            instance.disable_periodic_task(save=False)


pre_save.connect(company_pre_save, sender=Stock)


def company_post_save(sender, instance, created, *args, **kwargs):
    if created:
        if instance.scraping_scheduler_enabled and not instance.periodic_task:
            instance.enable_periodic_task(save=True)


post_save.connect(company_post_save, sender=Stock)


class PriceLookupEventManager(models.Manager):
    def create_event(self, ticker, pc):
        try:
            company_obj = Stock.objects.get(ticker__iexact=ticker)
        except Stock.DoesNotExist:
            # log issue
            company_obj = None
        except:
            company_obj = None
        obj = self.model(ticker=ticker, pc=pc)
        obj.company = company_obj
        obj.save()
        return obj


class PriceLookupEvent(models.Model):
    ticker = models.CharField(max_length=20)
    pc = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    source = models.CharField(max_length=50, choices=STOCK_MARKET_LOOKUP_SOURCES, default='finnhub')
    objects = PriceLookupEventManager()
