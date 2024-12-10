const apiEndpoint = 'https://y1ceks7lrg.execute-api.eu-west-1.amazonaws.com/Prod';

// Function to fetch and display storage units
async function fetchStorageUnits() {
    const storageEndpoint = `${apiEndpoint}/storage_units`;
    try {
        const response = await fetch(storageEndpoint);
        const units = await response.json();
        console.log(units);
        const unitsContainer = document.getElementById('storageUnits');
        unitsContainer.innerHTML = ''; // Clear previous units
        
        units.forEach(unit => {
            const unitDiv = document.createElement('div');
            unitDiv.className = 'unit';
            console.log(1);
            unitDiv.innerHTML = `
                <p>Unit Id: ${unit.unitid}</p>
                <p>Town: ${unit.Town}</p>
                <p>Unit Size: ${unit.Size}</p>
                <p>Status: ${unit.Status}</p>
                ${unit.Status === 'Available' ? `<button class="button" onclick="bookUnit('${unit.unitid}')">Book Now</button>` : ''}
                ${unit.Status === 'Reserved' ? `<button class="button" onclick="cancelRental('${unit.unitid}')">Cancel</button>` : ''}
            `;
            unitsContainer.appendChild(unitDiv);
        });
    } catch (error) {
        console.error('Error fetching storage units:', error);
    }
}

// Function to book a storage unit
async function bookUnit(unitId) {
    // const authToken = await checkAuthStatus();
    // if (!authToken) {
    //     login(); // Redirect to login if not authenticated
    //     return;
    // }

    const bookEndpoint = `${apiEndpoint}/storage_units/${unitId}`;
    try {
        const response = await fetch(bookEndpoint, { 
            method: 'POST', 
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        const result = await response.json();
        alert(result.message);
        fetchStorageUnits(); // Refresh the list
    } catch (error) {
        console.error('Error booking unit:', error);
    }
}

// Function to cancel a rental
async function cancelRental(unitId) {
    const authToken = await checkAuthStatus();
    if (!authToken) {
        login(); // Redirect to login if not authenticated
        return;
    }

    const cancelEndpoint = `${apiEndpoint}/storage_units/${unitId}/cancel`;
    try {
        const response = await fetch(cancelEndpoint, { 
            method: 'PUT', 
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        const result = await response.json();
        alert(result.message);
        fetchStorageUnits(); // Refresh the list after cancellation
    } catch (error) {
        console.error('Error canceling rental:', error);
    }
}

// Function to update the status of a storage unit
async function updateStatus(unitId, newStatus) {
    const authToken = localStorage.getItem('authToken');
    if (!authToken) {
        login();
        return;
    }

    const updateEndpoint = `${apiEndpoint}/storage_units/${unitId}/status/${newStatus}`;
    try {
        const response = await fetch(updateEndpoint, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
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

// Cognito login function
function login() {
    const cognitoLoginUrl = 'https://eu-west-1pv6wty3qq.auth.eu-west-1.amazoncognito.com/login?client_id=44t95jhbmn74mjqh99tn2lbhih&response_type=code&scope=aws.cognito.signin.user.admin+email+openid+phone+profile&redirect_uri=https%3A%2F%2Fmain.d2v7oqvnc2mjzz.amplifyapp.com%2F';
    window.location.href = cognitoLoginUrl;
}

// Cognito sign-out function
function signout() {
    localStorage.removeItem('authToken');
    window.location.href = '/';
}

// Handle Cognito redirect and store the token
async function handleCognitoRedirect() {
    const urlParams = new URLSearchParams(window.location.search);
    const authCode = urlParams.get('code');

    if (authCode) {
        const tokenResponse = await fetch('https://eu-west-1pv6wty3qq.auth.eu-west-1.amazoncognito.com/oauth2/token', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: new URLSearchParams({
                grant_type: 'authorization_code',
                code: authCode,
                redirect_uri: 'https://main.d2v7oqvnc2mjzz.amplifyapp.com',
                client_id: '44t95jhbmn74mjqh99tn2lbhih',
                client_secret: 'your-cognito-client-secret' // Replace with actual secret
            })
        });

        const tokenData = await tokenResponse.json();
        if (tokenData.id_token) {
            localStorage.setItem('authToken', tokenData.id_token);
            window.location.href = '/'; // Redirect to home or desired page
        } else {
            console.error('Failed to retrieve ID token.');
        }
    }
}

// Check authentication status
async function checkAuthStatus() {
    const authToken = localStorage.getItem('authToken');
    console.log(authToken);
    if (!authToken) {
        document.querySelector('.login-button').style.display = 'block';
        document.querySelector('.signout-button').style.display = 'none';
        return false;
    }

    try {
        const response = await fetch(`${apiEndpoint}/validateAuthToken`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            }
        });

        if (response.status === 200) {
            document.querySelector('.login-button').style.display = 'none';
            document.querySelector('.signout-button').style.display = 'block';
            return authToken;
        } else {
            document.querySelector('.login-button').style.display = 'block';
            document.querySelector('.signout-button').style.display = 'none';
            return false;
        }
    } catch (error) {
        console.error('Error checking auth status:', error);
        document.querySelector('.login-button').style.display = 'block';
        document.querySelector('.signout-button').style.display = 'none';
        return false;
    }
}

// Initialize app
handleCognitoRedirect();
fetchStorageUnits();
checkAuthStatus();
