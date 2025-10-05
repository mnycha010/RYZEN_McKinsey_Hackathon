// --- Global Constants and State ---
const currencySymbol = 'R';
const API_URL = '/api/dashboard'; // Simulated API endpoint

// Simulated Profile Data that would come from a Sign-in/Auth service
const AUTH_PROFILE_DATA = {
    userName: 'Thabo Mbeki', // New simulated user name from auth
    userEmail: 'thabo.mbeki@union.co.za', // New simulated email from auth
    joinDate: '2022-10-25', // Simulated join date from auth
    userId: 'user_mbeki_12345', 
    
    // 🔥 KEY CHANGE: Simulate using the KYC Selfie as the Profile Picture
    // In a real app, this path would point to the verified image file on the server.
    profilePicUrl: `/assets/profiles/${'user_mbeki_12345'}_kyc_selfie.jpg`, 
};

// Simulated token returned after successful sign-in
const USER_AUTH_TOKEN = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiJ1c2VyX21iZWtpXzEyMzQ1IiwiaWF0IjoxNjMyMDU4NzAwfQ.SFlk5w4R6c_wPZJq0Lg7gq9oT7GZlF-J0D0Y5Nn7QoI';


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
    ],
    // These profile fields will be OVERWRITTEN by the auth data fetch
    userName: 'Sipho Zulu',
    userEmail: 'sipho.zulu@example.com',
    joinDate: '2023-01-15',
    profilePicUrl: 'https://placehold.co/80x80/007bff/ffffff?text=SZ'
};

// Current local data state, starting with defaults until data is fetched
let currentData = { ...DEFAULT_DATA }; 
let authToken = null; // Store the token here after sign-in

// Store original values for the profile form to allow 'Cancel' to revert
let originalProfileValues = {};
const PROFILE_FORM_ID = 'personalInfoForm';

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

// Simulate fetching profile data from an Authentication service (Sign-up/in data)
function fetchUserProfile() {
    console.log("SIMULATING AUTH CALL: Fetching user profile data...");
    // Returns both the profile data and the simulated token
    return new Promise(resolve => {
        setTimeout(() => {
            console.log("Auth Success: Profile data and token received.");
            resolve({ profile: AUTH_PROFILE_DATA, token: USER_AUTH_TOKEN }); 
        }, 300); 
    });
}

// Simulate fetching dashboard data from a MongoDB endpoint
function fetchDashboardData(token) {
    if (!token) {
        console.error("SECURITY ALERT: Cannot fetch data. Authentication token is missing.");
        return Promise.reject(new Error("Unauthorized Access"));
    }

    console.log(`SIMULATING API CALL: Fetching data for ${AUTH_PROFILE_DATA.userId}. (Token sent in Headers)`);
    
    // Simulate network delay (e.g., 500ms)
    return new Promise(resolve => {
        setTimeout(() => {
            console.log("API Success: Dashboard data received.");
            resolve(DEFAULT_DATA); 
        }, 500);
    });
}

