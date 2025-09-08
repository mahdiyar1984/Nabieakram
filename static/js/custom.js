console.log("JS Loaded");

function setParentId(id) {
    document.getElementById("parent_id").value = id;
      // فرم رو پیدا کن
    const form = document.getElementById("comment-form");

    // اسکرول نرم به سمت فرم
    form.scrollIntoView({ behavior: "smooth", block: "start" });
}

document.addEventListener('DOMContentLoaded', function() {
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
