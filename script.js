// List of 36 departments
const departments = [
    "Agriculture Department", "Animal Husbandry, Dairying, and Fisheries",
    "Backward Classes, Most Backward Classes, and Minorities Welfare",
    "Commercial Taxes and Registration", "Cooperation, Food, and Consumer Protection",
    "Energy Department", "Environment and Forests", "Finance Department",
    "Handlooms, Handicrafts, Textiles, and Khadi", "Health and Family Welfare",
    "Higher Education Department", "Highways and Minor Ports",
    "Home, Prohibition, and Excise", "Housing and Urban Development",
    "Industries Department", "Information Technology and Digital Services",
    "Labour and Employment", "Law Department", "Micro, Small, and Medium Enterprises",
    "Municipal Administration and Water Supply", "Personnel and Administrative Reforms",
    "Planning, Development, and Special Initiatives", "Public Department",
    "Public Works Department", "Revenue and Disaster Management",
    "Rural Development and Panchayat Raj", "School Education Department",
    "Social Reforms Department", "Social Welfare and Nutritious Meal Programme",
    "Special Programme Implementation", "Tourism, Culture, and Religious Endowments",
    "Transport Department", "Tribal Welfare Department", "Welfare of Differently Abled Persons",
    "Welfare of Women", "Youth Welfare and Sports Development"
];
document.addEventListener('DOMContentLoaded', () => {
    const departmentContainer = document.querySelector('.departments-container');
    if (departmentContainer) {
        departments.forEach(department => {
            const depCard = document.createElement('div')
            depCard.className = "department-item";
            depCard.innerHTML = `<span>${department}</span>`
            departmentContainer.appendChild(depCard);
        });
    }
});