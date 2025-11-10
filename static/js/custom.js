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

// Rating in article detail
document.addEventListener('DOMContentLoaded', function () {
    const ratingDiv = document.getElementById('rating');
    if (!ratingDiv) return; // اگه صفحه امتیاز نداره، هیچی اجرا نکن

    const articleId = ratingDiv.dataset.articleId;
    const csrfToken = ratingDiv.dataset.csrf;
    const messageBox = document.getElementById('rating-message');

    document.querySelectorAll('input[name="rate"]').forEach(radio => {
        radio.addEventListener('change', function () {
            const score = this.value;

            fetch("/rate-article/", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': csrfToken,
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: `score=${score}&article_id=${articleId}`
            })
                .then(response => response.json())
                .then(data => {
                    if (data.average) {
                        // نمایش پیام در صفحه
                        messageBox.textContent = `✅ امتیاز شما ثبت شد.`;
                        messageBox.style.display = 'block';
                        messageBox.style.color = 'green';

                        // بعد از چند ثانیه پنهان شود
                        setTimeout(() => {
                            messageBox.style.display = 'none';
                        }, 4000);
                    } else if (data.error) {
                        messageBox.textContent = '❌ خطا در ثبت امتیاز. لطفا دوباره تلاش کنید.';
                        messageBox.style.color = 'red';
                        messageBox.style.display = 'block';
                    }
                })
                .catch(err => {
                    console.error(err);
                    messageBox.textContent = '❌ ارتباط با سرور برقرار نشد.';
                    messageBox.style.color = 'red';
                    messageBox.style.display = 'block';
                });
        });
    });
});

// Rating in lecture detail
document.addEventListener('DOMContentLoaded', function () {
    const ratingDiv = document.getElementById('rating2');
    if (!ratingDiv) return; // اگه صفحه امتیاز نداره، هیچی اجرا نکن

    const lectureId = ratingDiv.dataset.lectureId;
    const csrfToken = ratingDiv.dataset.csrf;
    const messageBox = document.getElementById('rating-message');

    document.querySelectorAll('input[name="rate"]').forEach(radio => {
        radio.addEventListener('change', function () {
            const score = this.value;

            fetch("/rate-lecture/", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': csrfToken,
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: `score=${score}&lecture_id=${lectureId}`
            })
                .then(response => response.json())
                .then(data => {
                    if (data.average) {
                        // نمایش پیام در صفحه
                        messageBox.textContent = `✅ امتیاز شما ثبت شد.`;
                        messageBox.style.display = 'block';
                        messageBox.style.color = 'green';

                        // بعد از چند ثانیه پنهان شود
                        setTimeout(() => {
                            messageBox.style.display = 'none';
                        }, 4000);
                    } else if (data.error) {
                        messageBox.textContent = '❌ خطا در ثبت امتیاز. لطفا دوباره تلاش کنید.';
                        messageBox.style.color = 'red';
                        messageBox.style.display = 'block';
                    }
                })
                .catch(err => {
                    console.error(err);
                    messageBox.textContent = '❌ ارتباط با سرور برقرار نشد.';
                    messageBox.style.color = 'red';
                    messageBox.style.display = 'block';
                });
        });
    });
});











// ckeditor.js
document.addEventListener("DOMContentLoaded", function () {
    ClassicEditor
        .create(document.querySelector('#editor'), {
            toolbar: {
                items: [
                    'heading', '|',
                    'bold', 'italic', 'underline', 'strikethrough', 'subscript', 'superscript', '|',
                    'fontFamily', 'fontSize', 'fontColor', 'fontBackgroundColor', '|',
                    'alignment', 'indent', 'outdent', '|',
                    'link', 'blockQuote', 'code', 'codeBlock', '|',
                    'bulletedList', 'numberedList', '|',
                    'insertTable', 'tableColumn', 'tableRow', 'mergeTableCells', '|',
                    'horizontalLine', 'pageBreak', 'specialCharacters', '|',
                    'undo', 'redo', '|',
                    'imageUpload', 'mediaEmbed', 'htmlEmbed'
                ]
            },
            table: {
                contentToolbar: ['tableColumn', 'tableRow', 'mergeTableCells']
            },
            image: {
                toolbar: [
                    'imageTextAlternative',
                    'imageStyle:inline',
                    'imageStyle:block',
                    'imageStyle:side'
                ]
            },
            htmlEmbed: {
                showPreviews: true
            },
            fontFamily: {
                options: [
                    'default',
                    'Arial, Helvetica, sans-serif',
                    'Times New Roman, Times, serif',
                    'Courier New, Courier, monospace',
                    'Tahoma, Geneva, sans-serif',
                    'Georgia, serif'
                ]
            },
            fontSize: {
                options: [10, 12, 14, 16, 18, 20, 24, 28],
                supportAllValues: true
            },
            link: {
                decorators: {
                    addTargetToExternalLinks: true,
                    defaultProtocol: 'https://'
                }
            },
            mediaEmbed: {
                previewsInData: true
            },
            heading: {
                options: [
                    { model: 'paragraph', title: 'پاراگراف', class: 'ck-heading_paragraph' },
                    { model: 'heading1', view: 'h1', title: 'عنوان ۱', class: 'ck-heading_heading1' },
                    { model: 'heading2', view: 'h2', title: 'عنوان ۲', class: 'ck-heading_heading2' },
                    { model: 'heading3', view: 'h3', title: 'عنوان ۳', class: 'ck-heading_heading3' },
                    { model: 'heading4', view: 'h4', title: 'عنوان ۴', class: 'ck-heading_heading4' }
                ]
            },
            wordCount: {
                onUpdate: stats => {
                    const counter = document.getElementById('word-count');
                    if (counter) {
                        counter.textContent = `کلمات: ${stats.words} | کاراکترها: ${stats.characters}`;
                    }
                }
            },
            language: 'fa'
        })
        .then(editor => {
            console.log("✅ CKEditor 5 Ready (Full Version)");
        })
        .catch(error => {
            console.error("CKEditor error:", error);
        });
});