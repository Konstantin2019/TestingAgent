var save_dom = $('#content').html();

function get_student(idx, student) {
    let row =
        $(`<tr id="${student["id"]}">
                <td>${idx}</td>
                <td id="surname${student["id"]}">${student["surname"]}</td>
                <td id="name${student["id"]}">${student["name"]}</td>
                <td id="patronymic${student["id"]}">${student["patronymic"]}</td>
                <td id="rk1_${student["id"]}">
                    <button id="view_student_rk1_${student["id"]}" data-toggle="tooltip" title="Просмотреть">
                        <span style="color: purple">
                            <i class="fas fa-eye"></i>
                        </span>
                        <script>
                            $('#view_student_rk1_${student["id"]}').click(["rk1"], view_student);
                        </script>
                    </button>
                    <span id="rk1_${student["id"]}_value">${student["rk1_score"]}</span>
                </td>
                <td id="rk2_${student["id"]}">
                    <button id="view_student_rk2_${student["id"]}" data-toggle="tooltip" title="Просмотреть">
                        <span style="color: purple">
                            <i class="fas fa-eye"></i>
                        </span>
                        <script>
                            $('#view_student_rk2_${student["id"]}').click(["rk2"], view_student);
                        </script>
                    </button>
                    <span id="rk2_${student["id"]}_value">${student["rk2_score"]}</span>
                </td>
                <td>
                    <button id="del_student_${student["id"]}" data-toggle="tooltip" title="Удалить">
                        <span style="color: red">
                            <i class="fas fa-ban"></i>
                        </span>
                        <script>
                            $('#del_student_${student["id"]}').click(del_student);
                        </script>
                    </button>
                    <button id="refresh_${student["id"]}" data-toggle="tooltip" title="Обновить">
                        <span style="color: red">
                            <i class="fa fa-refresh" aria-hidden="true"></i>
                        </span>
                        <script>
                            $('#refresh_${student["id"]}').click(refresh);
                        </script>
                    </button>
                </td>
        </tr>`);
    return row;
}

function make_questions_dom(rk, student) {
    let dom =
        $(`<div class="container">
            <div class="jumbotron">
                <div class="row justify-content-center">
                    <span style="font-size: 25px; color: cornflowerblue;"><b>${student}</b></span>
                </div>
                <div class="row">
                    <table id="${rk}" class="table">
                        <thead>
                            <tr>
                                <th scope="col">№</th>
                                <th scope="col">Вопрос</th>
                                <th scope="col">Ответ студента</th>
                                <th scope="col">Правильный ответ</th>
                                <th scope="col">Балл</th>
                            </tr>
                        </thead>
                        <tbody></tbody>
                    </table>
                </div>
                <div class="row justify-content-center">
                    <button id="back">
                        <script>
                            $('#back').click(go_back);
                        </script>
                    Назад</button>
                </div>
            </div>
        </div>`);
    return dom;
}

function get_question(idx, question) {
    let row =
        $(`<tr id="${question["id"]}">
            <td>${idx}</td>
            <td>${question["question"]}</td>
            <td>${question["student_answer"]}</td>
            <td>${question["correct_answer"]}</td>
            <td contenteditable="True">${question["score"]}</td>
        </tr>`);
    return row;
}

function view_student(rk_data) {
    let rk = rk_data.data[0];
    let student_id = $(this).parents('tr')[0].id;
    $.ajax({
        type: "GET",
        url: $(location).attr('href') + `/view_student/${student_id}`,
        data: { 'rk': rk, 'method': 'view' },
        success: (response) => {
            try {
                let json_rk = $.parseJSON(response);
                save_dom = $('#content').html();
                $('#year_sel').prop('disabled', true);
                $('#group_sel').prop('disabled', true);
                let student = $(`#surname${student_id}`).text() + ' ' + $(`#name${student_id}`).text();
                $('#content').empty();
                $('#content').append(make_questions_dom(rk, student));
                let idx = 1;
                json_rk.forEach(json_question => {
                    let question = $.parseJSON(json_question);
                    if (question != undefined || null) {
                        $(`#${rk}`).find('tbody').append(get_question(idx, question));
                    }
                    idx++;
                });
            }
            catch (err) { }
        }
    });
}

function del_student() {
    let student_id = $(this).parents('tr')[0].id;
    $.ajax({
        type: "POST",
        url: $(location).attr('href') + `/del_student/${student_id}`,
        contentType: "application/json",
        data: JSON.stringify({ 'method': 'delete' }),
        success: (response) => {
            let student_id = $.parseJSON(response);
            alert(`Студент с id = ${student_id} успешно удалён!`);
            $(`#${student_id}`).remove();
        },
        error: () => { }
    });
}

