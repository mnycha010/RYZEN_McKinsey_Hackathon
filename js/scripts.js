// --- Global Constants and State ---
const currencySymbol = 'R';

// The data structure used for the database (initial default values)
const DEFAULT_DATA = {
    groupBalance: 125450,
    userContribution: 2500,
    activeMembers: 10,
    totalMembers: 12,
    recentPayout: '2024-09-30', // YYYY-MM-DD
    currentProgress: 25000,
    targetProgress: 30000,
    missedContributors: [
        { name: 'Kabelo Mokoena', amountDue: 2500 },
        { name: 'Lerato Viljoen', amountDue: 2500 }
    ]
};

// Current local data state, starting with defaults until data is fetched
let currentData = { ...DEFAULT_DATA }; 

// --- Helper Functions ---

const formatCurrency = (amount) => `${currencySymbol}${amount.toLocaleString('en-ZA')}`;

const formatDate = (dateString) => {
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    try {
        return new Date(dateString).toLocaleDateString('en-US', options);
    } catch (e) {
        return 'N/A';
    }
};

// --- API Simulation Functions (Mimicking MongoDB Backend Calls) ---

// Simulate fetching data from a MongoDB endpoint
function fetchDashboardData() {
    console.log("SIMULATING API CALL: Fetching data from MongoDB backend...");
    // Simulate network delay (e.g., 500ms)
    return new Promise(resolve => {
        setTimeout(() => {
            // In a real app, this would be the response from your Node/Express server.
            console.log("API Success: Data received.");
            resolve(DEFAULT_DATA); 
        }, 500);
    });
}

// Simulate saving data to a MongoDB endpoint (PATCH/PUT request)
function saveDashboardData(data) {
    console.log("SIMULATING API CALL: Saving data to MongoDB backend...");
    // Simulate network delay and successful response
    return new Promise(resolve => {
        setTimeout(() => {
            console.log("API Success: Data saved.");
            // In a real app, the server would save this to MongoDB.
            resolve(data); 
        }, 500);
    });
}

// --- UI Update Logic ---

function updateDashboard(data) {
    // 1. Dynamic Month Name
    const now = new Date();
    const currentMonth = now.toLocaleDateString('en-US', { month: 'long' });
    const progressHeaderEl = document.querySelector('.progress-header h3');
    if (progressHeaderEl) {
        progressHeaderEl.textContent = `${currentMonth} Progress`;
    }
    
    // 2. Main Balance Card & User Percentage
    document.getElementById('total-balance').textContent = formatCurrency(data.groupBalance);
    document.getElementById('user-contribution').textContent = formatCurrency(data.userContribution);
    
    // Calculate percentage based on current progress vs target progress
    const userProgressPercentage = Math.round((data.userContribution / data.targetProgress) * 100);
    const contributionEl = document.getElementById('user-contribution');
    
    let userPctSpan = document.getElementById('user-progress-pct');
    if (!userPctSpan) {
        userPctSpan = document.createElement('span');
        userPctSpan.id = 'user-progress-pct';
        userPctSpan.className = 'user-pct';
        contributionEl.parentNode.appendChild(userPctSpan);
    }
    userPctSpan.textContent = ``; // REMOVED THE PERCENTAGE TEXT AS REQUESTED


    // 3. Secondary Cards
    const totalMembers = data.activeMembers + data.missedContributors.length;
    document.getElementById('active-members').textContent = `${data.activeMembers}/${totalMembers}`;
    
    const recentPayoutEl = document.getElementById('recent-payout');
    if (recentPayoutEl) {
        recentPayoutEl.textContent = formatDate(data.recentPayout);
    }

    // 4. Progress Card Details
    const groupPercentage = Math.round((data.currentProgress / data.targetProgress) * 100);
    const remaining = data.targetProgress - data.currentProgress;

    document.getElementById('progress-percentage').textContent = `${groupPercentage}%`;
    document.getElementById('current-amount').textContent = formatCurrency(data.currentProgress);
    document.getElementById('target-amount').textContent = formatCurrency(data.targetProgress);
    document.getElementById('remaining-amount').textContent = `${formatCurrency(remaining)} remaining`;
    document.getElementById('progress-bar').style.width = `${groupPercentage}%`;

    
    // 5. Update Warning Banner Visibility and Details (The automatic update part)
    const warningEl = document.getElementById('missed-contributions-alert');
    const listEl = document.getElementById('missed-members-list');
    const missedCount = data.missedContributors ? data.missedContributors.length : 0;
    const toggleBtn = document.getElementById('toggle-details-btn');


    if (warningEl && listEl && toggleBtn) {
        if (missedCount > 0) {
            warningEl.style.display = 'block'; // Show the banner
            const detailText = warningEl.querySelector('.alert-text');
            detailText.textContent = `${missedCount} member${missedCount > 1 ? 's' : ''} missed contributions this month`;
            
            toggleBtn.style.display = 'block';

            // Render the list of missed members
            listEl.innerHTML = ''; // Clear existing list
            data.missedContributors.forEach(member => {
                const li = document.createElement('li');
                // Automatically adds the name, surname, and amount owing
                li.innerHTML = `<span>${member.name}</span><strong>${formatCurrency(member.amountDue)}</strong>`;
                listEl.appendChild(li);
            });
            
        } else {
            warningEl.style.display = 'none'; // Hide the banner
            if (listEl) listEl.style.display = 'none';
        }
    }
}

