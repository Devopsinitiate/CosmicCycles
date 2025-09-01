
document.addEventListener('DOMContentLoaded', function() {
    // Set current year in footer
    document.getElementById('currentYear').textContent = new Date().getFullYear();

    // Update current time display
    function updateDateTime() {
        const now = new Date();
        const options = {
            weekday: 'long',
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        };
        document.getElementById('currentDateTime').textContent = now.toLocaleDateString('en-US', options);
    }
    updateDateTime();
    setInterval(updateDateTime, 1000);

    // Tab switching functionality
    const tabs = ['daily', 'yearly', 'business', 'soul'];
    tabs.forEach(tab => {
        const btn = document.getElementById(`${tab}Btn`);
        const content = document.getElementById(`${tab}Content`);

        btn.addEventListener('click', () => {
            // Hide all contents and reset all buttons
            document.querySelectorAll('.cycle-content').forEach(el => el.classList.add('hidden'));
            document.querySelectorAll('[id$="Btn"]').forEach(el => {
                el.classList.remove('bg-gradient-to-r', 'from-purple-600', 'to-blue-500', 'text-white');
                el.classList.add('bg-gray-800', 'text-purple-300', 'border', 'border-purple-900');
            });

            // Show selected content and update button
            content.classList.remove('hidden');
            btn.classList.remove('bg-gray-800', 'text-purple-300', 'border', 'border-purple-900');
            btn.classList.add('bg-gradient-to-r', 'from-purple-600', 'to-blue-500', 'text-white', 'shadow-lg', 'shadow-purple-500/20');

            // Update current cycle info based on the active tab
            updateCurrentCycleInfo(tab);
        });
    });

    // Function to update current cycle info display
    function updateCurrentCycleInfo(activeTab) {
        let infoHtml = '';
        const currentDailyPeriod = JSON.parse(document.getElementById('daily-period-data').textContent);
        const currentYearlyPeriod = JSON.parse(document.getElementById('yearly-period-data').textContent);
        const currentBusinessPeriod = JSON.parse(document.getElementById('business-period-data').textContent);
        const currentSoulPeriod = JSON.parse(document.getElementById('soul-period-data').textContent);

        switch(activeTab) {
            case 'daily':
                infoHtml = `
                    <div class="bg-indigo-50 rounded-lg p-4">
                        <h3 class="text-xl font-semibold text-indigo-800 mb-2">Current Daily Period: ${currentDailyPeriod.name}</h3>
                        <p class="text-indigo-700">${currentDailyPeriod.principle}</p>
                        <p class="mt-2 text-gray-600"><strong>Time:</strong> ${currentDailyPeriod.time}</p>
                        <p class="mt-1 text-gray-600"><strong>Suggestion:</strong> ${currentDailyPeriod.suggestion}</p>
                    </div>
                `;
                break;
            case 'yearly':
                infoHtml = `
                    <div class="bg-indigo-50 rounded-lg p-4">
                        <h3 class="text-xl font-semibold text-indigo-800 mb-2">Your Yearly Cycle</h3>
                        <p class="text-indigo-700">${currentYearlyPeriod.name}</p>
                        <p class="mt-2 text-gray-600"><strong>Principle:</strong> ${currentYearlyPeriod.principle}</p>
                    </div>
                `;
                break;
            case 'business':
                infoHtml = `
                    <div class="bg-indigo-50 rounded-lg p-4">
                        <h3 class="text-xl font-semibold text-indigo-800 mb-2">Business Cycle</h3>
                        <p class="text-indigo-700">${currentBusinessPeriod.name}</p>
                        <p class="mt-2 text-gray-600"><strong>Principle:</strong> ${currentBusinessPeriod.principle}</p>
                    </div>
                `;
                break;
            case 'soul':
                infoHtml = `
                    <div class="bg-indigo-50 rounded-lg p-4">
                        <h3 class="text-xl font-semibold text-indigo-800 mb-2">Soul Cycle</h3>
                        <p class="text-indigo-700">${currentSoulPeriod.name}</p>
                        <p class="mt-2 text-gray-600"><strong>Dates:</strong> ${currentSoulPeriod.dates}</p>
                        <p class="mt-1 text-gray-600"><strong>Principle:</strong> ${currentSoulPeriod.principle}</p>
                    </div>
                `;
                break;
        }
        document.getElementById('currentCycleInfo').innerHTML = infoHtml;
    }

    // Initial display
    document.getElementById('dailyBtn').click();
});
