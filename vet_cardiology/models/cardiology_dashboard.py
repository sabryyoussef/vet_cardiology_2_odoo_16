from odoo import models, fields, api
import json
from datetime import datetime, timedelta

class CardiologyDashboard(models.Model):
    _name = 'cardiology.dashboard'
    _description = 'Cardiology Dashboard'

    total_cases = fields.Integer(compute='_compute_cases')
    cases_trend = fields.Char(compute='_compute_cases')
    case_status_chart = fields.Char(compute='_compute_case_status_chart')
    monthly_trends_chart = fields.Char(compute='_compute_monthly_trends')
    arrhythmia_chart = fields.Char(compute='_compute_arrhythmia_chart')
    ecg_findings_chart = fields.Char(compute='_compute_ecg_findings_chart')

    def _get_chart_data(self):
        # This is a helper method to get chart colors
        return {
            'colors': ['#36A2EB', '#FFCE56', '#4BC0C0', '#FF6384', '#9966FF'],
            'chart_type': {
                'bar': {
                    'type': 'bar',
                    'options': {
                        'responsive': True,
                        'scales': {
                            'y': {'beginAtZero': True}
                        }
                    }
                },
                'pie': {
                    'type': 'pie',
                    'options': {
                        'responsive': True
                    }
                }
            }
        }

    @api.depends('case_status_chart')
    def _compute_case_status_chart(self):
        for record in self:
            chart_data = {
                'type': 'pie',  # Specify chart type
                'data': {
                    'labels': ['New', 'In Progress', 'Completed', 'Cancelled'],
                    'datasets': [{
                        'data': [30, 50, 100, 20],
                        'backgroundColor': self._get_chart_data()['colors']
                    }]
                },
                'options': {
                    'responsive': True,
                    'plugins': {
                        'legend': {
                            'position': 'bottom'
                        }
                    }
                }
            }
            record.case_status_chart = json.dumps(chart_data)

    @api.depends('monthly_trends_chart')
    def _compute_monthly_trends(self):
        for record in self:
            chart_data = {
                'type': 'bar',
                'data': {
                    'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                    'datasets': [{
                        'label': 'Number of Cases',
                        'data': [65, 59, 80, 81, 56, 55],
                        'backgroundColor': self._get_chart_data()['colors'][0],
                        'borderColor': self._get_chart_data()['colors'][0],
                        'borderWidth': 1
                    }]
                },
                'options': {
                    'responsive': True,
                    'scales': {
                        'y': {
                            'beginAtZero': True
                        }
                    }
                }
            }
            record.monthly_trends_chart = json.dumps(chart_data)

    @api.depends('arrhythmia_chart')
    def _compute_arrhythmia_chart(self):
        for record in self:
            chart_data = {
                'type': 'doughnut',
                'data': {
                    'labels': ['Normal', 'Mild', 'Moderate', 'Severe'],
                    'datasets': [{
                        'data': [45, 25, 20, 10],
                        'backgroundColor': self._get_chart_data()['colors']
                    }]
                },
                'options': {
                    'responsive': True,
                    'plugins': {
                        'legend': {
                            'position': 'bottom'
                        }
                    }
                }
            }
            record.arrhythmia_chart = json.dumps(chart_data)

    @api.depends('ecg_findings_chart')
    def _compute_ecg_findings_chart(self):
        for record in self:
            chart_data = {
                'type': 'line',
                'data': {
                    'labels': ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
                    'datasets': [
                        {
                            'label': 'Normal ECG',
                            'data': [12, 19, 3, 5],
                            'borderColor': self._get_chart_data()['colors'][0],
                            'fill': False,
                            'tension': 0.1
                        },
                        {
                            'label': 'Abnormal ECG',
                            'data': [3, 5, 2, 3],
                            'borderColor': self._get_chart_data()['colors'][3],
                            'fill': False,
                            'tension': 0.1
                        }
                    ]
                },
                'options': {
                    'responsive': True,
                    'scales': {
                        'y': {
                            'beginAtZero': True
                        }
                    }
                }
            }
            record.ecg_findings_chart = json.dumps(chart_data)

    @api.depends('total_cases')
    def _compute_cases(self):
        for record in self:
            # For now, using static data
            record.total_cases = 156
            record.cases_trend = "+12" 