document.addEventListener("DOMContentLoaded", function () {
    function getBrandColor() {
        const computedStyle = getComputedStyle(document.documentElement);
        return computedStyle.getPropertyValue("--color-primary-600").trim()
            || computedStyle.getPropertyValue("--color-fg-brand").trim()
            || "#0a947c";
    }

    function getChartTheme() {
        return document.documentElement.classList.contains("dark") ? "dark" : "light";
    }

    function getChartTextColor() {
        return getChartTheme() === "dark" ? "#e2e8f0" : "#334155";
    }

    function parseJsonScript(id, fallback) {
        const element = document.getElementById(id);
        if (!element) {
            return fallback;
        }

        try {
            return JSON.parse(element.textContent);
        } catch (error) {
            return fallback;
        }
    }

    function renderAppointmentChart() {
        const chartEl = document.getElementById("appointment-column-chart");

        if (!chartEl || typeof ApexCharts === "undefined") {
            return;
        }

        if (chartEl.dataset.rendered === "true") {
            return;
        }

        const labels = parseJsonScript("appointment-chart-labels", []);
        const counts = parseJsonScript("appointment-chart-counts", []);
        const seriesData = labels.map(function (label, index) {
            return { x: label, y: counts[index] || 0 };
        });

        const options = {
            colors: [getBrandColor()],
            series: [
                {
                    name: "Appointments",
                    data: seriesData,
                },
            ],
            chart: {
                type: "bar",
                height: 320,
                fontFamily: "Inter, sans-serif",
                toolbar: { show: true },
                background: "transparent",
            },
            theme: {
                mode: getChartTheme(),
            },
            plotOptions: {
                bar: {
                    horizontal: false,
                    columnWidth: "50%",
                    borderRadius: 8,
                    borderRadiusApplication: "end",
                },
            },
            dataLabels: {
                enabled: true,
            },
            legend: {
                show: false,
            },
            xaxis: {
                type: "category",
                labels: {
                    style: {
                        colors: getChartTextColor(),
                    },
                },
                axisBorder: { show: false },
                axisTicks: { show: false },
            },
            yaxis: {
                show: true,
                min: 0,
                forceNiceScale: true,
                labels: {
                    style: {
                        colors: getChartTextColor(),
                    },
                },
            },
            grid: {
                show: false,
            },
            tooltip: {
                shared: true,
                intersect: false,
            },
            fill: {
                opacity: 1,
            },
        };

        const chart = new ApexCharts(chartEl, options);
        chart.render();
        chartEl.dataset.rendered = "true";
    }

    function renderStatusChart() {
        const chartEl = document.getElementById("appointment-status-chart");

        if (!chartEl || typeof ApexCharts === "undefined") {
            return;
        }

        if (chartEl.dataset.rendered === "true") {
            return;
        }

        const labels = parseJsonScript("status-chart-labels", []);
        const counts = parseJsonScript("status-chart-counts", []);

        const options = {
            colors: ["#0a947c", "#0ea5e9", "#22c55e", "#ef4444"],
            series: counts,
            labels: labels,
            chart: {
                type: "donut",
                height: 320,
                fontFamily: "Inter, sans-serif",
                background: "transparent",
            },
            theme: {
                mode: getChartTheme(),
            },
            dataLabels: {
                enabled: true,
            },
            legend: {
                position: "bottom",
                labels: {
                    colors: getChartTextColor(),
                },
            },
            plotOptions: {
                pie: {
                    donut: {
                        size: "65%",
                        labels: {
                            show: true,
                            total: {
                                show: true,
                                label: "Total",
                                color: getChartTextColor(),
                            },
                        },
                    },
                },
            },
            stroke: {
                width: 0,
            },
        };

        const chart = new ApexCharts(chartEl, options);
        chart.render();
        chartEl.dataset.rendered = "true";
    }

    renderAppointmentChart();
    renderStatusChart();

    document.body.addEventListener("htmx:afterSwap", function () {
        renderAppointmentChart();
        renderStatusChart();
    });
});
