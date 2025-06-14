%# views/reports.tpl
% rebase('base.tpl', title='Reports', load_base_style=True, current_year=current_year)

<div class="report-container">
    <h2>Spending by Category (This Month)</h2>
    <div class="chart-box">
        <canvas id="categoryPieChart"></canvas>
    </div>
</div>

<style>
    .report-container { max-width: 800px; margin: 20px auto; }
    .chart-box { padding: 20px; border: 1px solid #ddd; border-radius: 5px; background: #fff; }
</style>

<script>
    // This script runs after the page loads
    document.addEventListener('DOMContentLoaded', function() {
        // Use the modern 'fetch' API to get data from our new API route
        fetch('/api/spending-by-category')
            .then(response => response.json())
            .then(chartData => {
                // We have the data, now create the chart
                const ctx = document.getElementById('categoryPieChart').getContext('2d');

                new Chart(ctx, {
                    type: 'pie', // The type of chart we want
                    data: {
                        labels: chartData.labels, // The category names from our API
                        datasets: [{
                            label: 'Spending',
                            data: chartData.data, // The spending amounts from our API
                            backgroundColor: [ // Add some default colors
                                'rgba(255, 99, 132, 0.8)',
                                'rgba(54, 162, 235, 0.8)',
                                'rgba(255, 206, 86, 0.8)',
                                'rgba(75, 192, 192, 0.8)',
                                'rgba(153, 102, 255, 0.8)',
                                'rgba(255, 159, 64, 0.8)',
                                'rgba(199, 199, 199, 0.8)',
                                'rgba(83, 102, 255, 0.8)',
                                'rgba(255, 99, 255, 0.8)'
                            ],
                            borderColor: 'rgba(255, 255, 255, 1)',
                            borderWidth: 2
                        }]
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            legend: {
                                position: 'top',
                            },
                            title: {
                                display: true,
                                text: 'Spending by Category'
                            }
                        }
                    }
                });
            })
            .catch(error => {
                console.error('Error fetching chart data:', error);
                // Optionally display an error message on the page
            });
    });
</script>