// Simulate saving data to a MongoDB endpoint (PATCH/PUT request)
function saveDashboardData(data, token) {
    if (!token) {
        console.error("SECURITY ALERT: Cannot save data. Authentication token is missing.");
        return Promise.reject(new Error("Unauthorized Access"));
    }
    
    console.log(`SIMULATING API CALL: Saving data for ${AUTH_PROFILE_DATA.userId}. (Token sent in Headers)`);
    
    // Simulate network delay and successful response
    return new Promise(resolve => {
        setTimeout(() => {
            console.log("API Success: Data saved.");
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
    
    // 2. Main Balance Card & User Contribution
    const totalBalanceEl = document.getElementById('total-balance');
    if (totalBalanceEl) totalBalanceEl.textContent = formatCurrency(data.groupBalance);

    const userContributionEl = document.getElementById('user-contribution');
    if (userContributionEl) userContributionEl.textContent = formatCurrency(data.userContribution);
    
    let userPctSpan = document.getElementById('user-progress-pct');
    if (userPctSpan) {
        userPctSpan.remove();
    }

    // 3. Secondary Cards
    const totalMembers = data.activeMembers + data.missedContributors.length;
    const activeMembersEl = document.getElementById('active-members');
    if (activeMembersEl) activeMembersEl.textContent = `${data.activeMembers}/${totalMembers}`;
    
    const recentPayoutEl = document.getElementById('recent-payout');
    if (recentPayoutEl) {
        recentPayoutEl.textContent = formatDate(data.recentPayout);
    }

    // 4. Progress Card Details
    const groupPercentage = Math.round((data.currentProgress / data.targetProgress) * 100);
    const remaining = data.targetProgress - data.currentProgress;

    const progressPercentageEl = document.getElementById('progress-percentage');
    if (progressPercentageEl) progressPercentageEl.textContent = `${groupPercentage}%`;

    const currentAmountEl = document.getElementById('current-amount');
    if (currentAmountEl) currentAmountEl.textContent = formatCurrency(data.currentProgress);

    const targetAmountEl = document.getElementById('target-amount');
    if (targetAmountEl) targetAmountEl.textContent = formatCurrency(data.targetProgress);

    const remainingAmountEl = document.getElementById('remaining-amount');
    if (remainingAmountEl) remainingAmountEl.textContent = `${formatCurrency(remaining)} remaining`;

    const progressBarEl = document.getElementById('progress-bar');
    if (progressBarEl) progressBarEl.style.width = `${groupPercentage}%`;

    
    // 5. Update Warning Banner Visibility and Details
    const warningEl = document.getElementById('missed-contributions-alert');
    const listEl = document.getElementById('missed-members-list');
    const missedCount = data.missedContributors ? data.missedContributors.length : 0;
    const toggleBtn = document.getElementById('toggle-details-btn');


    if (warningEl && listEl && toggleBtn) {
        if (missedCount > 0) {
            warningEl.style.display = 'block'; 
            const detailText = warningEl.querySelector('.alert-text');
            if (detailText) detailText.textContent = `${missedCount} member${missedCount > 1 ? 's' : ''} missed contributions this month`;
            
            toggleBtn.style.display = 'block';

            // Render the list of missed members
            listEl.innerHTML = ''; 
            data.missedContributors.forEach(member => {
                const li = document.createElement('li');
                li.innerHTML = `<span>${member.name}</span><strong>${formatCurrency(member.amountDue)}</strong>`;
                listEl.appendChild(li);
            });
            
        } else {
            warningEl.style.display = 'none'; 
            if (listEl) listEl.style.display = 'none';
        }
    }
    
    // 6. Update Profile Card and Form Inputs
    const profileNameEl = document.getElementById('profile-name');
    if (profileNameEl) profileNameEl.textContent = data.userName;
    
    const profileEmailEl = document.getElementById('profile-email');
    if (profileEmailEl) profileEmailEl.textContent = data.userEmail;
    
    const profileJoinDateEl = document.getElementById('profile-join-date');
    if (profileJoinDateEl) profileJoinDateEl.textContent = formatDate(data.joinDate);
    
    // 🌟 Profile Picture Update
    const profileImageEl = document.getElementById('profile-image');
    if (profileImageEl) profileImageEl.src = data.profilePicUrl; 
    
    // Populate the EDITABLE form fields on the profile page
    const firstNameInput = document.getElementById('firstName');
    const lastNameInput = document.getElementById('lastName');
    const emailInput = document.getElementById('email');
    
    const nameParts = data.userName.split(' ');
    
    if (firstNameInput) firstNameInput.value = nameParts[0] || '';
    if (lastNameInput) lastNameInput.value = nameParts.slice(1).join(' ') || '';
    if (emailInput) emailInput.value = data.userEmail;

}

// --- PROFILE PAGE LOGIC ---

/**
 * Captures the current values of the profile form inputs to the originalProfileValues
 * and disables the form inputs (view mode).
 */
function captureOriginalValues() {
    const formInputs = document.querySelectorAll(`#${PROFILE_FORM_ID} input`);
    const nameParts = currentData.userName.split(' ');
    
    originalProfileValues = {
        firstName: nameParts[0] || '',
        lastName: nameParts.slice(1).join(' ') || '',
        email: currentData.userEmail,
        phone: document.getElementById('phone')?.value || '',
        address: document.getElementById('address')?.value || ''
    };
    
    // Set the DOM inputs to disabled and the edit state to 'view'
    formInputs.forEach(input => input.setAttribute('disabled', 'disabled'));
    document.querySelector('.btn-outline-primary')?.classList.remove('d-none');
    document.getElementById('save-buttons')?.classList.add('d-none');
}

/**
 * Toggles the profile form into edit mode, enabling inputs and showing save buttons.
 */
function enableProfileEdit() {
    const formInputs = document.querySelectorAll(`#${PROFILE_FORM_ID} input`);
    formInputs.forEach(input => {
        if (input.id === 'firstName' || input.id === 'lastName' || input.id === 'email' || input.id === 'phone' || input.id === 'address') {
            input.removeAttribute('disabled');
        }
    });
    document.querySelector('.btn-outline-primary')?.classList.add('d-none');
    document.getElementById('save-buttons')?.classList.remove('d-none');
}

/**
 * Reverts the form fields to the captured original values and exits edit mode.
 */
function cancelProfileEdit() {
    const firstNameInput = document.getElementById('firstName');
    const lastNameInput = document.getElementById('lastName');
    const emailInput = document.getElementById('email');
    const phoneInput = document.getElementById('phone');
    const addressInput = document.getElementById('address');
    
    // Restore original values
    if (firstNameInput) firstNameInput.value = originalProfileValues.firstName;
    if (lastNameInput) lastNameInput.value = originalProfileValues.lastName;
    if (emailInput) emailInput.value = originalProfileValues.email;
    if (phoneInput) phoneInput.value = originalProfileValues.phone;
    if (addressInput) addressInput.value = originalProfileValues.address;
    
    captureOriginalValues(); // This disables the form inputs and reverts state
}


/**
 * Handles the submission of the profile form, simulates an API call, and updates state.
 * @param {Event} e - The form submission event.
 */
async function saveProfileChanges(e) {
    e.preventDefault();

    const firstName = document.getElementById('firstName').value.trim();
    const lastName = document.getElementById('lastName').value.trim();
    const email = document.getElementById('email').value.trim();

    if (!firstName || !lastName || !email) {
        alert("Please ensure First Name, Surname, and Email are filled.");
        return;
    }
    
    const newUserName = `${firstName} ${lastName}`;
    
    const profileChanges = {
        userName: newUserName,
        userEmail: email,
    };
    
    try {
        // Update local state (currentData) and the global AUTH_PROFILE_DATA
        currentData = { ...currentData, ...profileChanges };
        AUTH_PROFILE_DATA.userName = newUserName;
        AUTH_PROFILE_DATA.userEmail = email;
        
        // Simulate saving the updated user profile data
        await saveDashboardData(currentData, authToken); 

        // Re-capture and update UI
        updateDashboard(currentData); 
        captureOriginalValues(); 

        alert('Profile updated successfully! ✅');
        
    } catch (error) {
        console.error("Failed to save profile changes:", error);
        alert('Failed to save profile. Please try again. ⚠️');
    }
}


// --- Action Functions (for Dashboard interaction) ---

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
        
        // Save local state to simulated MongoDB, passing the token
        await saveDashboardData(currentData, authToken);
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
        
        const alreadyMissed = currentData.missedContributors.some(m => m.name === name);
        
        if (!alreadyMissed) {
            // Update local state
            currentData.missedContributors.push({ name: name, amountDue: amount });
            currentData.activeMembers = Math.max(0, currentData.activeMembers - 1);
            
            await saveDashboardData(currentData, authToken);
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
        // 1. Fetch user profile data and token (Simulated Sign-in/Auth)
        const authResult = await fetchUserProfile();
        authToken = authResult.token; 
        
        // 2. Fetch initial dashboard data (Simulated MongoDB), pass the token
        const initialData = await fetchDashboardData(authToken);
        
        // 3. Combine and set current data state, prioritizing profile data
        currentData = { ...initialData, ...authResult.profile };

        // 4. Initial UI render
        updateDashboard(currentData);
        
        // 5. Initialize profile form state and attach handlers
        captureOriginalValues(); 
        
        const editBtn = document.querySelector('.btn-outline-primary');
        const cancelBtn = document.getElementById('cancelEdit');
        const profileForm = document.getElementById(PROFILE_FORM_ID);

        if (editBtn) editBtn.addEventListener('click', enableProfileEdit);
        if (cancelBtn) cancelBtn.addEventListener('click', cancelProfileEdit);
        if (profileForm) profileForm.addEventListener('submit', saveProfileChanges);
        
        // 6. Attach the toggle function to the dashboard's missed contributions button
        const toggleBtn = document.getElementById('toggle-details-btn');
        if (toggleBtn) {
            toggleBtn.addEventListener('click', toggleDetails);
        }
        
        // 7. Ensure the missed members list is hidden on load
        const listEl = document.getElementById('missed-members-list');
        if (listEl) {
            listEl.style.display = 'none';
        }
        
        // DEMO: Simulate adding a new missed contribution after 5 seconds 
        setTimeout(() => {
            handleMissedContribution('Thandi Nxumalo', 2500);
        }, 5000);

    } catch (error) {
        console.error("Failed to initialize application:", error);
    }
});