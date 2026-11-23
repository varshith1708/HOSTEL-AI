document.addEventListener("DOMContentLoaded", function () {
    const exampleBtns = document.querySelectorAll(".example-btn");
    const textarea = document.getElementById("ticket_text");

    exampleBtns.forEach(btn => {
        btn.addEventListener("click", function () {
            const sampleText = this.getAttribute("data-text");
            if (textarea && sampleText) {
                textarea.value = sampleText;
                textarea.focus();
            }
        });
    });
});
