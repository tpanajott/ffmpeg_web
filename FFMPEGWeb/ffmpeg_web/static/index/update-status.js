function update_progress() {
    $.getJSON("/job_status", function(data) {
        $.each(data.jobs, function(index, job) {
            job_id = job.id
            var status_object = $("[data-id='"+job_id+"'] .convert_status")
            if (job.status == "running") {
                if (job.percentage == -1) {
                    status_object.text('Unknown progress')
                    status_object.attr('class', 'tag convert_status is-primary')
                } else {
                    status_object.text('Running: ' + job.percentage + '%')
                    status_object.attr('class', 'tag convert_status is-primary')
                }
            } else if (job.status == 'complete') {
                status_object.text('Completed')
                status_object.attr('class', 'tag convert_status is-success has-text-dark')
            } else if (job.status == 'failed') {
                status_object.text('Failed')
                status_object.attr('class', 'tag convert_status is-danger has-text-dark')
            } else if (job.status == 'canceled') {
                status_object.text('Canceled')
                status_object.attr('class', 'tag convert_status is-dark')
            } else {
                status_object.text('Unknown Error')
                status_object.attr('class', 'tag convert_status is-warning has-text-dark')
            }

            $("[data-id='"+job_id+"'] .speed").text(job.speed + 'x')
            $("[data-id='"+job_id+"'] .time_left").text(job.time_left)
        })
    })
}
update_progress()
setInterval(update_progress, 1000)