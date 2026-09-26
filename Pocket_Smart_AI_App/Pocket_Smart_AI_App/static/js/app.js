async function api(url, options = {}) {

    const response = await fetch(
        url,
        {
            credentials: "include",
            ...options
        }
    );

    const data =
        await response
            .json()
            .catch(() => ({}));


    if (!response.ok) {

        throw new Error(
            data.detail ||
            "Request failed"
        );
    }


    return data;
}


function esc(value) {

    return String(
        value ?? ""
    ).replace(
        /[&<>"']/g,
        function (character) {

            const map = {

                "&": "&amp;",

                "<": "&lt;",

                ">": "&gt;",

                '"': "&quot;",

                "'": "&#39;"
            };

            return map[character];
        }
    );
}