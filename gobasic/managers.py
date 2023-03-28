from django.db import models
from django.db.models import Sum, Count, F, ExpressionWrapper, FloatField
from datetime import date


class TripManager(models.Manager):
    def booked_by_agent_in_month(self, agent, year, month):
        return self.filter(agent=agent, booked=True, entry_created__year=year, entry_created__month=month)

    def not_booked_by_agent_in_month(self, agent, year, month):
        return self.filter(agent=agent, booked=False, entry_created__year=year, entry_created__month=month)

    def total_booked_in_financial_year(self, year):
        start_date = date(year, 4, 1)
        end_date = date(year + 1, 3, 31)
        return self.filter(booked=True, entry_created__range=(start_date, end_date))

    def total_revenue_in_year(self, year):
        trips = self.total_booked_in_financial_year(year)
        return trips.aggregate(revenue=Sum('total_trip_cost'))['revenue']

    def agent_monthly_revenue_percentage(self, agent, year, month):
        agent_revenue = self.booked_by_agent_in_month(agent, year, month).aggregate(revenue=Sum('total_trip_cost'))['revenue']
        total_revenue = self.filter(booked=True, entry_created__year=year, entry_created__month=month).aggregate(revenue=Sum('total_trip_cost'))['revenue']
        if total_revenue:
            return (agent_revenue / total_revenue) * 100
        return 0

    def agent_yearly_revenue_percentage(self, agent, year):
        start_date = date(year, 4, 1)
        end_date = date(year + 1, 3, 31)
        agent_revenue = self.filter(agent=agent, booked=True, entry_created__range=(start_date, end_date)).aggregate(revenue=Sum('total_trip_cost'))['revenue']
        total_revenue = self.total_revenue_in_year(year)
        if total_revenue:
            return (agent_revenue / total_revenue) * 100
        return 0

