console.log("JS Loaded");

function setParentId(id) {
    document.getElementById("parent_id").value = id;
    // فرم رو پیدا کن
    const form = document.getElementById("comment-form");

    // اسکرول نرم به سمت فرم
    form.scrollIntoView({behavior: "smooth", block: "start"});
}

document.addEventListener('DOMContentLoaded', function () {
    const avatarImg = document.getElementById('avatar-img');
    const avatarInput = document.getElementById('avatar-input');
    const avatarForm = document.getElementById('avatar-form');

    if (avatarImg && avatarInput && avatarForm) {
        avatarImg.addEventListener('click', function () {
            avatarInput.click();
        });

        avatarInput.addEventListener('change', function () {
            avatarForm.submit();
        });
    }
});

function toggleDropdown() {
    var menu = document.getElementById('dropdownMenu');
    if (menu.style.display === 'block') {
        menu.style.display = 'none';
    } else {
        menu.style.display = 'block';
    }
}

// Optional: Close dropdown if clicked outside
document.addEventListener('click', function (event) {
    var toggle = document.getElementById('dropdownToggle');
    var menu = document.getElementById('dropdownMenu');
    if (!toggle.contains(event.target) && !menu.contains(event.target)) {
        menu.style.display = 'none';
    }
});

// captcha in contact us
document.addEventListener('DOMContentLoaded', function () {
    const refreshLink = document.getElementById('refresh-captcha');
    if (!refreshLink) return;

    refreshLink.addEventListener('click', function (e) {
        e.preventDefault();

        fetch('/captcha/refresh/', {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'  // مهم: درخواست AJAX
            }
        })
            .then(response => {
                if (!response.ok) throw new Error('Network response was not ok');
                return response.json();
            })
            .then(data => {
                const img = document.querySelector('img.captcha');
                const hidden = document.getElementById('id_captcha_0');
                const inputText = document.getElementById('id_captcha_1'); // فیلد متن CAPTCHA
                if (img && hidden) {
                    img.src = data.image_url;
                    hidden.value = data.key;
                }
                if (inputText) {
                    inputText.value = ''; // پاک کردن فیلد متن
                }
            })
            .catch(error => console.error('CAPTCHA refresh error:', error));
    });
});