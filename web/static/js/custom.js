function submission_charts(id) {
    $.getJSON('/api?name=submission&id=' + id, function (data) {
        polarity_chart(data);
        subjectivity_chart(data);
        activity_chart(data);
        upvote_ratio_chart(data);
        special_users_chart(data);
        gilded_chart(data);
    }).always(function () {
        // hide loaders
        $('.loader').each(function () {
            $(this).hide();
        });
    }).fail(function (data, status, error) {
        $(".chart").append("<div class='error'><h5>An error occurred while loading this chart.</h5><p>Wait a moment, then try reloading the page.<br><i>(" + error + ")</i></p>");
    });
}

function polarity_chart(data) {
    Highcharts.chart('chart_polarity', {
        chart: {
            type: 'bar'
        },
        title: {
            text: null
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
        series: [
            {
                name: 'This post',
                data: data['polarity']['submission'],
            },
            {
                name: 'Subreddit avg.',
                data: data['polarity']['subreddit'],
            }
        ]
    });
}

function subjectivity_chart(data) {
    Highcharts.chart('chart_subjectivity', {
        chart: {
            type: 'bar'
        },
        title: {
            text: null
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
        series: [
            {
                name: 'This post',
                data: data['subjectivity']['submission'],
            },
            {
                name: 'Subreddit avg.',
                data: data['subjectivity']['subreddit'],
            }
        ]
    });
}

function activity_chart(data) {
    Highcharts.chart('chart_activity', {
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
            type: 'datetime'
        },
        yAxis: [
            {
                title: {
                    text: 'Karma'
                }
            },
            {
                title: {
                    text: 'Comments'
                },
                opposite: true
            }
        ],
        series: [
            {
                type: 'line',
                name: 'Karma',
                yAxis: 0,
                data: data['activity']['scores']
            },
            {
                type: 'line',
                name: 'Comments',
                yAxis: 1,
                data: data['activity']['comments']
            }
        ],
        colors: [
            'rgba(255, 69, 0, 1)',
            'rgba(47, 79, 79, 1)'
        ]
    });
}

function upvote_ratio_chart(data) {
    Highcharts.chart('chart_upvote_ratio', {
        chart: {
            zoomType: 'x'
        },
        title: {
            text: null
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
        series: [
            {
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
                data: [[data['upvote_ratio']['upvote_ratios'][0][0], data['upvote_ratio']['average_upvote_ratio']]]
            }
        ],
        colors: [
            'rgba(255, 69, 0, 1)'
        ]
    });
}

function special_users_chart(data) {
    Highcharts.chart('chart_special_users', {
        chart: {
            type: 'column'
        },
        title: {
            text: null
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
        series: [
            {
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

function gilded_chart(data) {
    Highcharts.chart('chart_gilded', {
        chart: {
            type: 'bar'
        },
        title: {
            text: null
        },
        credits: {
            enabled: false
        },
        xAxis: {
            categories: ['This post', 'Subreddit avg.'],
        },
        yAxis: {
            min: 0,
            title: {
                text: null
            }
        },
        tooltip: {
            valueSuffix: ' gold'
        },
        legend: {
            enabled: false
        },
        series: [
            {
                name: 'Gold given',
                data: data['gilded']['data'],
                colorByPoint: true
            }
        ],
        colors: [
            'rgba(218, 165, 32, 0.65)',
            'rgba(160, 82, 45, 0.65)'
        ]
    });
}
