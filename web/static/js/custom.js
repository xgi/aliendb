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

function submission_subjectivity_chart(data) {
    Highcharts.chart('submission_subjectivity_chart', {
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

function submission_upvote_ratio_chart(data) {
    Highcharts.chart('submission_upvote_ratio_chart', {
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

function submission_special_users_chart(data) {
    Highcharts.chart('submission_special_users_chart', {
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

function submission_gilded_chart(data) {
    Highcharts.chart('submission_gilded_chart', {
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

function subreddit_charts(id) {
    $.getJSON('/api?name=subreddit&id=' + id, function (data) {
        subreddit_activity_chart(data);
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
        plotOptions: {
            series: {
                lineWidth: 3
            }
        },
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
            text: null
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
        plotOptions: {
            line: {
                marker: {
                    enabled: false
                }
            },
            series: {
                lineWidth: 3
            }
        },
        series: [
            {
                type: 'line',
                name: 'Karma',
                yAxis: 0,
                data: data['front']['scores']
            },
            {
                type: 'line',
                name: 'Comments',
                yAxis: 1,
                data: data['front']['comments']
            }
        ],
        colors: [
            'rgba(255, 69, 0, 1)',
            'rgba(47, 79, 79, 1)'
        ]
    });
}