// --- Action Functions (now update via simulated API) ---

// Function to handle deposits or withdrawals (Transaction Simulation)
async function handleTransaction(amount, isUserContribution = true) {
    try {
        // Update local state first
        currentData.groupBalance += amount;

        if (amount > 0 && isUserContribution) {
            currentData.userContribution += amount;
            currentData.currentProgress += amount;
            currentData.currentProgress = Math.min(currentData.currentProgress, currentData.targetProgress);
        }
        
        // Save local state to simulated MongoDB
        await saveDashboardData(currentData);
        // We update UI immediately for quick feedback
        updateDashboard(currentData);
        
    } catch (error) {
        console.error("Error during transaction simulation:", error);
    }
}

// Function to handle the manual addition of a missed contribution
async function handleMissedContribution(name, amount) {
    try {
        if (!currentData.missedContributors) {
            currentData.missedContributors = [];
        }
        
        // Check if the member is already listed to avoid duplicates
        const alreadyMissed = currentData.missedContributors.some(m => m.name === name);
        
        if (!alreadyMissed) {
            // Update local state
            currentData.missedContributors.push({ name: name, amountDue: amount });
            currentData.activeMembers = Math.max(0, currentData.activeMembers - 1);
            
            // Save local state to simulated MongoDB
            await saveDashboardData(currentData);
            
            // Update UI
            updateDashboard(currentData);

            console.log(`${name} has been added to missed contributions and saved.`);
        }
    } catch (error) {
        console.error("Error adding missed contribution:", error);
    }
}

// Function to handle the dropdown toggle
function toggleDetails() {
    const listEl = document.getElementById('missed-members-list');
    const btn = document.getElementById('toggle-details-btn');
    
    const missedCount = currentData.missedContributors ? currentData.missedContributors.length : 0;
    if (missedCount === 0) return;

    if (listEl.style.display === 'block') {
        listEl.style.display = 'none';
        btn.innerHTML = 'View details &rarr;';
    } else {
        listEl.style.display = 'block';
        btn.innerHTML = 'Hide details &darr;';
    }
}

// --- Initial Load and Event Listener Setup ---
document.addEventListener('DOMContentLoaded', async () => {
    try {
        // 1. Fetch initial data from the simulated MongoDB API
        const initialData = await fetchDashboardData();
        currentData = initialData;

        // 2. Initial UI render
        updateDashboard(currentData);

        // 3. Attach the toggle function to the button
        const toggleBtn = document.getElementById('toggle-details-btn');
        if (toggleBtn) {
            toggleBtn.addEventListener('click', toggleDetails);
        }
        
        // 4. Ensure the list is hidden on load
        const listEl = document.getElementById('missed-members-list');
        if (listEl) {
            listEl.style.display = 'none';
        }
        
        // DEMO: Simulate adding a new missed contribution after 5 seconds 
        // by updating the simulated backend data.
        setTimeout(() => {
            handleMissedContribution('Thandi Nxumalo', 2500);
        }, 5000);

    } catch (error) {
        console.error("Failed to initialize dashboard:", error);
    }
});
