const approveNormButton = document.getElementById("approve-norm");

function getCookie(name) {
    const cookies = document.cookie.split(";");
    const cookie = cookies.find((item) => item.trim().startsWith(`${name}=`));
    return cookie ? decodeURIComponent(cookie.trim().slice(name.length + 1)) : null;
}

approveNormButton?.addEventListener("click", async (event) => {
    event.preventDefault();
    approveNormButton.classList.add("disabled");
    approveNormButton.setAttribute("aria-disabled", "true");

    try {
        const response = await fetch(approveNormButton.href, {
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
        status.className = "badge border border-success rounded-5 text-warning fw-semibold";
        approveNormButton.remove();
    } catch (error) {
        approveNormButton.classList.remove("disabled");
        approveNormButton.removeAttribute("aria-disabled");
        window.alert(error.message);
    }
});