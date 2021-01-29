current_path="/"
function update_file_list(path) {
    console.log('Entering path: ' + path)
    if (path == "../") {
        parts = current_path.split('/')
        // Remove empty arguments
        path_parts = []
        parts.forEach(part => {
            if(part != "") {
                path_parts.push(part)
            }
        });
        path_parts.pop()
        if(path_parts.length <= 0) {
            current_path = "/"
        } else {
            current_path = path_parts.join('/')
        }
        console.log(current_path)
    } else {
        current_path += path
    }

    $.getJSON('/media_files?path='+current_path, function(data) {
        $('#source-select-items').html('<p class="panel-heading">Select Source File</p>')
        $('#source-select-items').append("<a class=\"panel-block\" onclick=\"update_file_list('../')\">\
            <span class=\"panel-icon\">\
                <i class=\"fas fa-book\" aria-hidden=\"true\"></i>\
            </span>\
            ../</a>")
        $.each(data.directories, function(index, value) {
            $('#source-select-items').append("<a class=\"panel-block\" onclick=\"update_file_list('"+value+"')\">\
            <span class=\"panel-icon\">\
                <i class=\"fas fa-folder\" aria-hidden=\"true\"></i>\
            </span>\
            "+value+"</a>")
        });
        $.each(data.files, function(index, value) {
            $('#source-select-items').append("<a class=\"panel-block\" onclick=\"choose_file('"+value+"')\">\
            <span class=\"panel-icon\">\
                <i class=\"fas fa-file\" aria-hidden=\"true\"></i>\
            </span>\
            "+value+"</a>")
        });
    })
}

function choose_file(file) {
    full_path = current_path + "/" + file
    $('#source-file-input').val(full_path)
    insert_example_destination_file_name(file)
    $('#source-select-modal').removeClass('is-active');
}

function insert_example_destination_file_name(file_name) {
    name_parts = file_name.split('.')
    num_elements = name_parts.length
    name_parts.splice(num_elements-1, 0, "2")
    $('#destination-file-name').val(name_parts.join('.'))
}

update_file_list("/")