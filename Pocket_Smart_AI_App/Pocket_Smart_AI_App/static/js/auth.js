const form =
    document.querySelector(
        "#auth-form"
    );


if (form) {

    form.addEventListener(
        "submit",
        async function (event) {

            event.preventDefault();


            const message =
                document.querySelector(
                    "#msg"
                );


            try {

                const formData =
                    new FormData(form);


                const data =
                    Object.fromEntries(
                        formData.entries()
                    );


                const path =
                    form.dataset.mode
                    === "register"

                        ? "/api/auth/register"

                        : "/api/auth/login";


                await api(

                    path,

                    {

                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify(data)
                    }
                );


                location.href =
                    "/dashboard";


            } catch (error) {

                message.textContent =
                    error.message;

                message.className =
                    "error";
            }
        }
    );
}