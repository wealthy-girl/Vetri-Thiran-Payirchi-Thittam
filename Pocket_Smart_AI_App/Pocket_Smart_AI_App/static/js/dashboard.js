async function loadHistory() {

    try {

        const user =
            await api(
                "/api/auth/me"
            );


        document.querySelector(
            "#welcome"
        ).textContent =
            `Welcome, ${user.name}`;


        const rows =
            await api(
                "/api/history"
            );


        const history =
            document.querySelector(
                "#history"
            );


        if (!rows.length) {

            history.innerHTML =
                `
                <p class="muted">
                    No recommendations yet.
                </p>
                `;

            return;
        }


        history.innerHTML =
            rows
                .map(
                    row => `

                    <div class="item">

                        <b>
                            ${esc(row.planner)}
                        </b>

                        —

                        ${new Date(
                            row.created_at
                        ).toLocaleString()}

                        <br>

                        <a
                            href="/${esc(row.planner)}"
                        >
                            Create another plan
                        </a>

                    </div>
                `
                )
                .join("");


    } catch (error) {

        location.href =
            "/login";
    }
}


loadHistory();