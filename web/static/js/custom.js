Highcharts.setOptions({
    chart: {
        spacing: [5, 5, 5, 5],
        style: {
            fontFamily: '"Lato","Helvetica Neue",Helvetica,Arial,sans-serif'
        },
        plotOptions: {
            series: {
                states: {
                    hover: {
                        lineWidthPlus: 0
                    }
                }
            }
        },
        tooltip: {
            shadow: false
        },
    }
});

function submission_charts(id) {
    $.getJSON('/api?name=submission&id=' + id, function (data) {
        submission_polarity_chart(data);
        submission_subjectivity_chart(data);
        submission_activity_chart(data);
        submission_upvote_ratio_chart(data);
        submission_special_users_chart(data);
        submission_gilded_chart(data);
    }).always(function () {
        // hide loaders
        $('.loader').each(function () {
            $(this).hide();
        });
    }).fail(function (data, status, error) {
        $(".chart").append("<div class='error'><h5>An error occurred while loading this chart.</h5><p>Wait a moment, then try reloading the page.<br><i>(" + error + ")</i></p>");
    });
}

function submission_polarity_chart(data) {
    Highcharts.chart('submission_polarity_chart', {
        chart: {
            type: 'bar'
        },
        title: {
            text: "Polarity of this thread"
        },
        credits: {
            enabled: false
        },
        xAxis: {
            categories: ['Title', 'Comments'],
        },
        yAxis: {
            tickPositioner: function () {
                var maxDeviation = Math.round((Math.max(Math.abs(this.dataMax), Math.abs(this.dataMin)) + .05) * 10) / 10;
                var halfMaxDeviation = maxDeviation / 2;

                return [-maxDeviation, -halfMaxDeviation, 0, halfMaxDeviation, maxDeviation];
            },
            title: {
                text: null
            }
        },
        series: [{
            name: 'This post',
            data: data['polarity']['submission'],
            dataLabels: {
                enabled: true,
                color: '#FFFFFF',
                align: 'right',
                format: '{point.y:.4f}',
                style: {
                    fontSize: '13px'
                }
            }
        },
        {
            name: 'Subreddit avg.',
            data: data['polarity']['subreddit'],
            dataLabels: {
                enabled: true,
                color: '#FFFFFF',
                align: 'right',
                format: '{point.y:.4f}',
                style: {
                    fontSize: '13px'
                }
            }
        }
        ]
    });
}

function submission_subjectivity_chart(data) {
    Highcharts.chart('submission_subjectivity_chart', {
        chart: {
            type: 'bar'
        },
        title: {
            text: "Subjectivity of this thread"
        },
        credits: {
            enabled: false
        },
        xAxis: {
            categories: ['Title', 'Comments'],
        },
        yAxis: {
            tickPositioner: function () {
                var maxDeviation = Math.round((Math.max(Math.abs(this.dataMax), Math.abs(this.dataMin)) + .05) * 10) / 10;
                var halfMaxDeviation = maxDeviation / 2;

                return [0, halfMaxDeviation, maxDeviation];
            },
            title: {
                text: null
            }
        },
        series: [{
            name: 'This post',
            data: data['subjectivity']['submission'],
            dataLabels: {
                enabled: true,
                color: '#FFFFFF',
                align: 'right',
                format: '{point.y:.4f}',
                style: {
                    fontSize: '13px'
                }
            }
        },
        {
            name: 'Subreddit avg.',
            data: data['subjectivity']['subreddit'],
            dataLabels: {
                enabled: true,
                color: '#FFFFFF',
                align: 'right',
                format: '{point.y:.4f}',
                style: {
                    fontSize: '13px'
                }
            }
        }
        ]
    });
}

function submission_activity_chart(data) {
    Highcharts.chart('submission_activity_chart', {
        chart: {
            zoomType: 'x'
        },
        title: {
            text: null
        },
        credits: {
            enabled: false
        },
        tooltip: {
            shared: true
        },
        xAxis: {
            type: 'datetime',
            crosshair: true
        },
        yAxis: [{
            title: {
                text: 'Comments'
            }
        },
        {
            title: {
                text: 'Karma'
            },
            opposite: true
        }
        ],
        series: [{
            type: 'column',
            name: 'Comments',
            yAxis: 0,
            data: data['activity']['comments'],
            lineWidth: 4
        },
        {
            type: 'spline',
            name: 'Karma',
            yAxis: 1,
            data: data['activity']['scores'],
            lineWidth: 6,
            marker: {
                symbol: 'circle',
                radius: 4,
                lineColor: 'rgba(255, 255, 255, 1)',
                lineWidth: 1
            }
        }
        ],
        colors: [
            'rgba(47, 79, 79, 1)',
            'rgba(255, 69, 0, 1)'
        ]
    });
}

