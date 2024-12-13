/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component, onMounted, useRef } from "@odoo/owl";

export class CardiologyDashboard extends Component {
    setup() {
        this.orm = useService("orm");
        onMounted(() => this.initializeChart());
    }

    async initializeChart() {
        const ctx = document.getElementById('mainChart').getContext('2d');
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Treated', 'In Progress', 'Critical', 'New'],
                datasets: [{
                    data: [45, 25, 15, 15],
                    backgroundColor: [
                        '#28a745',
                        '#ffc107',
                        '#dc3545',
                        '#17a2b8'
                    ],
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'right',
                    }
                }
            }
        });
    }
}

CardiologyDashboard.template = 'cardiology_sc.Dashboard';
registry.category("actions").add("cardiology_dashboard", CardiologyDashboard);