function refresh () {
    let student_id = $(this).parents('tr')[0].id;
    $.ajax({
        type: "GET",
        url: $(location).attr('href') + `/get_student/${student_id}`,
        data: { 'refresh': 'yes' },
        success: (response) => {
            $(`#rk1_${student_id}_value`).text(response[0]);
            $(`#rk2_${student_id}_value`).text(response[1]);
        },
        error: () => { }
    });
}

function go_back() {
    $('#content').empty();
    $('#content').append(save_dom);
    $('#year_sel').prop('disabled', false);
    $('#group_sel').prop('disabled', false);
}

$(document).ready(() => {
    $('#year_sel').on('change', function () {
        let selected_year = $('option:selected', this);
        let year_value = selected_year.val();
        if (year_value != undefined || null) {
            $.ajax({
                type: "GET",
                url: $(location).attr('href') + '/view_year',
                data: { year: year_value },
                success: (response) => {
                    try {
                        let json_groups = $.parseJSON(response);
                        $('#group_sel').empty();
                        $('#group_sel').append($('<option>', { text: "Выберите группу..." }));
                        json_groups.forEach(json_group => {
                            let group = $.parseJSON(json_group);
                            $('#group_sel').append($('<option>', {
                                value: group["id"],
                                text: group["group_name"]
                            }));
                        });
                    } catch (err) { }
                },
                error: () => { }
            });
        }
    });

    $('#group_sel').on('change', function () {
        let selected_year = $('#year_sel option:selected');
        let selected_group = $('option:selected', this);
        let year_value = selected_year.val();
        let group_value = selected_group.val();
        if (group_value != undefined || null) {
            $.ajax({
                type: "GET",
                url: $(location).attr('href') + '/view_group',
                data: { year: year_value, group: group_value },
                success: (response) => {
                    try {
                        let json_students = $.parseJSON(response);
                        $('#students_lst tbody').empty();
                        let idx = 1;
                        json_students.forEach(json_student => {
                            let student = $.parseJSON(json_student);
                            if (student != undefined || null) {
                                $('#students_lst').find('tbody').append(get_student(idx, student));
                                idx++;
                            }
                        });
                    } catch (err) { }
                },
                error: () => { }
            });
        }
    });

    $('#add_group').click(() => {
        if ($('#gr_inp').css('visibility') == 'hidden') {
            $('#gr_inp').css('visibility', 'visible');
        }
        else {
            let text = $('#gr_inp').val();
            if (text.length > 3) {
                $.ajax({
                    type: "POST",
                    url: $(location).attr('href') + '/create_group',
                    contentType: "application/json",
                    data: JSON.stringify({ 'group_name': text, 'method': 'create' }),
                    success: (response) => {
                        $('#gr_inp').css('visibility', 'hidden');
                        let id = $.parseJSON(response);
                        alert(`Группа с id = ${id} успешно добавлена!`);
                        $('#group_sel').append($('<option>', {
                            value: id,
                            text: text,
                        }));
                        $('#group_sel option:last').prop('selected', true).change();
                    },
                    error: () => { }
                });
            }
        }
    });

    $('#del_group').click(() => {
        let group_id = $('#group_sel option:selected').val();
        if (group_id != undefined || null) {
            $.ajax({
                type: "POST",
                url: $(location).attr('href') + `/del_group/${group_id}`,
                contentType: "application/json",
                data: JSON.stringify({ 'method': 'delete' }),
                success: (response) => {
                    let id = $.parseJSON(response);
                    alert(`Группа с id = ${id} успешно удалена!`);
                    $('#group_sel').find('[value=' + id + ']').remove();
                    $('#group_sel option:last').prop('selected', true).change();
                },
                error: () => { }
            });
        }
    });

    $(document).on('keypress', 'table tbody tr', function (e) {
        if (e.key == "Enter") {
            e.preventDefault();
            let table_id = $(this).parents('table')[0].id;
            let question_id = $(this).attr('id');
            if (table_id == 'rk1' || table_id == 'rk2') {
                let taget = $('td:last', this);
                $.ajax({
                    type: "POST",
                    url: $(location).attr('href') + `/patch_question/${question_id}`,
                    contentType: "application/json",
                    data: JSON.stringify({
                        'question_score': taget.text(),
                        'rk': table_id
                    }),
                    success: (response) => {
                        let id = $.parseJSON(response);
                        alert(`Баллы за вопрос с id = ${id} успешно изменены!`);
                    },
                    error: () => { }
                });
            }
        }
    });
});