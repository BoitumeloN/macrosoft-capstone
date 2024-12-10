const apiEndpoint = 'https://y1ceks7lrg.execute-api.eu-west-1.amazonaws.com/Prod';

// Function to check if the user is authenticated
async function checkAuthStatus() {
    const authToken = localStorage.getItem('authToken');
    if (!authToken) {
        document.querySelector('.login-button').style.display = 'block';
        document.querySelector('.signout-button').style.display = 'none';
        return null;
    }
    document.querySelector('.login-button').style.display = 'none';
    document.querySelector('.signout-button').style.display = 'block';
    return authToken;
}

// Fetch storage units from the backend
async function fetchStorageUnits() {
    const authToken = await checkAuthStatus();
    const apiEndpoint = `${apiEndpoint}/storage_units`;
    
    try {
        const response = await fetch(apiEndpoint, {
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        const units = await response.json();
        console.log(units);
        
        const unitsContainer = document.getElementById('storageUnits');
        unitsContainer.innerHTML = ''; // Clear previous units
        
        units.forEach(unit => {
            const unitDiv = document.createElement('div');
            unitDiv.className = 'unit';
            unitDiv.innerHTML = `
                <p>Unit Id: ${unit.unitid}</p>
                <p>Town: ${unit.Town}</p>
                <p>Unit Size: ${unit.Size}</p>
                <p>Status: ${unit.Status}</p>
                ${unit.Status === 'Available' ? `<button class="button" onclick="bookUnit('${unit.unitid}')">Book Now</button>` : ''}
                ${unit.Status === 'Reserved' ? `<button class="button" onclick="cancelRental('${unit.unitid}')">Cancel</button>` : ''}
                ${unit.Status === 'Rented' ? `<button class="button" onclick="updateStatus('${unit.unitid}', 'Available')">Make Available</button>` : ''}
            `;
            unitsContainer.appendChild(unitDiv);
        });
    } catch (error) {
        console.error('Error fetching storage units:', error);
    }
}

// Function to book a storage unit
async function bookUnit(unitId) {
    const authToken = await checkAuthStatus();
    if (!authToken) {
        login(); // Redirect to login if not authenticated
        return;
    }

    const apiEndpoint = `https://y1ceks7lrg.execute-api.eu-west-1.amazonaws.com/Prod/storage_units/${unitId}`;
    try {
        const response = await fetch(apiEndpoint, { method: 'POST', headers: { 'Authorization': `Bearer ${authToken}` } });
        const result = await response.json();
        alert(result.message);
        fetchStorageUnits(); // Refresh the list
    } catch (error) {
        console.error('Error booking unit:', error);
    }
}

// Function to update the status of a storage unit
async function updateStatus(unitId, newStatus) {
    const authToken = await checkAuthStatus();
    if (!authToken) {
        login(); // Redirect to login if not authenticated
        return;
    }

    const apiEndpoint = `https://y1ceks7lrg.execute-api.eu-west-1.amazonaws.com/Prod/storage_units/${unitId}/status/${newStatus}`;
    try {
        const response = await fetch(apiEndpoint, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}` // Include your Cognito token
            },
            body: JSON.stringify({ status: newStatus })
        });
        const result = await response.json();
        alert(result.message);
        fetchStorageUnits(); // Refresh the list after updating
    } catch (error) {
        console.error('Error updating status:', error);
    }
}

// Function to cancel a rental for a unit
async function cancelRental(unitId) {
    const authToken = await checkAuthStatus();
    if (!authToken) {
        login(); // Redirect to login if not authenticated
        return;
    }

    const apiEndpoint = `https://y1ceks7lrg.execute-api.eu-west-1.amazonaws.com/Prod/storage_units/${unitId}/cancel`;
    try {
        const response = await fetch(apiEndpoint, {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${authToken}` // Include your Cognito token
            }
        });
        const result = await response.json();
        alert(result.message);
        fetchStorageUnits(); // Refresh the list after cancellation
    } catch (error) {
        console.error('Error canceling rental:', error);
    }
}

// Login function - redirects to Cognito login page
function login() {
    const cognitoLoginUrl = 'https://eu-west-1pv6wty3qq.auth.eu-west-1.amazoncognito.com/login?client_id=44t95jhbmn74mjqh99tn2lbhih&response_type=code&scope=aws.cognito.signin.user.admin+email+openid+phone+profile&redirect_uri=https%3A%2F%2Fmain.d2v7oqvnc2mjzz.amplifyapp.com%2F';
    window.location.href = cognitoLoginUrl;
}

// Function to sign out
function signout() {
    localStorage.removeItem('authToken');
    window.location.href = '/';
}

// Extract authorization code from the URL
function extractAuthCode() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('code');
}

// Exchange the authorization code for access tokens
async function exchangeAuthCodeForToken(authCode) {
    const clientId = '44t95jhbmn74mjqh99tn2lbhih'; // Replace with your client ID
    const redirectUri = 'https://main.d2v7oqvnc2mjzz.amplifyapp.com/'; // Your redirect URI
    const tokenEndpoint = 'https://eu-west-1pv6wty3qq.auth.eu-west-1.amazoncognito.com/oauth2/token';

    const data = new URLSearchParams();
    data.append('grant_type', 'authorization_code');
    data.append('client_id', clientId);
    data.append('code', authCode);
    data.append('redirect_uri', redirectUri);

    try {
        const response = await fetch(tokenEndpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: data,
        });

        if (!response.ok) {
            throw new Error('Failed to exchange authorization code for tokens');
        }

        const tokens = await response.json();
        localStorage.setItem('authToken', tokens.access_token); // Store the access token
        localStorage.setItem('idToken', tokens.id_token);       // Optionally store ID token
        alert('Login successful!');
        window.location.href = '/'; // Redirect to the homepage
    } catch (error) {
        console.error('Error exchanging auth code for tokens:', error);
    }
}

// Check if the page was redirected with a code parameter
window.onload = () => {
    const authCode = extractAuthCode();
    if (authCode) {
        exchangeAuthCodeForToken(authCode);
    }
};
