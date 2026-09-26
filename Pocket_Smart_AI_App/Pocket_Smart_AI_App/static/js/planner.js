async function showResult(data) {

    const box =
        document.querySelector(
            "#result"
        );


    box.innerHTML = `

        <div class="card">

            <h2>
                ${esc(data.summary)}
            </h2>

            <p>

                <b>Budget:</b>
                ₹${Number(data.budget).toLocaleString()}

                &nbsp;

                <b>Allocated:</b>
                ₹${Number(data.allocated).toLocaleString()}

                &nbsp;

                <b>Remaining:</b>
                ₹${Number(data.remaining).toLocaleString()}

            </p>

            ${
                data.items
                    .map(
                        item => `

                        <div class="item">

                            <b>
                                ${esc(item.name)}
                            </b>

                            <br>

                            ${esc(item.category)}

                            ·

                            ₹${Number(
                                item.price
                            ).toLocaleString()}

                            ·

                            ${esc(
                                item.platform
                            )}

                            <br>

                            <span class="muted">

                                ${esc(
                                    item.reason
                                )}

                            </span>

                            <br>

                            <a
                                href="${esc(item.url)}"
                                target="_blank"
                                rel="noopener"
                            >
                                Open platform search
                            </a>

                        </div>
                    `
                    )
                    .join("")
            }

        </div>
    `;
}