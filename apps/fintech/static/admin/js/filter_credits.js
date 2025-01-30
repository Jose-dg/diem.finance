document.addEventListener("DOMContentLoaded", function () {
    const userSelect = document.querySelector("#id_user");

    function updateCredits() {
        const userId = userSelect.value;
        if (!userId) return;

        document.querySelectorAll("[id^=id_accountmethodamount_set-][id$=-credit]").forEach(select => {
            const selectedValue = select.value;  // 🔹 Guardamos el valor seleccionado antes de actualizar
            const url = new URL(window.location.href);
            url.searchParams.set('user', userId);

            fetch(url)
                .then(response => response.text())
                .then(html => {
                    const parser = new DOMParser();
                    const doc = parser.parseFromString(html, "text/html");
                    const newCreditSelect = doc.querySelector("#" + select.id);

                    if (newCreditSelect) {
                        select.innerHTML = newCreditSelect.innerHTML;

                        // 🔹 Restaurar la opción seleccionada después de la actualización
                        if (selectedValue && select.querySelector(`option[value="${selectedValue}"]`)) {
                            select.value = selectedValue;
                        }
                    }
                })
                .catch(error => console.error("Error updating credits:", error));
        });
    }

    if (userSelect) {
        userSelect.addEventListener("change", updateCredits);
        updateCredits();  // Ejecutarlo al cargar la página para inicializarlo
    }
});


// document.addEventListener("DOMContentLoaded", function () {
//     const userSelect = document.querySelector("#id_user");

//     function updateCredits() {
//         const userId = userSelect.value;
//         if (!userId) return;

//         document.querySelectorAll("[id^=id_accountmethodamount_set-][id$=-credit]").forEach(select => {
//             const selectedValue = select.value;  // 🔹 Guardamos el valor seleccionado antes de actualizar
//             const url = new URL(window.location.href);
//             url.searchParams.set('user', userId);

//             fetch(url)
//                 .then(response => response.text())
//                 .then(html => {
//                     const parser = new DOMParser();
//                     const doc = parser.parseFromString(html, "text/html");
//                     const newCreditSelect = doc.querySelector("#" + select.id);

//                     if (newCreditSelect) {
//                         select.innerHTML = newCreditSelect.innerHTML;

//                         // 🔹 Restaurar la opción seleccionada después de la actualización
//                         if (selectedValue && select.querySelector(`option[value="${selectedValue}"]`)) {
//                             select.value = selectedValue;
//                         }
//                     }
//                 })
//                 .catch(error => console.error("Error updating credits:", error));
//         });
//     }

//     if (userSelect) {
//         userSelect.addEventListener("change", updateCredits);
//         updateCredits();  // Ejecutarlo al cargar la página para inicializarlo
//     }
// });
