// --- Dashboard Data ---
let currentData = {
    groupBalance: 125450,
    userContribution: 2500,
    activeMembers: 10,
    totalMembers: 12,
    nextMeeting: 'Dec 15, 2024',
    recentPayout: 'Sep 30, 2024',
    currentProgress: 25000,
    targetProgress: 30000
};

const currencySymbol = 'R';

// Format numbers as South African currency
const formatCurrency = (amount) => `${currencySymbol}${amount.toLocaleString('en-ZA')}`;

// Update the dashboard UI
function updateDashboard(data) {
    document.getElementById('total-balance').textContent = formatCurrency(data.groupBalance);
    document.getElementById('user-contribution').textContent = formatCurrency(data.userContribution);
    document.getElementById('active-members').textContent = `${data.activeMembers}/${data.totalMembers}`;
    document.getElementById('next-meeting').textContent = data.nextMeeting;
    document.getElementById('recent-payout').textContent = data.recentPayout;

    const percentage = Math.round((data.currentProgress / data.targetProgress) * 100);
    const remaining = data.targetProgress - data.currentProgress;

    document.getElementById('progress-percentage').textContent = `${percentage}%`;
    document.getElementById('current-amount').textContent = formatCurrency(data.currentProgress);
    document.getElementById('target-amount').textContent = formatCurrency(data.targetProgress);
    document.getElementById('remaining-amount').textContent = `${formatCurrency(remaining)} remaining`;
    document.getElementById('progress-bar').style.width = `${percentage}%`;

    console.log(`Dashboard updated: New balance = ${formatCurrency(data.groupBalance)}`);
}

// Handle deposits or withdrawals
function handleTransaction(amount) {
    currentData.groupBalance += amount;

    if (amount > 0) {
        currentData.userContribution += amount;
        currentData.currentProgress += amount;
    }

    updateDashboard(currentData);
}

// --- Initial Load ---
updateDashboard(currentData);

// --- Demo Transactions (optional: remove or keep for testing) ---
setTimeout(() => handleTransaction(4000), 5000);   // R4,000 deposit after 5s
setTimeout(() => handleTransaction(-1500), 10000); // R1,500 withdrawal after 10s
