document.addEventListener("DOMContentLoaded", () => {
    const topSchemes = [
        "Amma Two Wheeler Scheme",
        "Chief Minister's Comprehensive Health Insurance Scheme",
        "Amma Kudineer (Drinking Water) Scheme",
        "Unemployed Youth Employment Generation Programme"
    ];

    const recentSchemes = [
        "Kalaignar Magalir Urimai Thittam (Women's Basic Income Scheme)",
        "Naan Mudhalvan - Skill Development Program",
        "Pudhumai Penn Scheme for Girls' Education",
        "Tamil Nadu Green Mission - Urban Forest Expansion"
    ];

    const topContainer = document.getElementById("top-schemes-container");
    const recentContainer = document.getElementById("recent-schemes-container");

    function createSchemeCard(name) {
        const card = document.createElement("div");
        card.className = "scheme-card";

        const title = document.createElement("div");
        title.className = "scheme-title";
        title.textContent = name;

        card.appendChild(title);
        return card;
    }

    topSchemes.forEach(scheme => {
        const card = createSchemeCard(scheme);
        topContainer.appendChild(card);
    });

    recentSchemes.forEach(scheme => {
        const card = createSchemeCard(scheme);
        recentContainer.appendChild(card);
    });
});
