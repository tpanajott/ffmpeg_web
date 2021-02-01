function update_changed_html(item, html) {
    var object = $(item)
    if (object.html() !== html) {
        object.html(html)
    }
}

function update_progress(id) {
    $.getJSON("/job_status/"+job_id, function(job) {
        item = ""
        job_id = job.id
        var status_object = $(".convert_status")
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
        $(".speed").text(job.speed + 'x')
        $(".time_left").text(job.time_left)
        update_changed_html('#progress', '<progress class="progress is-primary" value="'+job.percentage+'" max="100">'+job.percentage+'</progress>')
    })
}
update_progress(job_id)
setInterval(update_progress, 1000)