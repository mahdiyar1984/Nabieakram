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

function toggleDropdown() {
      var menu = document.getElementById('dropdownMenu');
      if (menu.style.display === 'block') {
        menu.style.display = 'none';
      } else {
        menu.style.display = 'block';
      }
    }
    // Optional: Close dropdown if clicked outside
    document.addEventListener('click', function(event) {
      var toggle = document.getElementById('dropdownToggle');
      var menu = document.getElementById('dropdownMenu');
      if (!toggle.contains(event.target) && !menu.contains(event.target)) {
        menu.style.display = 'none';
      }
    });