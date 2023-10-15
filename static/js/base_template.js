$(document).ready(function () {
    $(".dropdown-trigger").dropdown();
    $('.sidenav').sidenav();
    $('.modal').modal();
});
$('#send_new_avatar_btn').click(function () {
    $("#avatar_form").submit();
});
document.getElementById('registerModalForm').addEventListener('submit', (e) => {
    e.preventDefault();
    const formData = new FormData(document.getElementById('registerModalForm'));
    fetch('/register_from_modal/', {
        method: 'POST', body: formData
    })
        .then(res => res.json()).then(res => {
        if (res.status === 'OK') {
            window.alert('Регистрация успешно выполнена! Можно входить в свой новый аккаунт!');
            window.location.reload();
        } else {
            switch (res.error) {
                case 'password_mismatch':
                    document.getElementById('reg_error_txt').innerHTML = 'Пароли не совпадают!';
                    break;
                default:
                    document.getElementById('reg_error_txt').innerHTML = res.error;
            }
        }
    })
        .catch((e) => {
            console.error('Произошла ошибка при отправке формы:', e);
        });
});
document.getElementById('loginModalForm').addEventListener('submit', (e) => {
    e.preventDefault();
    const formData = new FormData(document.getElementById('loginModalForm'));
    fetch('/login_from_modal/', {
        method: 'POST', body: formData
    })
        .then(async res => {
            if (!res.ok) {
                const errorInfo = await res.json();
                document.getElementById('login_error_txt').innerHTML = errorInfo.error;
            } else {
                window.location.reload();
            }
        })
        .catch((e) => {
            console.error('Произошла ошибка при отправке формы:', e);
        });
});

function jumpToPage(num) {
    const current_location = window.location.href;
    const page_counter_pattern = /page=\d+/i;
    if (page_counter_pattern.test(current_location)) {
        // пользователь уже на какой-то определенной странице (то есть в адресе есть page=X)
        window.location.href = current_location.replace(page_counter_pattern, `page=${num}`);
    } else if (current_location.includes('?')) {
        // пользователь еще не выбрал конкретную страницу, но в адресе есть параметр вида ?param=value, который нужно сохранить
        window.location.href = `${current_location}&page=${num}`;
    } else {
        // пользователь не выбрал страницу, никаких get-параметров в адресе нет
        window.location.href = `${current_location}?page=${num}`;
    }
}