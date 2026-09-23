const submitForApprovalButton = document.getElementById("submit-for-approval");

function getCookie(name) {
    const cookies = document.cookie.split(";");
    const cookie = cookies.find((item) => item.trim().startsWith(`${name}=`));
    return cookie ? decodeURIComponent(cookie.trim().slice(name.length + 1)) : null;
}

submitForApprovalButton?.addEventListener("click", async (event) => {
    event.preventDefault();
    submitForApprovalButton.classList.add("disabled");
    submitForApprovalButton.setAttribute("aria-disabled", "true");

    try {
        const response = await fetch(submitForApprovalButton.href, {
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
        status.className = "badge border border-primary rounded-5 text-primary fw-semibold";
        submitForApprovalButton.remove();
    } catch (error) {
        submitForApprovalButton.classList.remove("disabled");
        submitForApprovalButton.removeAttribute("aria-disabled");
        window.alert(error.message);
    }
});