document.addEventListener("DOMContentLoaded", function () {

    
    // ADD CANDIDATE FORM VALIDATION
    
    const addForm = document.getElementById("addCandidateForm");

    if (addForm) {
        addForm.addEventListener("submit", function (event) {

            const class10 = parseFloat(document.getElementById("class10").value);
            const class12 = parseFloat(document.getElementById("class12").value);
            const cgpa = parseFloat(document.getElementById("cgpa").value);
            const projects = parseInt(document.getElementById("projects").value);
            const hackathons = parseInt(document.getElementById("hackathons_count").value);
            const leetcode = parseInt(document.getElementById("leetcode").value);
            const codechef = parseInt(document.getElementById("codechef").value);
            const hackerrank = parseInt(document.getElementById("hackerrank").value);

            function isInvalid(condition, message) {
                if (condition) {
                    alert(message);
                    event.preventDefault();
                    return true;
                }
                return false;
            }

            if (
                isInvalid(class10 < 0 || class10 > 100, "Class 10 percentage must be between 0 and 100.") ||
                isInvalid(class12 < 0 || class12 > 100, "Class 12 percentage must be between 0 and 100.") ||
                isInvalid(cgpa < 0 || cgpa > 10, "CGPA must be between 0 and 10.") ||
                isInvalid(projects < 0, "Projects cannot be negative.") ||
                isInvalid(hackathons < 0, "Hackathons count cannot be negative.") ||
                isInvalid(leetcode < 0 || codechef < 0 || hackerrank < 0, "Coding scores cannot be negative.")
            ) {
                return;
            }
        });
    }

    
    // SKILLS CLEANING 
    
    const skillsInput = document.getElementById("skills");

    if (skillsInput) {
        skillsInput.addEventListener("blur", function () {

            let cleaned = skillsInput.value
                .split(",")
                .map(skill => skill.trim().toLowerCase())
                .filter(skill => skill.length > 0);

            skillsInput.value = cleaned.join(", ");
        });
    }

    
    // FILTER FORM CONFIRMATION
    
    const filterForm = document.getElementById("filterForm");

    if (filterForm) {
        filterForm.addEventListener("submit", function (event) {
            const confirmAction = confirm("Apply filter and rank candidates?");
            if (!confirmAction) {
                event.preventDefault();
            }
        });
    }

});

// RESULT PIE CHART (Filter Result Page)

function renderResultChart(selected, rejected) {
    const canvas = document.getElementById("resultChart");

    if (!canvas) return;

    new Chart(canvas, {
        type: "pie",
        data: {
            labels: ["Selected", "Rejected"],
            datasets: [{
                data: [selected, rejected],
                backgroundColor: ["#22c55e", "#ef4444"],
                borderWidth: 1
            }]
        },
        options: {
            plugins: {
                legend: {
                    labels: {
                        color: "#e2e8f0"
                    }
                }
            }
        }
    });
}