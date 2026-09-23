const submitForReviewButton = document.getElementById("submit-for-review");

function getCookie(name) {
    const cookies = document.cookie.split(";");
    const cookie = cookies.find((item) => item.trim().startsWith(`${name}=`));
    return cookie ? decodeURIComponent(cookie.trim().slice(name.length + 1)) : null;
}

submitForReviewButton?.addEventListener("click", async (event) => {
    event.preventDefault();
    submitForReviewButton.classList.add("disabled");
    submitForReviewButton.setAttribute("aria-disabled", "true");

    try {
        const response = await fetch(submitForReviewButton.href, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
                "Accept": "application/json",
            },
            mode: "same-origin",
        });

        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || "Não foi possível submeter a norma para revisão.");
        }

        const status = document.querySelector("#norm-status");
        status.querySelector(".fw-bold").textContent = data.status;
        status.className = "badge border border-warning rounded-5 text-warning fw-semibold";
        submitForReviewButton.remove();
    } catch (error) {
        submitForReviewButton.classList.remove("disabled");
        submitForReviewButton.removeAttribute("aria-disabled");
        window.alert(error.message);
    }
});