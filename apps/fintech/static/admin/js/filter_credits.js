document.addEventListener("DOMContentLoaded", function () {
   const userSelect = document.querySelector("#id_user");
   const creditSelect = document.querySelector("#id_credit");

   if (!userSelect || !creditSelect) return; // Evita errores si no encuentra los campos

   function updateCredits() {
       const userId = userSelect.value;
       if (!userId) {
           creditSelect.innerHTML = '<option value="">---------</option>';
           return;
       }

       const url = new URL(window.location.href);
       url.searchParams.set('user', userId);

       fetch(url)
           .then(response => response.text())
           .then(html => {
               const parser = new DOMParser();
               const doc = parser.parseFromString(html, "text/html");
               const newCreditSelect = doc.querySelector("#id_credit");

               if (newCreditSelect) {
                   creditSelect.innerHTML = newCreditSelect.innerHTML;
               }
           })
           .catch(error => console.error("Error updating credits:", error));
   }

   userSelect.addEventListener("change", updateCredits);
});
