document.addEventListener('DOMContentLoaded', function() {
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
                el.classList.add('bg-gray-800', 'text-purple-300');
            });
            
            // Show selected content and update button
            content.classList.remove('hidden');
            btn.classList.remove('bg-gray-800', 'text-purple-300');
            btn.classList.add('bg-gradient-to-r', 'from-purple-600', 'to-blue-500', 'text-white');
        });
    });

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

    // Initialize daily cycle as default
    document.getElementById('dailyBtn').click();
});