function submission_upvote_ratio_chart(data) {
    Highcharts.chart('submission_upvote_ratio_chart', {
        chart: {
            zoomType: 'x'
        },
        title: {
            text: "Upvote ratio over time"
        },
        credits: {
            enabled: false
        },
        xAxis: {
            type: 'datetime'
        },
        yAxis: {
            title: {
                text: 'Upvote ratio'
            },
            plotLines: [{
                color: 'rgba(47, 79, 79, 1)',
                dashStyle: 'dash',
                value: data['upvote_ratio']['average_upvote_ratio'],
                width: 2,
                label: {
                    text: 'Subreddit avg. = ' + data['upvote_ratio']['average_upvote_ratio'],
                    align: 'left',
                    x: +5
                },
                zIndex: 1
            }]
        },
        series: [{
            type: 'line',
            name: 'Upvote ratio',
            yAxis: 0,
            data: data['upvote_ratio']['upvote_ratios']
        },
        {
            // dummy series to force graph to include subreddit avg
            type: 'scatter',
            marker: {
                enabled: false
            },
            enableMouseTracking: false,
            showInLegend: false,
            data: [
                [data['upvote_ratio']['upvote_ratios'][0][0], data['upvote_ratio']['average_upvote_ratio']]
            ]
        }
        ],
        colors: [
            'rgba(255, 69, 0, 1)'
        ]
    });
}

function submission_special_users_chart(data) {
    Highcharts.chart('submission_special_users_chart', {
        chart: {
            type: 'column'
        },
        title: {
            text: "Special user presence"
        },
        credits: {
            enabled: false
        },
        xAxis: {
            categories: ['OP', 'Mod', 'Admin', 'Special'],
            title: {
                text: null
            }
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Comments',
            },
            labels: {
                overflow: 'justify'
            }
        },
        tooltip: {
            valueSuffix: ' comments'
        },
        series: [{
            name: "This post",
            data: data['special_users']['submission']
        },
        {
            name: "Subreddit avg.",
            data: data['special_users']['subreddit']
        }
        ],
        colors: [
            'rgba(255, 99, 132, 0.65)',
            'rgba(54, 162, 235, 0.65)'
        ]
    });
}

function submission_gilded_chart(data) {
    Highcharts.chart('submission_gilded_chart', {
        chart: {
            type: 'bar'
        },
        title: {
            text: "Coins given"
        },
        credits: {
            enabled: false
        },
        xAxis: {
            categories: ['Silver', 'Gold', 'Platinum'],
        },
        yAxis: {
            min: 0,
            title: {
                text: null
            }
        },
        series: [{
            name: "Submission",
            data: data['gilded']['submission'],
        },
        {
            name: "Comments",
            data: data['gilded']['comments']
        },
        {
            name: "Subreddit avg.",
            data: data['gilded']['subreddit']
        }
        ],
        colors: [
            'rgba(218, 165, 32, 0.65)',
            'rgba(160, 82, 45, 0.65)',
            'rgba(160, 45, 65, 0.65)'
        ]
    });
}

function subreddit_charts(id) {
    $.getJSON('/api?name=subreddit&id=' + id, function (data) {
        subreddit_activity_chart(data);
        subreddit_polarity_chart(data);
        subreddit_subjectivity_chart(data);
    }).always(function () {
        // hide loaders
        $('.loader').each(function () {
            $(this).hide();
        });
    }).fail(function (data, status, error) {
        $(".chart").append("<div class='error'><h5>An error occurred while loading this chart.</h5><p>Wait a moment, then try reloading the page.<br><i>(" + error + ")</i></p>");
    });
}

function subreddit_activity_chart(data) {
    Highcharts.chart('subreddit_activity_chart', {
        chart: {
            zoomType: 'x'
        },
        title: {
            text: null
        },
        credits: {
            enabled: false
        },
        tooltip: {
            shared: true
        },
        xAxis: {
            type: 'datetime',
            crosshair: true
        },
        yAxis: [{
            title: {
                text: 'Δ Comments (per day)'
            }
        },
        {
            title: {
                text: 'Δ Karma (per day)'
            },
            opposite: true
        }
        ],
        series: [{
            type: 'column',
            name: 'Δ Comments',
            yAxis: 0,
            data: data['activity']['comment_differentials']
        },
        {
            type: 'line',
            name: 'Δ Karma',
            yAxis: 1,
            data: data['activity']['score_differentials'],
            lineWidth: 6,
            marker: {
                symbol: 'circle',
                radius: 4,
                lineColor: 'rgba(255, 255, 255, 1)',
                lineWidth: 1
            }
        }
        ],
        colors: [
            'rgba(47, 79, 79, 1)',
            'rgba(255, 69, 0, 1)'
        ]
    });
}

