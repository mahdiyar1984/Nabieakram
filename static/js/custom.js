function setParentId(id) {
    document.getElementById("parent_id").value = id;
      // فرم رو پیدا کن
    const form = document.getElementById("comment-form");

    // اسکرول نرم به سمت فرم
    form.scrollIntoView({ behavior: "smooth", block: "start" });
}
