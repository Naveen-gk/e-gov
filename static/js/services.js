document.addEventListener("DOMContentLoaded", () => {
    const services = [
        {
            title: "Online Applications",
            description: "Application Status for online applications for Social Welfare Schemes."
        },
        {
            title: "Online Birth Certificate",
            description: "Allows citizens to apply and download birth certificates online."
        },
        {
            title: "TNEB",
            description: "EOnline Payment of Electricity Bill (for consumers of Tamil Nadu)"
        },
        {
            title: "E-Sevai Centers",
            description: "One-stop digital services for applying certificates, paying bills, and more."
        },
        {
            title: "Employment Exchange",
            description: "Job seekers can register and get notified of job openings."
        },
        {
            title: "RTI Portal",
            description: "Citizens can file RTI applications to seek information from government departments."
        }
    ];

    const container = document.getElementById("services-container");

    services.forEach(service => {
        const card = document.createElement("div");
        card.className = "service-card";

        const title = document.createElement("h2");
        title.textContent = service.title;

        const desc = document.createElement("p");
        desc.textContent = service.description;

        card.appendChild(title);
        card.appendChild(desc);
        container.appendChild(card);
    });
});