function subreddit_polarity_chart(data) {
    Highcharts.chart('subreddit_polarity_chart', {
        chart: {
            type: 'bar'
        },
        title: {
            text: "Polarity of this subreddit"
        },
        credits: {
            enabled: false
        },
        xAxis: {
            categories: ['Title', 'Comments'],
        },
        yAxis: {
            tickPositioner: function () {
                var maxDeviation = Math.round((Math.max(Math.abs(this.dataMax), Math.abs(this.dataMin)) + .05) * 10) / 10;
                var halfMaxDeviation = maxDeviation / 2;

                return [-maxDeviation, -halfMaxDeviation, 0, halfMaxDeviation, maxDeviation];
            },
            title: {
                text: null
            }
        },
        series: [{
            name: 'This subreddit',
            data: data['polarity']['subreddit'],
            dataLabels: {
                enabled: true,
                color: '#FFFFFF',
                align: 'right',
                format: '{point.y:.4f}',
                style: {
                    fontSize: '13px'
                }
            }
        },
        {
            name: 'Overall avg.',
            data: data['polarity']['overall'],
            dataLabels: {
                enabled: true,
                color: '#FFFFFF',
                align: 'right',
                format: '{point.y:.4f}',
                style: {
                    fontSize: '13px'
                }
            }
        }
        ]
    });
}

function subreddit_subjectivity_chart(data) {
    Highcharts.chart('subreddit_subjectivity_chart', {
        chart: {
            type: 'bar'
        },
        title: {
            text: "Subjectivity of this subreddit"
        },
        credits: {
            enabled: false
        },
        xAxis: {
            categories: ['Title', 'Comments'],
        },
        yAxis: {
            tickPositioner: function () {
                var maxDeviation = Math.round((Math.max(Math.abs(this.dataMax), Math.abs(this.dataMin)) + .05) * 10) / 10;
                var halfMaxDeviation = maxDeviation / 2;

                return [0, halfMaxDeviation, maxDeviation];
            },
            title: {
                text: null
            }
        },
        series: [{
            name: 'This subreddit',
            data: data['subjectivity']['subreddit'],
            dataLabels: {
                enabled: true,
                color: '#FFFFFF',
                align: 'right',
                format: '{point.y:.4f}',
                style: {
                    fontSize: '13px'
                }
            }
        },
        {
            name: 'Overall avg.',
            data: data['subjectivity']['overall'],
            dataLabels: {
                enabled: true,
                color: '#FFFFFF',
                align: 'right',
                format: '{point.y:.4f}',
                style: {
                    fontSize: '13px'
                }
            }
        }
        ]
    });
}

function cumulative_charts(timerange) {
    $.getJSON('/api?name=cumulative&timerange=' + timerange, function (data) {
        cumulative_activity_front_chart(data);
    }).always(function () {
        // hide loaders
        $('.loader').each(function () {
            $(this).hide();
        });
    }).fail(function (data, status, error) {
        $(".chart").append("<div class='error'><h5>An error occurred while loading this chart.</h5><p>Wait a moment, then try reloading the page.<br><i>(" + error + ")</i></p>");
    });
}

function cumulative_activity_front_chart(data) {
    Highcharts.chart('cumulative_activity_front_chart', {
        chart: {
            height: '300px',
            zoomType: 'x'
        },
        title: {
            text: "Activity of top 100 threads"
        },
        credits: {
            enabled: false
        },
        legend: {
            enabled: false
        },
        tooltip: {
            shared: true
        },
        xAxis: {
            type: 'datetime',
            crosshair: true
        },
        yAxis: [{
            title: {
                text: 'Comments'
            }
        },
        {
            title: {
                text: 'Karma'
            },
            opposite: true
        }
        ],
        series: [{
            type: 'column',
            name: 'Comments',
            yAxis: 0,
            data: data['front']['comments'],
            pointPadding: 0.01
        },
        {
            type: 'line',
            name: 'Karma',
            yAxis: 1,
            data: data['front']['scores'],
            lineWidth: 6,
            marker: {
                symbol: 'circle',
                radius: 4,
                lineColor: 'rgba(255, 255, 255, 1)',
                lineWidth: 1
            }
        }
        ],
        colors: [
            'rgba(47, 79, 79, 1)',
            'rgba(255, 69, 0, 1)'
        ],
        responsive: {
            rules: [{
                condition: {
                    maxWidth: 500
                },
                chartOptions: {
                    yAxis: [{
                        title: {
                            text: null
                        }
                    },
                    {
                        title: {
                            text: null
                        }
                    }
                    ],
                }
            }]
        }
    });
}